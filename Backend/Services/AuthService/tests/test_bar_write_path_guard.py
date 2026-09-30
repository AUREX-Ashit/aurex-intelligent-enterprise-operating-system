"""
TD-171 remediation tranche (WP-23 Charter §21a), R-02 / OD-2: static
write-path guard for the enterprise BAR.

Both canonical BAR write paths, `BarIdentifierService.issue_identifier()`
and `BarRegistrationService.register()`, are governed: no production
module in AuthService may reach them, or the BAR write repositories, or
construct BAR rows directly, except the BAR modules themselves and the
designated governed registration operation.

This is the repository-side control only. The authoritative production
barrier is database-role separation (EP-02), which is an external
prerequisite and is NOT verified by this test. Tests, migrations
(`alembic/`) and the virtualenv are outside the scanned production tree.

Uses the AST approach of `Backend/Runtime/BusinessActivityEngine/tests/
test_package_boundary.py`: symbols and imports are inspected, never text
inside strings or comments, so docstrings may mention the write surface.
"""

from __future__ import annotations

import ast
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]

# Modules and symbols that constitute the BAR write surface.
WRITE_MODULES = frozenset(
    {
        "services.bar_registration_service",
        "services.bar_identifier_service",
        "repositories.bar_registration_repository",
        "repositories.bar_identifier_repository",
    }
)
WRITE_SYMBOLS = frozenset(
    {
        "BarRegistrationService",
        "BarIdentifierService",
        "BarRegistrationRepository",
        "BarIdentifierRepository",
        "issue_identifier",
    }
)
# Constructing these ORM rows directly is a write, reading them is not.
ROW_CONSTRUCTORS = frozenset({"BarRegistration", "BarIdentifierLedger"})

# The BAR modules themselves (Workstreams B/C, unchanged) and the
# designated governed registration operation. The governed operation is
# delivered by the next TD-171 slice; until then its path is reserved here
# so that it is the only production module permitted to add a caller.
BAR_OWN_MODULES = frozenset(
    {
        "services/bar_registration_service.py",
        "services/bar_identifier_service.py",
        "repositories/bar_registration_repository.py",
        "repositories/bar_identifier_repository.py",
        "models/bar_registration.py",
        "models/bar_identifier_ledger.py",
    }
)
GOVERNED_OPERATION_MODULES = frozenset({"services/bar_governed_registration.py"})
ALLOWED_MODULES = BAR_OWN_MODULES | GOVERNED_OPERATION_MODULES

EXCLUDED_TOP_LEVEL = frozenset({"venv", "tests", "alembic", "__pycache__"})


def production_sources() -> list[Path]:
    sources = []
    for path in SERVICE_ROOT.rglob("*.py"):
        relative = path.relative_to(SERVICE_ROOT)
        if relative.parts[0] in EXCLUDED_TOP_LEVEL or "__pycache__" in relative.parts:
            continue
        sources.append(path)
    return sorted(sources)


def violations_in(source: str) -> list[str]:
    """Every reference to the BAR write surface in one module's source."""
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in WRITE_MODULES:
                    found.append(f"imports {alias.name}")
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                qualified = f"{node.module}.{alias.name}"
                if node.module in WRITE_MODULES or qualified in WRITE_MODULES:
                    found.append(f"imports {qualified}")
                if alias.name in WRITE_SYMBOLS:
                    found.append(f"imports {alias.name}")
        elif isinstance(node, ast.Name) and node.id in WRITE_SYMBOLS:
            found.append(f"references {node.id}")
        elif isinstance(node, ast.Attribute) and node.attr in WRITE_SYMBOLS:
            found.append(f"references .{node.attr}")
        elif isinstance(node, ast.Call):
            callee = node.func
            name = callee.id if isinstance(callee, ast.Name) else callee.attr if isinstance(callee, ast.Attribute) else None
            if name in ROW_CONSTRUCTORS:
                found.append(f"constructs {name}(...)")
    return found


# ------------------------------------------------------------ repository scan


def test_scan_covers_the_production_tree():
    relative = {path.relative_to(SERVICE_ROOT).as_posix() for path in production_sources()}
    assert len(relative) > 50
    assert {"main.py", "dependencies.py", "services/bar_registration_service.py"} <= relative
    assert not any(name.startswith(("tests/", "alembic/", "venv/")) for name in relative)


def test_no_uncontrolled_production_module_reaches_the_bar_write_surface():
    offenders = {}
    for path in production_sources():
        relative = path.relative_to(SERVICE_ROOT).as_posix()
        if relative in ALLOWED_MODULES:
            continue
        found = violations_in(path.read_text(encoding="utf-8"))
        if found:
            offenders[relative] = found
    assert not offenders, (
        "BAR issuance/registration may only be reached through the governed "
        f"registration operation (TD-171, OD-2). Offending modules: {offenders}"
    )


def test_allowlist_names_only_real_bar_modules_or_the_reserved_governed_operation():
    for relative in BAR_OWN_MODULES:
        assert (SERVICE_ROOT / relative).is_file(), f"stale allowlist entry: {relative}"
    assert GOVERNED_OPERATION_MODULES.isdisjoint(BAR_OWN_MODULES)


# ------------------------------------------------------- negative controls


def test_detects_service_import_and_call():
    source = (
        "from services.bar_registration_service import BarRegistrationService\n"
        "async def handler(session):\n"
        "    return await BarRegistrationService(a, b).register(business_activity_reference='x')\n"
    )
    found = violations_in(source)
    assert "imports services.bar_registration_service.BarRegistrationService" in found
    assert "references BarRegistrationService" in found


def test_detects_identifier_issuance():
    found = violations_in("async def f(svc):\n    return await svc.issue_identifier()\n")
    assert found == ["references .issue_identifier"]


def test_detects_module_imports_and_repository_use():
    source = (
        "import services.bar_identifier_service\n"
        "from repositories import bar_registration_repository\n"
        "from repositories.bar_identifier_repository import BarIdentifierRepository\n"
    )
    found = violations_in(source)
    assert "imports services.bar_identifier_service" in found
    assert "imports repositories.bar_registration_repository" in found
    assert "imports BarIdentifierRepository" in found


def test_detects_direct_row_construction():
    source = (
        "from models.bar_registration import BarRegistration\n"
        "import models.bar_identifier_ledger as ledger\n"
        "def f(session):\n"
        "    session.add(BarRegistration(identifier='BA-000001'))\n"
        "    session.add(ledger.BarIdentifierLedger(identifier='BA-000002'))\n"
    )
    assert violations_in(source) == ["constructs BarRegistration(...)", "constructs BarIdentifierLedger(...)"]


# -------------------------------------------------- false-positive controls


def test_unrelated_register_methods_and_text_are_not_flagged():
    source = (
        '"""Mentions BarRegistrationService.register() and issue_identifier in prose."""\n'
        "# BarIdentifierService.issue_identifier() in a comment\n"
        "registry = ResolverRegistry().register(resolver)\n"
    )
    assert violations_in(source) == []


def test_reading_bar_rows_is_not_flagged():
    source = (
        "from sqlalchemy import select\n"
        "from models.bar_registration import BarRegistration\n"
        "query = select(BarRegistration).where(BarRegistration.identifier == 'BA-000001')\n"
    )
    assert violations_in(source) == []
