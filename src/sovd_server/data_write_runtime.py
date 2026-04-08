"""
In-memory overlays for ISO-style PUT .../data/{data-id} (DataResourceWrite).

Base values come from YAML; successful writes replace the effective ``data`` object
for GET collection and GET single until ``reset()`` (e.g. in tests).
"""

from __future__ import annotations

import copy
import threading
from typing import Any, Dict, Optional, Tuple

_lock = threading.Lock()
_overrides: Dict[Tuple[str, str], Dict[str, Any]] = {}


def reset() -> None:
    with _lock:
        _overrides.clear()


def get_override(entity_path: str, data_id: str) -> Optional[Dict[str, Any]]:
    with _lock:
        v = _overrides.get((entity_path, data_id))
        return copy.deepcopy(v) if v is not None else None


def set_override(entity_path: str, data_id: str, data: Dict[str, Any]) -> None:
    with _lock:
        _overrides[(entity_path, data_id)] = copy.deepcopy(data)
