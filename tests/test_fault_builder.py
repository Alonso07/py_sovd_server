"""Unit tests for fault query filtering and OpenAPI-aligned references."""

from sovd_server.fault_builder import (
    filter_faults_for_query,
    parse_query_mask,
    yaml_severity_to_int,
)


def test_yaml_severity_words():
    assert yaml_severity_to_int("warning") == 1
    assert yaml_severity_to_int("error") == 2
    assert yaml_severity_to_int("critical") == 3
    assert yaml_severity_to_int(2) == 2


def test_parse_query_mask():
    assert parse_query_mask(None) is None
    assert parse_query_mask("") is None
    assert parse_query_mask("1") == 1
    assert parse_query_mask("0x01") == 1
    assert parse_query_mask("FF") == 255


def test_filter_scope():
    faults = [
        {"id": "A", "name": "n", "scope": "system", "severity": "warning"},
        {"id": "B", "name": "n", "scope": "ecu", "severity": "warning"},
    ]
    r = filter_faults_for_query(faults, scope="ecu")
    assert [x["id"] for x in r] == ["B"]


def test_filter_severity_int():
    faults = [
        {"id": "A", "name": "n", "scope": "s", "severity": "critical"},
        {"id": "B", "name": "n", "scope": "s", "severity": "warning"},
    ]
    r = filter_faults_for_query(faults, severity=3)
    assert [x["id"] for x in r] == ["A"]


def test_filter_status():
    faults = [
        {"id": "A", "name": "n", "scope": "s", "severity": "w", "status": "active"},
        {"id": "B", "name": "n", "scope": "s", "severity": "w", "status": "inactive"},
    ]
    r = filter_faults_for_query(faults, status="inactive")
    assert [x["id"] for x in r] == ["B"]


def test_filter_mask_intersection():
    faults = [
        {"id": "A", "name": "n", "scope": "s", "severity": "w", "mask": "FF"},
        {"id": "B", "name": "n", "scope": "s", "severity": "w", "mask": "04"},
    ]
    r = filter_faults_for_query(faults, mask=0x01)
    assert set(x["id"] for x in r) == {"A"}
    r2 = filter_faults_for_query(faults, mask=0x04)
    assert set(x["id"] for x in r2) == {"A", "B"}
