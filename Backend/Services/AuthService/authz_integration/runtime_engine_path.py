"""
WP-13 (Authorization Runtime Integration). Makes
`Backend/Runtime/AuthorizationEngine`'s own `authorization`/`adapters`
packages importable from AuthService.

`AuthorizationEngine` has no `pyproject.toml`/`setup.py` (confirmed by
direct inspection) — it is not pip-installable, and its own README
Quick Start assumes it is run with its own directory on `sys.path`.
AuthService has no local path-based dependency mechanism today (its
`requirements.txt` lists only PyPI packages). Rather than repeat
`Backend/Shared/Logging`/`Events`'s own disclosed defect — importing
from a package path (`aurex.backend.shared...`) that does not
correspond to any real, installed package — this module inserts the
engine's own real, on-disk directory into `sys.path` directly, computed
relative to this file so it is independent of the working directory a
given process happens to be launched from.

This is a disclosed, pragmatic interim measure, not a final packaging
decision — formal packaging (a `pyproject.toml` for
`AuthorizationEngine`, installed editable into every consuming
service's own environment) remains a legitimate future improvement,
tracked as Technical Debt, not silently assumed resolved here.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ENGINE_ROOT = (
    Path(__file__).resolve().parents[3] / "Runtime" / "AuthorizationEngine"
)


def ensure_on_path() -> None:
    """Idempotent — safe to call from every module that needs the engine."""
    engine_root_str = str(_ENGINE_ROOT)
    if _ENGINE_ROOT.is_dir() and engine_root_str not in sys.path:
        sys.path.insert(0, engine_root_str)
