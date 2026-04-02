#!/usr/bin/env python3
"""
Round-robin HTTP response selection from YAML resource definitions.

YAML may define ``responses`` (list of ``status`` + ``body``). If absent, legacy
single-response behavior is preserved (200 + existing ``data`` / ``response_success``).
"""

from __future__ import annotations

import threading
from typing import Any, Dict, List, Tuple

_lock = threading.Lock()
_counters: Dict[str, int] = {}


def round_robin_key(kind: str, entity_path: str, resource_id: str) -> str:
    return f"{kind}:{entity_path}:{resource_id}"


def _next_index(key: str, n: int) -> int:
    if n <= 0:
        return 0
    with _lock:
        idx = _counters.get(key, 0)
        _counters[key] = (idx + 1) % n
        return idx


def reset_counters() -> None:
    """Clear round-robin state (e.g. for tests)."""
    with _lock:
        _counters.clear()


def data_for_list_view(resource: Dict[str, Any]) -> Any:
    """Value used in GET .../data collection when building DataResource items."""
    if resource.get("data") is not None:
        return resource["data"]
    responses = resource.get("responses") or []
    if responses:
        body = responses[0].get("body") or {}
        if isinstance(body, dict) and "data" in body:
            return body["data"]
        return body
    return {}


def data_resource_response_variants(
    resource: Dict[str, Any],
) -> List[Tuple[int, Dict[str, Any]]]:
    """
    Build ordered list of (http_status, json_body) for GET .../data/{id}.
    Legacy: one entry (200, DataResource.to_dict()).
    """
    if resource.get("responses"):
        out: List[Tuple[int, Dict[str, Any]]] = []
        for item in resource["responses"]:
            status = int(item.get("status", 200))
            body = item.get("body")
            if body is None:
                body = {}
            elif not isinstance(body, dict):
                body = {"value": body}
            out.append((status, body))
        return out if out else [_legacy_data_resource_tuple(resource)]

    return [_legacy_data_resource_tuple(resource)]


def _legacy_data_resource_tuple(resource: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    from sovd_server.models.data_resource import DataResource

    dr = DataResource(
        id=resource["id"],
        name=resource["name"],
        data=resource["data"],
        _schema=resource.get("schema"),
        tags=resource.get("tags", []),
    )
    return (200, dr.to_dict())


def operation_response_variants(
    operation: Dict[str, Any],
) -> List[Tuple[int, Dict[str, Any]]]:
    """Ordered (status, body) for POST .../operations/{id}."""
    if operation.get("responses"):
        out: List[Tuple[int, Dict[str, Any]]] = []
        for item in operation["responses"]:
            status = int(item.get("status", 200))
            body = item.get("body")
            if body is None:
                body = {}
            elif not isinstance(body, dict):
                body = {"value": body}
            out.append((status, body))
        return out if out else [_legacy_operation_tuple(operation)]
    return [_legacy_operation_tuple(operation)]


def _legacy_operation_tuple(operation: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    body = dict(operation.get("response_success") or {})
    return (200, body)


def pick_data_resource_response(
    entity_path: str, resource: Dict[str, Any]
) -> Tuple[int, Dict[str, Any]]:
    variants = data_resource_response_variants(resource)
    key = round_robin_key("data", entity_path, resource["id"])
    i = _next_index(key, len(variants))
    return variants[i]


def pick_operation_response(
    entity_path: str, operation: Dict[str, Any]
) -> Tuple[int, Dict[str, Any]]:
    variants = operation_response_variants(operation)
    key = round_robin_key("operation", entity_path, operation["id"])
    i = _next_index(key, len(variants))
    return variants[i]


def _legacy_fault_tuple(fault_data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    from sovd_server.models.fault import Fault
    from sovd_server.models.fault_reference import FaultReference
    from sovd_server.models.fault_status import FaultStatus

    fault_status = FaultStatus(
        test_failed="false",
        confirmed_dtc="false",
        aggregated_status=fault_data.get("status", "inactive"),
    )
    fault_ref = FaultReference(
        code=fault_data["id"],
        scope=fault_data.get("scope", "system"),
        display_code=fault_data["id"],
        fault_name=fault_data["name"],
        severity=fault_data.get("severity", "warning"),
        status=fault_status,
    )
    fault = Fault(item=fault_ref)
    return (200, fault.to_dict())


def fault_response_variants(
    fault_data: Dict[str, Any],
) -> List[Tuple[int, Dict[str, Any]]]:
    """GET /faults/{id} — optional ``responses`` list; else legacy Fault JSON."""
    if fault_data.get("responses"):
        out: List[Tuple[int, Dict[str, Any]]] = []
        for item in fault_data["responses"]:
            status = int(item.get("status", 200))
            body = item.get("body")
            if body is None:
                body = {}
            elif not isinstance(body, dict):
                body = {"value": body}
            out.append((status, body))
        return out if out else [_legacy_fault_tuple(fault_data)]
    return [_legacy_fault_tuple(fault_data)]


def pick_fault_response(
    entity_path: str, fault_data: Dict[str, Any]
) -> Tuple[int, Dict[str, Any]]:
    variants = fault_response_variants(fault_data)
    key = round_robin_key("fault", entity_path, fault_data["id"])
    i = _next_index(key, len(variants))
    return variants[i]


def _legacy_mode_tuple(mode_data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    from sovd_server.models.mode import Mode

    mode = Mode(
        id=mode_data["id"],
        name=mode_data["name"],
        value=mode_data.get("value", mode_data["id"]),
        description=mode_data["description"],
    )
    return (200, mode.to_dict())


def mode_response_variants(
    mode_data: Dict[str, Any],
) -> List[Tuple[int, Dict[str, Any]]]:
    """GET /modes/{id} — optional ``responses`` list; else legacy Mode JSON."""
    if mode_data.get("responses"):
        out: List[Tuple[int, Dict[str, Any]]] = []
        for item in mode_data["responses"]:
            status = int(item.get("status", 200))
            body = item.get("body")
            if body is None:
                body = {}
            elif not isinstance(body, dict):
                body = {"value": body}
            out.append((status, body))
        return out if out else [_legacy_mode_tuple(mode_data)]
    return [_legacy_mode_tuple(mode_data)]


def pick_mode_response(
    entity_path: str, mode_data: Dict[str, Any]
) -> Tuple[int, Dict[str, Any]]:
    variants = mode_response_variants(mode_data)
    key = round_robin_key("mode", entity_path, mode_data["id"])
    i = _next_index(key, len(variants))
    return variants[i]
