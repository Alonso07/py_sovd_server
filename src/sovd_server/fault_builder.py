"""
ISO / OpenAPI-aligned fault references and query filtering.

GET /{entity}/faults supports query parameters ``severity`` (1–3), ``scope``,
``status`` (aggregated: active | inactive | pending), and optional ``mask``
(DTC status filter bitmask, hex or decimal). The OpenAPI spec lists the first
three; ``mask`` follows common diagnostic “status mask” semantics used with SOVD.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# Word severities in YAML → OpenAPI integer 1 (lowest) … 3 (highest)
_SEVERITY_WORD_TO_INT = {"warning": 1, "error": 2, "critical": 3}
_DEFAULT_SEVERITY_INT = 2


def yaml_severity_to_int(severity: Any) -> int:
    """Map YAML ``severity`` (word or int) to OpenAPI 1..3."""
    if isinstance(severity, int):
        if 1 <= severity <= 3:
            return severity
        return _DEFAULT_SEVERITY_INT
    if severity is None:
        return _DEFAULT_SEVERITY_INT
    s = str(severity).lower().strip()
    return _SEVERITY_WORD_TO_INT.get(s, _DEFAULT_SEVERITY_INT)


def _parse_byte_value(m: Any) -> Optional[int]:
    """Parse optional mask byte from YAML (int, hex string, decimal string)."""
    if m is None or isinstance(m, bool):
        return None
    if isinstance(m, int):
        return m & 0xFF
    s = str(m).strip()
    if not s:
        return None
    try:
        if s.lower().startswith("0x"):
            return int(s, 16) & 0xFF
        if len(s) == 2 and all(c in "0123456789abcdefABCDEF" for c in s):
            return int(s, 16) & 0xFF
        return int(s, 10) & 0xFF
    except ValueError:
        return None


def mask_byte_from_yaml(fault_data: Dict[str, Any]) -> Optional[int]:
    """Optional DTC/status mask byte from ``mask``, ``status_mask``, or ``dtc_mask``."""
    for key in ("mask", "status_mask", "dtc_mask"):
        b = _parse_byte_value(fault_data.get(key))
        if b is not None:
            return b
    return None


def mask_hex_for_status(fault_data: Dict[str, Any]) -> str:
    """Two-digit uppercase hex for ``FaultStatus.mask`` (``00`` if unset)."""
    b = mask_byte_from_yaml(fault_data)
    return f"{b:02X}" if b is not None else "00"


def parse_query_mask(raw: Optional[str]) -> Optional[int]:
    """Parse ``mask`` query parameter (``0x2A``, ``42``, etc.)."""
    if raw is None:
        return None
    t = str(raw).strip()
    if not t:
        return None
    try:
        if t.lower().startswith("0x"):
            return int(t, 16) & 0xFF
        if len(t) == 2 and all(c in "0123456789abcdefABCDEF" for c in t):
            return int(t, 16) & 0xFF
        return int(t, 10) & 0xFF
    except ValueError:
        return None


def fault_matches_query_mask(
    fault_data: Dict[str, Any], query_mask: Optional[int]
) -> bool:
    """If ``query_mask`` is set, keep faults whose YAML mask shares a set bit."""
    if query_mask is None:
        return True
    b = mask_byte_from_yaml(fault_data)
    if b is None:
        return True
    return (b & query_mask) != 0


def normalized_aggregated_status(fault_data: Dict[str, Any]) -> str:
    s = (fault_data.get("status") or "inactive").lower()
    if s in ("active", "inactive", "pending"):
        return s
    return "inactive"


def _status_bit(bits: Dict[str, Any], key: str, default: str = "0") -> str:
    v = bits.get(key)
    if v is None:
        return default
    if isinstance(v, bool):
        return "1" if v else "0"
    return "1" if str(v).strip() in ("1", "true", "True") else "0"


def build_fault_status(fault_data: Dict[str, Any]) -> Any:
    """Build ``FaultStatus`` with ISO-style 0/1 string fields and mask."""
    from sovd_server.models.fault_status import FaultStatus

    bits: Dict[str, Any] = fault_data.get("status_bits") or {}
    agg = normalized_aggregated_status(fault_data)
    return FaultStatus(
        test_failed=_status_bit(bits, "test_failed", "0"),
        test_failed_this_operation_cycle=_status_bit(
            bits, "test_failed_this_operation_cycle", "0"
        ),
        pending_dtc=_status_bit(bits, "pending_dtc", "0"),
        confirmed_dtc=_status_bit(bits, "confirmed_dtc", "0"),
        test_not_completed_since_last_clear=_status_bit(
            bits, "test_not_completed_since_last_clear", "0"
        ),
        test_failed_since_last_clear=_status_bit(
            bits, "test_failed_since_last_clear", "0"
        ),
        test_not_completed_this_operation_cycle=_status_bit(
            bits, "test_not_completed_this_operation_cycle", "0"
        ),
        warning_indicator_requested=_status_bit(
            bits, "warning_indicator_requested", "0"
        ),
        mask=mask_hex_for_status(fault_data),
        aggregated_status=agg,
    )


def build_fault_reference(fault_data: Dict[str, Any]) -> Any:
    """Build ``FaultReference`` for collection or ``Fault.item``."""
    from sovd_server.models.fault_reference import FaultReference

    return FaultReference(
        code=fault_data["id"],
        scope=fault_data.get("scope", "system"),
        display_code=fault_data["id"],
        fault_name=fault_data["name"],
        fault_translation_id=fault_data.get("fault_translation_id"),
        severity=yaml_severity_to_int(fault_data.get("severity")),
        status=build_fault_status(fault_data),
    )


def filter_faults_for_query(
    faults_data: List[Dict[str, Any]],
    *,
    severity: Optional[int] = None,
    scope: Optional[str] = None,
    status: Optional[str] = None,
    mask: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Apply OpenAPI-style GET /faults query filters."""
    out: List[Dict[str, Any]] = []
    for fd in faults_data:
        if (
            severity is not None
            and yaml_severity_to_int(fd.get("severity")) != severity
        ):
            continue
        if scope is not None and fd.get("scope", "system") != scope:
            continue
        if status is not None and normalized_aggregated_status(fd) != status.lower():
            continue
        if not fault_matches_query_mask(fd, mask):
            continue
        out.append(fd)
    return out
