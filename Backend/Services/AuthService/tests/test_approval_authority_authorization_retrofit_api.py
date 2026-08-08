"""
WP-13 (Authorization Runtime Integration) — API-level tests for the
DOMAIN-scoped retrofit of routers/approval_authority.py's own
establish_approval_authority (BA-03, TD-023), moved for scope_type =
DOMAIN only from the interim PLATFORM_ADMIN-only gate to a real,
database-backed DomainPermission grant evaluated through the
Authorization Runtime Engine (dependencies.py::enforce_domain_permission)
— the same mechanism already proven for establish_domain_permission
(TD-022) and domain_permission.py's own full lifecycle (TD-137/138/139).

GLOBAL, COMPANY, and OBJECT scope remain PLATFORM_ADMIN-only, unchanged
— Corporate Admin authority (URA-001-32) is not modeled anywhere in
this repository, and no authority is named anywhere for OBJECT scope;
retrofitting either would require inventing new architecture, which
this Work Package does not do.

Satisfies CLAUDE.md §21.4's Mandatory Tenant-Isolation Test Checklist:
two distinct, unrelated Organizations with no shared row; explicit
cross-Organization denial; an explicit probe of a foreign-object
identifier (a domain_id belonging to an unrelated Organization) not
derived from the caller's own claims.
"""

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.domain import Domain
from models.domain_permission import DomainPermission
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role


def _access_token(person_id, organization_id, membership_id, role_code: str = "MEMBER") -> str:
    claims = {
        "person_id": str(person_id),
        "identity_id": str(uuid.uuid4()),
        "organization_id": str(organization_id),
        "membership_id": str(membership_id),
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth_headers(person_id, organization_id, membership_id, role_code: str = "MEMBER") -> dict[str, str]:
    return {"Authorization": f"Bearer {_access_token(person_id, organization_id, membership_id, role_code)}"}


@pytest.fixture
async def two_orgs(db_session: AsyncSession) -> dict:
    """Two distinct, unrelated Organizations, each with its own Person/Membership/Domain — no shared row, per CLAUDE.md §21.4(a)."""
    role = Role(role_code="AA_RETROFIT_TEST_ROLE", role_name="Approval Authority Retrofit Test Role")
    db_session.add(role)
    await db_session.flush()

    org_a = Organization(organization_code="AA-RETROFIT-ORG-A", organization_name="Retrofit Org A", organization_type="CORPORATE")
    person_a = Person(first_name="Alice", last_name="OrgA", display_name="Alice OrgA")
    db_session.add_all([org_a, person_a])
    await db_session.flush()
    membership_a = Membership(person_id=person_a.id, organization_id=org_a.id, role_id=role.id)
    domain_a = Domain(domain_name="Org A Domain", organization_id=org_a.id)
    db_session.add_all([membership_a, domain_a])
    await db_session.flush()

    org_b = Organization(organization_code="AA-RETROFIT-ORG-B", organization_name="Retrofit Org B", organization_type="CORPORATE")
    person_b = Person(first_name="Bob", last_name="OrgB", display_name="Bob OrgB")
    db_session.add_all([org_b, person_b])
    await db_session.flush()
    membership_b = Membership(person_id=person_b.id, organization_id=org_b.id, role_id=role.id)
    domain_b = Domain(domain_name="Org B Domain", organization_id=org_b.id)
    db_session.add_all([membership_b, domain_b])
    await db_session.commit()

    return {
        "org_a": org_a, "person_a": person_a, "membership_a": membership_a, "domain_a": domain_a,
        "org_b": org_b, "person_b": person_b, "membership_b": membership_b, "domain_b": domain_b,
    }


async def _grant(db_session: AsyncSession, membership: Membership, domain: Domain, level: str) -> DomainPermission:
    grant = DomainPermission(membership_id=membership.id, domain_id=domain.id, permission_level=level)
    db_session.add(grant)
    await db_session.commit()
    return grant


def _headers_for(ctx: dict, org_key: str, role_code: str = "MEMBER") -> dict[str, str]:
    person = ctx[f"person_{org_key}"]
    org = ctx[f"org_{org_key}"]
    membership = ctx[f"membership_{org_key}"]
    return _auth_headers(person.id, org.id, membership.id, role_code)


def _domain_scope_payload(organization_id, domain_id) -> dict:
    return {
        "organization_id": str(organization_id),
        "authority_name": "Domain Finance Approval",
        "approval_strategy": "ANY_ONE",
        "scope_type": "DOMAIN",
        "domain_id": str(domain_id),
    }


# ---------------------------------------------------------------------------
# scope_type = DOMAIN — retrofitted to the Authorization Runtime Engine
# ---------------------------------------------------------------------------

async def test_establish_approval_authority_domain_scope_succeeds_with_admin_grant(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "ADMIN")
    headers = _headers_for(ctx, "a")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json=_domain_scope_payload(ctx["org_a"].id, ctx["domain_a"].id),
    )

    assert response.status_code == 201
    assert response.json()["scope_type"] == "DOMAIN"


async def test_establish_approval_authority_domain_scope_denies_insufficient_grant(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """A VIEW grant must not satisfy the DOMAIN-scope ADMIN requirement."""
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "VIEW")
    headers = _headers_for(ctx, "a")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json=_domain_scope_payload(ctx["org_a"].id, ctx["domain_a"].id),
    )

    assert response.status_code == 403


async def test_establish_approval_authority_domain_scope_denies_no_grant(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    headers = _headers_for(ctx, "a")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json=_domain_scope_payload(ctx["org_a"].id, ctx["domain_a"].id),
    )

    assert response.status_code == 403


async def test_establish_approval_authority_domain_scope_denies_grant_from_unrelated_organization(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """
    Tenant isolation (CLAUDE.md §21.4b/c): Membership B's own ADMIN grant
    on Domain B (Organization B's own Domain) must not authorize
    establishing a DOMAIN-scoped Approval Authority against Domain A —
    an unrelated Organization's own Domain, a foreign-object identifier
    not derived from Membership B's own claims.
    """
    ctx = two_orgs
    await _grant(db_session, ctx["membership_b"], ctx["domain_b"], "ADMIN")
    headers = _headers_for(ctx, "b")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json=_domain_scope_payload(ctx["org_a"].id, ctx["domain_a"].id),
    )

    assert response.status_code == 403


async def test_establish_approval_authority_domain_scope_succeeds_for_platform_admin(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """PLATFORM_ADMIN must remain a universal bypass for DOMAIN scope, regardless of any grant."""
    ctx = two_orgs
    headers = _headers_for(ctx, "a", role_code="PLATFORM_ADMIN")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json=_domain_scope_payload(ctx["org_a"].id, ctx["domain_a"].id),
    )

    assert response.status_code == 201


# ---------------------------------------------------------------------------
# scope_type = GLOBAL / COMPANY / OBJECT — existing PLATFORM_ADMIN-only
# behavior preserved; a DOMAIN-scoped ADMIN grant must not leak into them.
# ---------------------------------------------------------------------------

async def test_establish_approval_authority_global_scope_denies_domain_admin_grant_holder(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """A caller's own DOMAIN-scoped ADMIN grant must not satisfy GLOBAL scope's own unchanged PLATFORM_ADMIN-only gate."""
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "ADMIN")
    headers = _headers_for(ctx, "a")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json={
            "organization_id": str(ctx["org_a"].id),
            "authority_name": "Global Framework Approval",
            "approval_strategy": "ANY_ONE",
            "scope_type": "GLOBAL",
        },
    )

    assert response.status_code == 403


async def test_establish_approval_authority_global_scope_succeeds_for_platform_admin(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    headers = _headers_for(ctx, "a", role_code="PLATFORM_ADMIN")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json={
            "organization_id": str(ctx["org_a"].id),
            "authority_name": "Global Framework Approval",
            "approval_strategy": "ANY_ONE",
            "scope_type": "GLOBAL",
        },
    )

    assert response.status_code == 201


async def test_establish_approval_authority_company_scope_denies_domain_admin_grant_holder(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "ADMIN")
    headers = _headers_for(ctx, "a")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json={
            "organization_id": str(ctx["org_a"].id),
            "authority_name": "Company Framework Approval",
            "approval_strategy": "ANY_ONE",
            "scope_type": "COMPANY",
        },
    )

    assert response.status_code == 403


async def test_establish_approval_authority_object_scope_denies_domain_admin_grant_holder(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "ADMIN")
    headers = _headers_for(ctx, "a")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json={
            "organization_id": str(ctx["org_a"].id),
            "authority_name": "Revenue CDE Approval",
            "approval_strategy": "ALL",
            "scope_type": "OBJECT",
            "object_type": "revenue_cde",
            "object_id": str(uuid.uuid4()),
        },
    )

    assert response.status_code == 403


async def test_establish_approval_authority_object_scope_succeeds_for_platform_admin(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    headers = _headers_for(ctx, "a", role_code="PLATFORM_ADMIN")

    response = client.post(
        "/approval-authorities",
        headers=headers,
        json={
            "organization_id": str(ctx["org_a"].id),
            "authority_name": "Revenue CDE Approval",
            "approval_strategy": "ALL",
            "scope_type": "OBJECT",
            "object_type": "revenue_cde",
            "object_id": str(uuid.uuid4()),
        },
    )

    assert response.status_code == 201
