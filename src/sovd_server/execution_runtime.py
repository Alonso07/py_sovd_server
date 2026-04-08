"""
In-memory operation executions for ISO paths:

  POST   /{entity}/operations/{op}/executions
  GET    /{entity}/operations/{op}/executions
  GET    /{entity}/operations/{op}/executions/{execution-id}
  DELETE /{entity}/operations/{op}/executions/{execution-id}

See ``sovd-api.yaml`` (DIS 17978-3 Part 3 API) OperationExecution / ExecutionCollection.
"""

from __future__ import annotations

import copy
import threading
import uuid
from typing import Any, Dict, List, Optional, Tuple

_lock = threading.Lock()
_records: Dict[Tuple[str, str, str], Dict[str, Any]] = {}


def reset() -> None:
    with _lock:
        _records.clear()


def _key(
    entity_path: str, operation_id: str, execution_id: str
) -> Tuple[str, str, str]:
    return (entity_path, operation_id, execution_id)


def create(
    entity_path: str, operation_id: str, parameters: Optional[Dict[str, Any]]
) -> str:
    execution_id = f"exec-{uuid.uuid4().hex[:16]}"
    rec: Dict[str, Any] = {
        "id": execution_id,
        "status": "running",
    }
    if parameters:
        rec["parameters"] = copy.deepcopy(parameters)
    with _lock:
        _records[_key(entity_path, operation_id, execution_id)] = rec
    return execution_id


def list_ids(entity_path: str, operation_id: str) -> List[str]:
    with _lock:
        return [
            eid
            for (ep, op, eid) in _records
            if ep == entity_path and op == operation_id
        ]


def get_record(
    entity_path: str, operation_id: str, execution_id: str
) -> Optional[Dict[str, Any]]:
    with _lock:
        r = _records.get(_key(entity_path, operation_id, execution_id))
        return copy.deepcopy(r) if r is not None else None


def terminate(entity_path: str, operation_id: str, execution_id: str) -> bool:
    with _lock:
        k = _key(entity_path, operation_id, execution_id)
        if k not in _records:
            return False
        _records[k] = {
            "id": execution_id,
            "status": "terminated",
        }
        return True
