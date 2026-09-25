"""
WP-BAE-001 M1 -- package boundary tests (static, AST-based).

Proves: the runtime core has no HTTP/FastAPI or persistence dependency
(transport independence; no persistence in M1); it imports nothing from
any Business Capability service, BAR's own modules included, so it
cannot register a Business Activity or issue an identifier; it contains
no discovery mechanism (ADR-042 / RO-M1-03); its only Authorization
Engine dependencies are the existing public contract types.
"""

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1] / "business_activity_engine"
SOURCES = sorted(PACKAGE.glob("*.py"))


def _imported_modules() -> set[str]:
    modules: set[str] = set()
    for path in SOURCES:
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                modules.add(node.module)
    return modules


def _names_used() -> set[str]:
    names: set[str] = set()
    for path in SOURCES:
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.Attribute):
                names.add(node.attr)
    return names


def test_package_sources_exist() -> None:
    assert {path.name for path in SOURCES} >= {"engine.py", "identity.py", "pipeline.py", "ports.py", "results.py"}


def test_runtime_core_is_transport_and_persistence_independent() -> None:
    roots = {module.split(".")[0] for module in _imported_modules()}
    assert not roots & {"fastapi", "starlette", "httpx", "requests", "sqlalchemy", "alembic", "asyncpg"}


def test_no_capability_service_or_bar_module_is_imported() -> None:
    modules = _imported_modules()
    forbidden_fragments = ("bar_", "models", "repositories", "services", "routers", "dependencies", "authz_integration")
    assert not [m for m in modules if any(fragment in m.split(".")[0] for fragment in forbidden_fragments)]


def test_no_registration_or_identifier_issuance_is_referenced() -> None:
    names = _names_used()
    assert not names & {"register", "BarRegistrationService", "BarIdentifierService", "issue_identifier", "BarRegistration"}


def test_no_discovery_mechanism_is_used() -> None:
    roots = {module.split(".")[0] for module in _imported_modules()}
    assert not roots & {"importlib", "pkgutil", "os", "glob", "fnmatch", "sys"}
    assert not _names_used() & {"__import__", "import_module", "walk_packages", "iter_modules", "__subclasses__"}


def test_only_the_existing_authorization_contract_is_imported() -> None:
    engine_modules = {m for m in _imported_modules() if m.split(".")[0] in {"authorization", "adapters"}}
    assert engine_modules == {"authorization.models", "adapters.authorization_adapter"}
