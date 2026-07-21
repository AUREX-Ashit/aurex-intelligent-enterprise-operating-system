import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.identity import Identity
from models.membership import Membership
from models.organization import Organization
from models.permission import Permission
from models.role import Role
from models.role_permission import RolePermission
from scripts import bootstrap_data as seed
from services.bootstrap_service import BootstrapService


@pytest.fixture
def production_environment():
    """IC-001 M1: temporarily flips settings.environment to production and restores it after."""
    original = settings.environment
    settings.environment = "production"
    yield
    settings.environment = original


async def _counts(session: AsyncSession) -> dict[str, int]:
    return {
        "roles": len((await session.execute(select(Role))).scalars().all()),
        "permissions": len((await session.execute(select(Permission))).scalars().all()),
        "role_permissions": len((await session.execute(select(RolePermission))).scalars().all()),
        "organizations": len((await session.execute(select(Organization))).scalars().all()),
        "identities": len((await session.execute(select(Identity))).scalars().all()),
        "memberships": len((await session.execute(select(Membership))).scalars().all()),
    }


async def test_first_run_creates_full_seed_graph(db_session: AsyncSession) -> None:
    """
    Business Activity Completion Criteria: 'Business state transitioned
    correctly'. Verifies the exact row counts documented in
    scripts/03_seed_r001_data.sql (6 roles, 12 permissions, 42
    role_permissions) plus the 1 demo organization and 2 identities/
    memberships (demo admin + platform admin) from scripts/05 and 07.
    """
    result = await BootstrapService(db_session).run()

    assert result.roles_created == 6
    assert result.permissions_created == 12
    assert result.role_permissions_created == 42
    assert result.organizations_created == 1
    assert result.persons_created == 2
    assert result.identities_created == 2
    assert result.memberships_created == 2
    assert result.is_first_run is True

    counts = await _counts(db_session)
    assert counts["roles"] == 6
    assert counts["permissions"] == 12
    assert counts["role_permissions"] == 42
    assert counts["organizations"] == 1
    assert counts["identities"] == 2
    assert counts["memberships"] == 2


async def test_second_run_is_a_true_no_op(db_session: AsyncSession) -> None:
    """
    IMP-CICD-002 / Rollback Framework requirement: re-running must never
    duplicate rows. This is the idempotency contract test — it would fail
    if BootstrapService inserted a second time rather than detecting the
    existing row (a CRUD-only implementation could pass a naive 'no
    exception raised' check while silently duplicating data; this test
    specifically checks row counts, not just successful execution).
    """
    service = BootstrapService(db_session)
    first = await service.run()
    second = await service.run()

    assert first.total_created > 0
    assert second.total_created == 0
    assert second.is_first_run is False

    counts = await _counts(db_session)
    assert counts["roles"] == 6
    assert counts["permissions"] == 12
    assert counts["role_permissions"] == 42
    assert counts["organizations"] == 1
    assert counts["identities"] == 2
    assert counts["memberships"] == 2


async def test_platform_admin_identity_matches_documented_credentials(db_session: AsyncSession) -> None:
    """
    Business behaviour, not CRUD: proves the seeded Platform Administrator
    can actually be looked up by the exact email the roadmap's Demo
    Scenario names, with the PLATFORM_ADMIN role correctly linked —
    not merely that *some* rows were inserted.
    """
    await BootstrapService(db_session).run()

    result = await db_session.execute(
        select(Identity).where(Identity.email == "platform.admin@corpstage.com")
    )
    identity = result.scalar_one()
    assert identity.person_id == seed.PLATFORM_ADMIN_PERSON.id
    assert identity.is_verified is True

    membership_result = await db_session.execute(
        select(Membership).where(Membership.person_id == identity.person_id)
    )
    membership = membership_result.scalar_one()
    assert membership.role_id == seed.PLATFORM_ADMIN_MEMBERSHIP.role_id
    assert membership.membership_status == "ACTIVE"


async def test_is_bootstrapped_reflects_actual_state(db_session: AsyncSession) -> None:
    """Readiness-probe support: false before bootstrap, true after."""
    service = BootstrapService(db_session)
    assert await service.is_bootstrapped() is False

    await service.run()
    assert await service.is_bootstrapped() is True


async def test_production_environment_refuses_builtin_demo_hash(
    db_session: AsyncSession, production_environment, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    IC-001 M1: the built-in demo/platform-admin bcrypt hash is public (visible
    in scripts/bootstrap_data.py, documented in RUNBOOK_BOOTSTRAP.md). Bootstrap
    must refuse to seed it unattended in production rather than silently
    creating a publicly-known credential.
    """
    monkeypatch.delenv("BOOTSTRAP_ADMIN_PASSWORD_HASH", raising=False)
    monkeypatch.delenv("BOOTSTRAP_PLATFORM_ADMIN_PASSWORD_HASH", raising=False)

    with pytest.raises(RuntimeError, match="production environment"):
        await BootstrapService(db_session).run()

    # Failed run must not leave partial state (rollback is exercised, not just raised).
    counts = await _counts(db_session)
    assert counts["identities"] == 0
    assert counts["memberships"] == 0


async def test_production_environment_accepts_override_hash(
    db_session: AsyncSession, production_environment, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A production operator supplying real, rotated password hashes may still bootstrap."""
    monkeypatch.setenv("BOOTSTRAP_ADMIN_PASSWORD_HASH", "$2b$12$overriddenAdminHashXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    monkeypatch.setenv("BOOTSTRAP_PLATFORM_ADMIN_PASSWORD_HASH", "$2b$12$overriddenPlatformHashXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    result = await BootstrapService(db_session).run()
    assert result.identities_created == 2

    seeded = (
        await db_session.execute(select(Identity).where(Identity.email == seed.PLATFORM_ADMIN_IDENTITY.email))
    ).scalar_one()
    assert seeded.password_hash == "$2b$12$overriddenPlatformHashXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    assert seeded.password_hash != seed.PLATFORM_ADMIN_IDENTITY.password_hash
