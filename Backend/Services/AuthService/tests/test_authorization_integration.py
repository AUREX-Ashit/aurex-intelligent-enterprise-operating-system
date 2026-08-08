"""
WP-13 (Authorization Runtime Integration). Verifies the first real,
database-backed consumer of `Backend/Runtime/AuthorizationEngine`
anywhere in this repository — `dependencies.py::require_domain_permission`,
backed by `AuthServiceDomainPermissionResolver` and
`DomainPermissionRepository.get_active_grant_at_or_above()`.

Calls the dependency function directly (mirroring this test suite's own
`_service(session)` pattern elsewhere) rather than through a full HTTP
round-trip — this exercises the real repository → resolver → registry →
pipeline → adapter → decision chain exactly as a real endpoint would,
without needing a throwaway router just to host this test.
"""

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_domain_permission
from models.domain import Domain
from models.domain_permission import DomainPermission, DomainPermissionLevel
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role
from repositories.domain_permission_repository import DomainPermissionRepository


@pytest.fixture
async def seeded_membership_and_domain(db_session: AsyncSession) -> tuple[Membership, Domain]:
    person = Person(first_name="Grant", last_name="Holder", display_name="Grant Holder")
    organization = Organization(
        organization_code="AUTHZ-TEST-ORG",
        organization_name="Authorization Integration Test Org",
        organization_type="CORPORATE",
    )
    role = Role(role_code="AUTHZ_TEST_ROLE", role_name="Authorization Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    domain = Domain(domain_name="Finance")
    db_session.add_all([membership, domain])
    await db_session.flush()

    return membership, domain


def _claims(membership: Membership, organization_id: uuid.UUID, role_code: str = "MEMBER") -> dict:
    return {
        "person_id": str(membership.person_id),
        "organization_id": str(organization_id),
        "membership_id": str(membership.id),
        "role_code": role_code,
    }


async def _grant(
    db_session: AsyncSession,
    membership: Membership,
    domain: Domain,
    level: str,
    status: str = "ACTIVE",
    effective_to: datetime | None = None,
) -> DomainPermission:
    grant = DomainPermission(
        membership_id=membership.id,
        domain_id=domain.id,
        permission_level=level,
        status=status,
        effective_to=effective_to,
    )
    db_session.add(grant)
    await db_session.flush()
    return grant


# ---------------------------------------------------------------------------
# Repository — get_active_grant_at_or_above (new, WP-13)
# ---------------------------------------------------------------------------

async def test_repo_finds_exact_level_match(db_session, seeded_membership_and_domain):
    membership, domain = seeded_membership_and_domain
    await _grant(db_session, membership, domain, "EDIT")
    repo = DomainPermissionRepository(db_session)

    found = await repo.get_active_grant_at_or_above(membership.id, domain.id, "EDIT")
    assert found is not None


async def test_repo_finds_higher_level_grant_satisfying_lower_requirement(db_session, seeded_membership_and_domain):
    """A caller holding ADMIN should satisfy a request for the lower-ranked VIEW."""
    membership, domain = seeded_membership_and_domain
    await _grant(db_session, membership, domain, "ADMIN")
    repo = DomainPermissionRepository(db_session)

    found = await repo.get_active_grant_at_or_above(membership.id, domain.id, "VIEW")
    assert found is not None


async def test_repo_rejects_lower_level_grant_against_higher_requirement(db_session, seeded_membership_and_domain):
    """A caller holding only VIEW must not satisfy a request for ADMIN."""
    membership, domain = seeded_membership_and_domain
    await _grant(db_session, membership, domain, "VIEW")
    repo = DomainPermissionRepository(db_session)

    found = await repo.get_active_grant_at_or_above(membership.id, domain.id, "ADMIN")
    assert found is None


async def test_repo_ignores_non_active_status(db_session, seeded_membership_and_domain):
    membership, domain = seeded_membership_and_domain
    await _grant(db_session, membership, domain, "ADMIN", status="RETIRED")
    repo = DomainPermissionRepository(db_session)

    found = await repo.get_active_grant_at_or_above(membership.id, domain.id, "VIEW")
    assert found is None


async def test_repo_ignores_expired_grant(db_session, seeded_membership_and_domain):
    membership, domain = seeded_membership_and_domain
    await _grant(
        db_session, membership, domain, "ADMIN",
        effective_to=datetime.now(timezone.utc) - timedelta(days=1),
    )
    repo = DomainPermissionRepository(db_session)

    found = await repo.get_active_grant_at_or_above(membership.id, domain.id, "VIEW")
    assert found is None


async def test_repo_never_returns_another_memberships_grant(db_session, seeded_membership_and_domain):
    """Tenant-isolation-adjacent: a grant belonging to an unrelated Membership must never satisfy this Membership's own check."""
    membership, domain = seeded_membership_and_domain
    other_person = Person(first_name="Other", last_name="Person", display_name="Other Person")
    db_session.add(other_person)
    await db_session.flush()
    other_membership = Membership(
        person_id=other_person.id, organization_id=membership.organization_id, role_id=membership.role_id
    )
    db_session.add(other_membership)
    await db_session.flush()
    await _grant(db_session, other_membership, domain, "ADMIN")

    repo = DomainPermissionRepository(db_session)
    found = await repo.get_active_grant_at_or_above(membership.id, domain.id, "VIEW")
    assert found is None


# ---------------------------------------------------------------------------
# require_domain_permission — the real dependency, full chain
# ---------------------------------------------------------------------------

async def test_dependency_allows_caller_with_sufficient_grant(db_session, seeded_membership_and_domain):
    membership, domain = seeded_membership_and_domain
    await _grant(db_session, membership, domain, "EDIT")
    dependency = require_domain_permission(domain.id, DomainPermissionLevel.VIEW)

    result = await dependency(claims=_claims(membership, membership.organization_id), session=db_session)
    assert result["membership_id"] == str(membership.id)


async def test_dependency_denies_caller_with_insufficient_grant(db_session, seeded_membership_and_domain):
    membership, domain = seeded_membership_and_domain
    await _grant(db_session, membership, domain, "VIEW")
    dependency = require_domain_permission(domain.id, DomainPermissionLevel.ADMIN)

    with pytest.raises(HTTPException) as exc:
        await dependency(claims=_claims(membership, membership.organization_id), session=db_session)
    assert exc.value.status_code == 403


async def test_dependency_denies_caller_with_no_grant_at_all(db_session, seeded_membership_and_domain):
    membership, domain = seeded_membership_and_domain
    dependency = require_domain_permission(domain.id, DomainPermissionLevel.VIEW)

    with pytest.raises(HTTPException) as exc:
        await dependency(claims=_claims(membership, membership.organization_id), session=db_session)
    assert exc.value.status_code == 403


async def test_dependency_platform_admin_bypasses_regardless_of_grant(db_session, seeded_membership_and_domain):
    """PLATFORM_ADMIN must remain a universal bypass — this replacement is additive, never a narrowing of existing access."""
    membership, domain = seeded_membership_and_domain
    dependency = require_domain_permission(domain.id, DomainPermissionLevel.ADMIN)

    result = await dependency(
        claims=_claims(membership, membership.organization_id, role_code="PLATFORM_ADMIN"),
        session=db_session,
    )
    assert result["role_code"] == "PLATFORM_ADMIN"


async def test_dependency_denies_caller_with_no_membership_id(db_session, seeded_membership_and_domain):
    """A caller whose own claims carry no membership_id at all cannot hold a Domain Permission grant — explicit probe, not an unhandled edge case."""
    membership, domain = seeded_membership_and_domain
    await _grant(db_session, membership, domain, "ADMIN")
    dependency = require_domain_permission(domain.id, DomainPermissionLevel.VIEW)
    claims = _claims(membership, membership.organization_id)
    claims["membership_id"] = None

    with pytest.raises(HTTPException) as exc:
        await dependency(claims=claims, session=db_session)
    assert exc.value.status_code == 403
