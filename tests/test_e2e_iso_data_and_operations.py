"""
E2E checks for ISO DIS 17978-3 Part 3 (SOVD API) shapes implemented in ``sovd-api.yaml``.

The PDF/Markdown export ``docs/ISO_DIS_17978-3(en).md`` is the normative document; this
repository's OpenAPI file defines the concrete JSON shapes we assert here:

- ``DataResource``: required ``id``, ``data`` (GET .../data/{id})
- ``DataResourceWrite``: required ``data`` (PUT .../data/{id})
- ``OperationExecution``: required ``id``, ``status`` enum
- POST .../operations/{id}/executions → 202 and ``Location`` header
- DELETE .../executions/{id} → 204
"""

from __future__ import annotations

import json

import pytest

from sovd_server import app, data_write_runtime, execution_runtime
from sovd_server.resource_response import reset_counters

ECU = "/engine/ecu"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def _reset_runtime():
    reset_counters()
    data_write_runtime.reset()
    execution_runtime.reset()
    yield
    data_write_runtime.reset()
    execution_runtime.reset()
    reset_counters()


def test_iso_data_resource_get_shape_matches_openapi(client):
    r = client.get(f"{ECU}/data/ECUVoltage")
    assert r.status_code == 200
    body = r.get_json()
    assert isinstance(body, dict)
    assert "id" in body and body["id"] == "ECUVoltage"
    assert "data" in body and isinstance(body["data"], dict)
    assert "value" in body["data"]


def test_iso_data_resource_put_merge_and_get(client):
    r0 = client.get(f"{ECU}/data/ECUVoltage")
    assert r0.status_code == 200
    original = r0.get_json()["data"]

    w = client.put(
        f"{ECU}/data/ECUVoltage",
        data=json.dumps({"data": {"value": 12.5}}),
        content_type="application/json",
    )
    assert w.status_code == 200
    written = w.get_json()
    assert written["id"] == "ECUVoltage"
    assert written["data"]["value"] == 12.5
    assert written["data"].get("unit") == original.get("unit")

    r1 = client.get(f"{ECU}/data/ECUVoltage")
    assert r1.get_json()["data"]["value"] == 12.5


def test_iso_data_resource_put_requires_data_object(client):
    r = client.put(
        f"{ECU}/data/ECUVoltage",
        data=json.dumps({"not_data": 1}),
        content_type="application/json",
    )
    assert r.status_code == 400


def test_iso_operation_start_list_get_status_delete(client):
    start = client.post(
        f"{ECU}/operations/ECU-RESET/executions",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert start.status_code == 202
    ex = start.get_json()
    assert "id" in ex
    assert ex.get("status") == "running"

    loc = start.headers.get("Location")
    assert loc is not None
    assert ex["id"] in loc
    assert str(loc).rstrip("/").endswith(ex["id"])

    lst = client.get(f"{ECU}/operations/ECU-RESET/executions")
    assert lst.status_code == 200
    items = lst.get_json().get("items", [])
    assert any(i.get("id") == ex["id"] for i in items)

    st = client.get(
        f"{ECU}/operations/ECU-RESET/executions/{ex['id']}",
    )
    assert st.status_code == 200
    assert st.get_json()["status"] == "running"

    d = client.delete(
        f"{ECU}/operations/ECU-RESET/executions/{ex['id']}",
    )
    assert d.status_code == 204
    assert d.data == b""

    after = client.get(
        f"{ECU}/operations/ECU-RESET/executions/{ex['id']}",
    )
    assert after.status_code == 200
    assert after.get_json()["status"] == "terminated"


def test_iso_operation_executions_post_accepts_parameters(client):
    start = client.post(
        f"{ECU}/operations/ECU-RESET/executions",
        data=json.dumps({"parameters": {"foo": "bar"}}),
        content_type="application/json",
    )
    assert start.status_code == 202
    body = start.get_json()
    assert body["parameters"] == {"foo": "bar"}
