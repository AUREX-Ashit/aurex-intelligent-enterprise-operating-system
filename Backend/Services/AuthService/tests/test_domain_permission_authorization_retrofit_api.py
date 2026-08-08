"""
WP-13 (Authorization Runtime Integration) — API-level tests for the
per-endpoint retrofit of routers/domain_permission.py's own
establish_domain_permission (BA-02, TD-022), list_domain_permissions
(TD-090), and get_domain_permission (TD-090), each moved from the
interim PLATFORM_ADMIN-only gate to a real, database-backed
DomainPermission grant evaluated through the Authorization Runtime
Engine (dependencies.py::enforce_domain_permission).

Exercises the real HTTP round-trip end to end (client -> router ->
dependencies.py -> Authorization Runtime Engine -> repository),
complementing test_authorization_integration.py's own direct
dependency-function calls rather than duplicating them.

Satisfies CLAUDE.md §21.4's Mandatory Tenant-Isolation Test Checklist:
(a) two distinct, unrelated Organizations with no shared row
    (`two_orgs` fixture below);
(b) explicit confirmation a caller in one Organization cannot use a
    grant on their own Organization's Domain to act on or view another
    Organization's own Domain;
(c) an explicit probe of whether a foreign-object identifier not
    derived from the caller's own claims (an unrelated Organization's
    own domain_id, or a domain_permission_id naming a record governed
    by an unrelated Organization's own Domain) is accepted.

Domain Permission's own governing boundary is the Domain (URA-001-76's
fifth precedence tier), not Organization membership —
DomainPermissionService.deprecate() already documents this explicitly
("Domain Permission has no organization_id column of its own... not
reopened here"). These tests therefore probe the Domain boundary itself
(a grant on Domain A must never authorize acting on Domain B), not an
Organization-membership boundary this resource was never built to
have — inventing the latter here would be an undocumented new security
model, prohibited by CLAUDE.md §18.
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
    role = Role(role_code="DP_RETROFIT_TEST_ROLE", role_name="Domain Permission Retrofit Test Role")
    db_session.add(role)
    await db_session.flush()

    org_a = Organization(organization_code="DP-RETROFIT-ORG-A", organization_name="Retrofit Org A", organization_type="CORPORATE")
    person_a = Person(first_name="Alice", last_name="OrgA", display_name="Alice OrgA")
    db_session.add_all([org_a, person_a])
    await db_session.flush()
    membership_a = Membership(person_id=person_a.id, organization_id=org_a.id, role_id=role.id)
    domain_a = Domain(domain_name="Org A Domain", organization_id=org_a.id)
    db_session.add_all([membership_a, domain_a])
    await db_session.flush()

    org_b = Organization(organization_code="DP-RETROFIT-ORG-B", organization_name="Retrofit Org B", organization_type="CORPORATE")
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


# ---------------------------------------------------------------------------
# establish_domain_permission (BA-02, TD-022) — POST /domain-permissions
# ---------------------------------------------------------------------------

async def test_establish_domain_permission_succeeds_with_admin_grant_holder(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "ADMIN")
    headers = _headers_for(ctx, "a")

    response = client.post(
        "/domain-permissions",
        headers=headers,
        json={
            "membership_id": str(ctx["membership_a"].id),
            "domain_id": str(ctx["domain_a"].id),
            "permission_level": "EDIT",
        },
    )

    assert response.status_code == 201


async def test_establish_domain_permission_denies_insufficient_grant_level(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """A VIEW grant must not satisfy establish_domain_permission's own ADMIN requirement."""
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "VIEW")
    headers = _headers_for(ctx, "a")

    response = client.post(
        "/domain-permissions",
        headers=headers,
        json={
            "membership_id": str(ctx["membership_a"].id),
            "domain_id": str(ctx["domain_a"].id),
            "permission_level": "EDIT",
        },
    )

    assert response.status_code == 403


async def test_establish_domain_permission_denies_admin_grant_holder_acting_on_unrelated_orgs_domain(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """
    Tenant isolation (CLAUDE.md §21.4b/c): Membership A's own ADMIN grant
    on Domain A must not authorize establishing a permission on Domain B
    — an unrelated Organization's own Domain, a foreign-object identifier
    not derived from the caller's own claims.
    """
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "ADMIN")
    headers = _headers_for(ctx, "a")

    response = client.post(
        "/domain-permissions",
        headers=headers,
        json={
            "membership_id": str(ctx["membership_b"].id),
            "domain_id": str(ctx["domain_b"].id),
            "permission_level": "VIEW",
        },
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# list_domain_permissions (TD-090) — GET /domain-permissions
# ---------------------------------------------------------------------------

async def test_list_domain_permissions_succeeds_with_view_grant_on_filtered_domain(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "VIEW")
    headers = _headers_for(ctx, "a")

    response = client.get(f"/domain-permissions?domain_id={ctx['domain_a'].id}", headers=headers)

    assert response.status_code == 200


async def test_list_domain_permissions_denies_grant_holder_filtering_unrelated_orgs_domain(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """Tenant isolation (CLAUDE.md §21.4b/c): a VIEW grant on Domain A must not authorize listing Domain B's own permissions."""
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "VIEW")
    headers = _headers_for(ctx, "a")

    response = client.get(f"/domain-permissions?domain_id={ctx['domain_b'].id}", headers=headers)

    assert response.status_code == 403


async def test_list_domain_permissions_unscoped_still_requires_platform_admin_despite_domain_grant(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """An unscoped (no domain_id) listing remains PLATFORM_ADMIN-only — a single Domain grant must never widen it (router's own documented rationale)."""
    ctx = two_orgs
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "ADMIN")
    headers = _headers_for(ctx, "a")

    response = client.get("/domain-permissions", headers=headers)

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# get_domain_permission (TD-090) — GET /domain-permissions/{id}
# ---------------------------------------------------------------------------

async def test_get_domain_permission_succeeds_with_view_grant_on_records_domain(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    record = await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "EDIT")
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "VIEW")
    headers = _headers_for(ctx, "a")

    response = client.get(f"/domain-permissions/{record.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == str(record.id)


async def test_get_domain_permission_denies_caller_with_no_grant_on_unrelated_orgs_record(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """
    Tenant isolation (CLAUDE.md §21.4b/c): a Domain Permission record
    governed by Domain A (Organization A's own Domain) must not be
    retrievable by Membership B (Organization B), who holds no grant on
    Domain A — an explicit probe of a foreign-object identifier
    (domain_permission_id) not derived from Membership B's own claims.
    """
    ctx = two_orgs
    record = await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "EDIT")
    headers = _headers_for(ctx, "b")

    response = client.get(f"/domain-permissions/{record.id}", headers=headers)

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# version_domain_permission (BA-07, TD-137) — POST /domain-permissions/{id}/versions
# ---------------------------------------------------------------------------

async def test_version_domain_permission_succeeds_with_admin_grant_on_records_domain(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    ctx = two_orgs
    record = await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "EDIT")
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "ADMIN")
    headers = _headers_for(ctx, "a")

    response = client.post(f"/domain-permissions/{record.id}/versions", headers=headers, json={})

    assert response.status_code == 201
    body = response.json()
    assert body["supersedes_id"] == str(record.id)


async def test_version_domain_permission_denies_insufficient_grant_level(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """A VIEW grant must not satisfy version_domain_permission's own ADMIN requirement."""
    ctx = two_orgs
    record = await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "EDIT")
    await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "VIEW")
    headers = _headers_for(ctx, "a")

    response = client.post(f"/domain-permissions/{record.id}/versions", headers=headers, json={})

    assert response.status_code == 403


async def test_version_domain_permission_denies_caller_with_no_grant_on_unrelated_orgs_record(
    client: TestClient, db_session: AsyncSession, two_orgs: dict
) -> None:
    """
    Tenant isolation (CLAUDE.md §21.4b/c): a Domain Permission record
    governed by Domain A must not be versionable by Membership B
    (Organization B), who holds no grant on Domain A — an explicit
    probe of a foreign-object identifier (domain_permission_id) not
    derived from Membership B's own claims. Membership B's own ADMIN
    grant on its own Domain B must not leak into authorizing an
    operation on Domain A's own record.
    """
    ctx = two_orgs
    record = await _grant(db_session, ctx["membership_a"], ctx["domain_a"], "EDIT")
    await _grant(db_session, ctx["membership_b"], ctx["domain_b"], "ADMIN")
    headers = _headers_for(ctx, "b")

    response = client.post(f"/domain-permissions/{record.id}/versions", headers=headers, json={})

    assert response.status_code == 403
