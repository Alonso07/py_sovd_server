"""
In-memory state for SOVD software-update flows (prepare / execute / status).
YAML defines available packages; this module tracks runtime progress for demos/tests.
"""

from __future__ import annotations

import threading
from typing import Any, Dict, List, Optional

_lock = threading.Lock()
# Packages registered via POST /updates (id -> body dict)
_registered: Dict[str, Dict[str, Any]] = {}
# Per-package status for GET .../status
_status: Dict[str, Dict[str, Any]] = {}


def reset() -> None:
    with _lock:
        _registered.clear()
        _status.clear()


def register_package(package_id: str, body: Dict[str, Any]) -> None:
    with _lock:
        _registered[package_id] = dict(body)


def get_registered(package_id: str) -> Optional[Dict[str, Any]]:
    with _lock:
        return dict(_registered[package_id]) if package_id in _registered else None


def list_registered_ids() -> List[str]:
    with _lock:
        return list(_registered.keys())


def delete_registered(package_id: str) -> bool:
    with _lock:
        return _registered.pop(package_id, None) is not None


def set_status(package_id: str, status: Dict[str, Any]) -> None:
    with _lock:
        _status[package_id] = dict(status)


def get_status(package_id: str) -> Optional[Dict[str, Any]]:
    with _lock:
        return dict(_status[package_id]) if package_id in _status else None


def merge_status(package_id: str, defaults: Dict[str, Any]) -> Dict[str, Any]:
    with _lock:
        base = dict(defaults)
        if package_id in _status:
            base.update(_status[package_id])
        return base
