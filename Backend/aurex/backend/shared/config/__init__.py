"""
Import-path alias for Backend/Shared/Config. See
Backend/aurex/backend/shared/logging/__init__.py for the full rationale
(identical defect, identical fix, applied per shared component).
"""
from pathlib import Path

_real_dir = Path(__file__).resolve().parents[4] / "Shared" / "Config"
__path__ = [str(_real_dir)]

with open(_real_dir / "__init__.py", encoding="utf-8") as _f:
    exec(compile(_f.read(), str(_real_dir / "__init__.py"), "exec"), globals())
