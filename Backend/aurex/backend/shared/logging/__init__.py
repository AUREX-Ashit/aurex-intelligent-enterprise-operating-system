"""
Import-path alias for Backend/Shared/Logging.

Backend/Shared/Logging's own modules already import each other via the
absolute path `aurex.backend.shared.logging.<module>` (see e.g.
audit_logger.py). No `aurex` package existed anywhere in the repository,
so every one of those imports failed with ModuleNotFoundError, and every
consuming service wrote its own local stand-in instead (see
Backend/Services/AuthService/observability.py's own docstring).

This package makes that existing, already-correct import path resolve to
the real files, by redirecting this package's own __path__ to
Backend/Shared/Logging rather than moving, renaming, or duplicating any
of that package's content. TD-105 in TECH-DEBT.md tracks this fix and
its own disclosed scope.
"""
from pathlib import Path

_real_dir = Path(__file__).resolve().parents[4] / "Shared" / "Logging"
__path__ = [str(_real_dir)]

# __path__ alone only redirects *submodule* lookups (e.g. this package's
# own audit_logger.py). This package's own __init__.py is still the file
# physically at this location, not Backend/Shared/Logging/__init__.py's —
# so its re-exports (LoggerFactory, AuditLogger, ...) are executed here,
# in this already-__path__-corrected namespace, rather than duplicated.
with open(_real_dir / "__init__.py", encoding="utf-8") as _f:
    exec(compile(_f.read(), str(_real_dir / "__init__.py"), "exec"), globals())
