"""Flask test-client coverage for round-robin HTTP responses (enhanced server)."""

import json

import pytest

from sovd_server import app
from sovd_server.resource_response import reset_counters

ECU = "/engine/ecu"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def _reset_rr():
    reset_counters()
    yield
    reset_counters()


def test_e2e_data_resource_round_robin(client):
    r1 = client.get(f"{ECU}/data/RoundRobinDemo")
    assert r1.status_code == 200
    assert r1.get_json()["data"]["step"] == 1

    r2 = client.get(f"{ECU}/data/RoundRobinDemo")
    assert r2.status_code == 503
    assert r2.get_json()["code"] == "DEMO_RETRY"

    r3 = client.get(f"{ECU}/data/RoundRobinDemo")
    assert r3.status_code == 201
    assert r3.get_json()["data"]["step"] == 3


def test_e2e_operation_post_round_robin(client):
    r1 = client.post(
        f"{ECU}/operations/ECU-RR-DEMO",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert r1.status_code == 200
    assert r1.get_json()["message"] == "step A"

    r2 = client.post(
        f"{ECU}/operations/ECU-RR-DEMO",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert r2.status_code == 409
    assert r2.get_json()["message"] == "step B"

    r3 = client.post(
        f"{ECU}/operations/ECU-RR-DEMO",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert r3.status_code == 200
    assert r3.get_json()["message"] == "step C"


def test_e2e_fault_single_round_robin(client):
    r1 = client.get(f"{ECU}/faults/ECU-RR")
    assert r1.status_code == 200
    assert r1.get_json()["demo"] == "fault-step-a"

    r2 = client.get(f"{ECU}/faults/ECU-RR")
    assert r2.status_code == 404
    assert r2.get_json()["error"] == "fault-not-found-demo"

    r3 = client.get(f"{ECU}/faults/ECU-RR")
    assert r3.status_code == 200
    assert r3.get_json()["demo"] == "fault-step-c"


def test_e2e_mode_single_round_robin(client):
    r1 = client.get(f"{ECU}/modes/ECU-RR-MODE")
    assert r1.status_code == 200
    assert r1.get_json()["demo"] == "mode-step-a"

    r2 = client.get(f"{ECU}/modes/ECU-RR-MODE")
    assert r2.status_code == 503
    assert r2.get_json()["error"] == "mode-unavailable"

    r3 = client.get(f"{ECU}/modes/ECU-RR-MODE")
    assert r3.status_code == 200
    assert r3.get_json()["demo"] == "mode-step-c"


def test_e2e_fault_not_found(client):
    r = client.get(f"{ECU}/faults/NO-SUCH-FAULT")
    assert r.status_code == 404


def test_e2e_legacy_fault_shape(client):
    """Fault without ``responses`` returns OpenAPI Fault JSON."""
    r = client.get(f"{ECU}/faults/ECU-001")
    assert r.status_code == 200
    body = r.get_json()
    assert body["item"]["code"] == "ECU-001"
    assert body["item"]["severity"] == 3
    assert body["item"]["status"]["mask"] == "FF"


def test_e2e_fault_collection_is_fault_references(client):
    """GET /faults returns FaultCollection with ``items`` as references (not nested Fault)."""
    r = client.get(f"{ECU}/faults")
    assert r.status_code == 200
    data = r.get_json()
    assert "items" in data
    assert data["items"]
    first = data["items"][0]
    assert "item" not in first
    assert first["code"] == "ECU-001"
    assert first["severity"] == 3
    assert first["status"]["aggregated_status"] == "active"
    assert first["status"]["mask"] == "FF"


def test_e2e_faults_filter_scope_and_mask(client):
    r = client.get(f"{ECU}/faults?scope=system")
    assert r.status_code == 200
    items = r.get_json()["items"]
    codes = [x["code"] for x in items]
    assert all(x["scope"] == "system" for x in items)
    assert "ECU-001" in codes
    assert "ECU-002" not in codes

    r2 = client.get(f"{ECU}/faults?mask=4")
    codes2 = {x["code"] for x in r2.get_json()["items"]}
    assert "ECU-001" in codes2
    assert "ECU-003" in codes2
    assert "ECU-002" not in codes2
