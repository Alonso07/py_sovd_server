"""
Pytest configuration.

Ensures ``src`` is on ``sys.path`` so ``import sovd_server`` works even when the
interpreter skips editable-install ``.pth`` files (e.g. some Python 3.13 +
virtualenv combinations). ``pyproject.toml`` also sets ``pythonpath = ["src"]``;
this is a redundant safeguard for IDE runners that omit that option.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
_src_str = str(_SRC)
if _src_str not in sys.path:
    sys.path.insert(0, _src_str)

# OpenAPI stub expects ``sovd_server.test`` + Connexion layout under ``generated/``; keep out of CI.
collect_ignore = [os.path.join(os.path.dirname(__file__), "test_default_controller.py")]
