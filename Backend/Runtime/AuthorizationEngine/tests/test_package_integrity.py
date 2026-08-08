"""
Package hardening / integrity validation for WP-RTA-001 Milestone M6.

Verifies runtime isolation (no capability-specific or web-framework
coupling anywhere in `authorization`/`adapters`), that every declared
public export actually resolves, and that no debug artifacts (bare
`print`, TODO/FIXME/XXX markers) were left behind. Complements
`test_adapter.py`'s own AST-based dependency-direction check (M4,
fixed M5) rather than duplicating it.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import pathlib
import re

import adapters
import authorization

_FORBIDDEN_IMPORT_PREFIXES = ("fastapi", "sqlalchemy", "starlette", "Backend", "backend")


def _all_package_source_files() -> list[pathlib.Path]:
    authorization_dir = pathlib.Path(inspect.getfile(authorization)).parent
    adapters_dir = pathlib.Path(inspect.getfile(adapters)).parent
    return sorted(authorization_dir.glob("*.py")) + sorted(adapters_dir.glob("*.py"))


def _imported_top_level_names(source_file: pathlib.Path) -> list[str]:
    tree = ast.parse(source_file.read_text(encoding="utf-8"), filename=str(source_file))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


# ---------------------------------------------------------------------------
# Runtime isolation
# ---------------------------------------------------------------------------


def test_no_file_imports_a_web_framework_or_orm() -> None:
    for source_file in _all_package_source_files():
        for name in _imported_top_level_names(source_file):
            top = name.split(".")[0]
            assert top not in ("fastapi", "sqlalchemy", "starlette"), (
                f"{source_file}: imports {name!r} -- this runtime must remain framework-independent."
            )


def test_no_file_imports_a_capability_specific_service() -> None:
    for source_file in _all_package_source_files():
        for name in _imported_top_level_names(source_file):
            assert not name.startswith(("Backend.Services", "Backend.Shared")), (
                f"{source_file}: imports {name!r} -- this Runtime Work Package owns no Business Capability coupling (IRA-RTA-001 S9)."
            )


def test_authorization_package_never_imports_adapters() -> None:
    """Re-affirms M4/M5's own finding with a fresh, independent AST walk (not a call into test_adapter.py)."""
    authorization_dir = pathlib.Path(inspect.getfile(authorization)).parent
    for source_file in sorted(authorization_dir.glob("*.py")):
        for name in _imported_top_level_names(source_file):
            assert not (name == "adapters" or name.startswith("adapters.")), (
                f"{source_file.name} imports from 'adapters' -- the runtime must never depend on the adapter layer."
            )


# ---------------------------------------------------------------------------
# Export normalization
# ---------------------------------------------------------------------------


def test_every_declared_export_actually_resolves() -> None:
    for module in (authorization, adapters):
        for name in module.__all__:
            assert hasattr(module, name), f"{module.__name__}.__all__ declares {name!r}, which does not exist"


def test_no_export_is_declared_twice() -> None:
    for module in (authorization, adapters):
        assert len(module.__all__) == len(set(module.__all__)), f"{module.__name__}.__all__ has a duplicate entry"


def test_reimporting_the_package_is_idempotent() -> None:
    """A basic package-hygiene check: re-importing must not raise or produce a different module object."""
    first = importlib.import_module("authorization")
    second = importlib.import_module("authorization")
    assert first is second


# ---------------------------------------------------------------------------
# No debug artifacts left behind
# ---------------------------------------------------------------------------


_DEBUG_MARKER_PATTERN = re.compile(r"\b(TODO|FIXME|XXX)\b")


def test_no_todo_fixme_or_xxx_markers_left_in_production_code() -> None:
    for source_file in _all_package_source_files():
        text = source_file.read_text(encoding="utf-8")
        match = _DEBUG_MARKER_PATTERN.search(text)
        assert match is None, f"{source_file}: contains a {match.group(0) if match else ''} marker"


def test_no_bare_print_statements_in_production_code() -> None:
    for source_file in _all_package_source_files():
        tree = ast.parse(source_file.read_text(encoding="utf-8"), filename=str(source_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
                raise AssertionError(f"{source_file}: contains a bare print() call -- not appropriate for production runtime code")
