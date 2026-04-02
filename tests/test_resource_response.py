"""Tests for round-robin multi-response resource handling."""

import pytest

from sovd_server.resource_response import (
    data_for_list_view,
    data_resource_response_variants,
    fault_response_variants,
    mode_response_variants,
    operation_response_variants,
    pick_data_resource_response,
    pick_fault_response,
    pick_mode_response,
    pick_operation_response,
    reset_counters,
)


@pytest.fixture(autouse=True)
def _reset_rr():
    reset_counters()
    yield
    reset_counters()


def test_legacy_data_resource_single_200():
    r = {
        "id": "X",
        "name": "N",
        "data": {"v": 1},
        "tags": [],
    }
    variants = data_resource_response_variants(r)
    assert len(variants) == 1
    assert variants[0][0] == 200
    assert variants[0][1]["id"] == "X"
    assert variants[0][1]["data"]["v"] == 1


def test_data_round_robin_order():
    r = {
        "id": "R1",
        "name": "N",
        "data": {"v": 0},
        "responses": [
            {"status": 200, "body": {"a": 1}},
            {"status": 404, "body": {"error": "x"}},
        ],
    }
    ep = "/engine/ecu"
    assert pick_data_resource_response(ep, r) == (200, {"a": 1})
    assert pick_data_resource_response(ep, r) == (404, {"error": "x"})
    assert pick_data_resource_response(ep, r) == (200, {"a": 1})


def test_operation_round_robin():
    op = {
        "id": "OP1",
        "responses": [
            {"status": 201, "body": {"ok": True}},
            {"status": 500, "body": {"fail": True}},
        ],
    }
    ep = "/engine/ecu"
    assert pick_operation_response(ep, op) == (201, {"ok": True})
    assert pick_operation_response(ep, op) == (500, {"fail": True})
    assert pick_operation_response(ep, op) == (201, {"ok": True})


def test_legacy_operation_uses_response_success():
    op = {
        "id": "OP2",
        "response_success": {"status": "success", "message": "m"},
    }
    variants = operation_response_variants(op)
    assert variants == [(200, {"status": "success", "message": "m"})]


def test_data_for_list_prefers_data_key():
    r = {
        "id": "R1",
        "data": {"list": True},
        "responses": [{"status": 200, "body": {"data": {"list": False}}}],
    }
    assert data_for_list_view(r) == {"list": True}


def test_data_for_list_from_first_response():
    r = {
        "id": "R1",
        "responses": [{"status": 200, "body": {"data": {"from": "resp"}}}],
    }
    assert data_for_list_view(r) == {"from": "resp"}


def test_fault_round_robin():
    fault = {
        "id": "F1",
        "name": "N",
        "description": "d",
        "responses": [
            {"status": 200, "body": {"a": 1}},
            {"status": 418, "body": {"teapot": True}},
        ],
    }
    ep = "/engine/ecu"
    assert pick_fault_response(ep, fault) == (200, {"a": 1})
    assert pick_fault_response(ep, fault) == (418, {"teapot": True})
    assert pick_fault_response(ep, fault) == (200, {"a": 1})


def test_mode_round_robin():
    mode = {
        "id": "M1",
        "name": "N",
        "description": "d",
        "responses": [
            {"status": 200, "body": {"x": 1}},
            {"status": 500, "body": {"err": "e"}},
        ],
    }
    ep = "/camera/front"
    assert pick_mode_response(ep, mode) == (200, {"x": 1})
    assert pick_mode_response(ep, mode) == (500, {"err": "e"})
    assert pick_mode_response(ep, mode) == (200, {"x": 1})


def test_fault_mode_independent_keys():
    """Different resource kinds / ids do not share round-robin state."""
    f = {
        "id": "F1",
        "name": "n",
        "description": "d",
        "responses": [{"body": {"k": "f"}}],
    }
    m = {
        "id": "M1",
        "name": "n",
        "description": "d",
        "responses": [{"body": {"k": "m"}}],
    }
    ep = "/engine/ecu"
    assert pick_fault_response(ep, f) == (200, {"k": "f"})
    assert pick_mode_response(ep, m) == (200, {"k": "m"})
    assert pick_fault_response(ep, f) == (200, {"k": "f"})


def test_legacy_fault_variants_single_200():
    fault = {
        "id": "ECU-001",
        "name": "N",
        "description": "d",
        "severity": "warning",
        "scope": "system",
    }
    v = fault_response_variants(fault)
    assert len(v) == 1
    assert v[0][0] == 200
    assert v[0][1]["item"]["code"] == "ECU-001"


def test_legacy_mode_variants_single_200():
    mode = {
        "id": "ECU-NORMAL",
        "name": "Normal",
        "description": "d",
    }
    v = mode_response_variants(mode)
    assert len(v) == 1
    assert v[0][0] == 200
    assert v[0][1]["id"] == "ECU-NORMAL"
