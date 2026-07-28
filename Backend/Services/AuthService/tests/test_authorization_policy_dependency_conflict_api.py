"""
WP-02 BA-09 — Detect and Resolve Authorization Policy Dependency
Conflict (ERB-C003-03 / EX-C003-09). API-layer tests for the ten new
POST /{resource}/{id}/dependency-check and /resolve-dependency
endpoints — one representative path per object type, plus the shared
404/403/400/422 behavior exercised once (on Role), since the underlying
service logic is identical across types.
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.domain import Domain
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
    claims = {
        "person_id": "11111111-1111-1111-1111-111111111111",
        "identity_id": "22222222-2222-2222-2222-222222222222",
        "organization_id": "33333333-3333-3333-3333-333333333333",
        "membership_id": "44444444-4444-4444-4444-444444444444",
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth_headers(role_code: str = "PLATFORM_ADMIN") -> dict[str, str]:
    return {"Authorization": f"Bearer {_access_token(role_code)}"}


# --- Role -----------------------------------------------------------------


def test_check_role_dependencies_clean(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA09_API_ROLE_1", "role_name": "V1"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(f"/roles/{role_id}/dependency-check", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["has_conflicts"] is False
    assert body["violations"] == []


def test_check_role_dependencies_rejects_unknown_role(client: TestClient) -> None:
    response = client.post(f"/roles/{uuid.uuid4()}/dependency-check", headers=_auth_headers())
    assert response.status_code == 404


def test_check_role_dependencies_rejects_non_platform_admin(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA09_API_ROLE_AUTH", "role_name": "V1"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(f"/roles/{role_id}/dependency-check", headers=_auth_headers(role_code="ESG_MANAGER"))
    assert response.status_code == 403


def test_check_role_dependencies_requires_authorization_header(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA09_API_ROLE_NOAUTH", "role_name": "V1"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(f"/roles/{role_id}/dependency-check")
    assert response.status_code == 400


@pytest.fixture
async def seeded_membership_on_new_role(db_session: AsyncSession) -> str:
    person = Person(first_name="BA09", last_name="APIDep", display_name="BA09 API Dep")
    organization = Organization(
        organization_code="BA09-API-ROLE-ORG", organization_name="BA-09 API Role Org", organization_type="CORPORATE",
    )
    role = Role(role_code="BA09_API_ROLE_DEP", role_name="BA-09 API Dependent Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    db_session.add(membership)
    await db_session.commit()

    return str(role.id)


def test_check_role_dependencies_finds_active_membership(client: TestClient, seeded_membership_on_new_role: str) -> None:
    response = client.post(f"/roles/{seeded_membership_on_new_role}/dependency-check", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["has_conflicts"] is True
    assert any(v["rule"] == "BR-C003-04" for v in body["violations"])
    assert len(body["active_dependents"]) == 1


def test_resolve_role_dependency_accepted_break(client: TestClient, seeded_membership_on_new_role: str) -> None:
    response = client.post(
        f"/roles/{seeded_membership_on_new_role}/resolve-dependency",
        headers=_auth_headers(),
        json={"resolution_type": "ACCEPTED_BREAK", "reason": "Membership reassigned via C-007."},
    )

    assert response.status_code == 200
    # Audit-trail-only today (TD-030) — the dependent itself is unchanged.
    assert response.json()["has_conflicts"] is True


def test_resolve_role_dependency_reassignment_requires_target(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA09_API_ROLE_REASSIGN", "role_name": "V1"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(
        f"/roles/{role_id}/resolve-dependency",
        headers=_auth_headers(),
        json={"resolution_type": "REASSIGNMENT_CONFIRMED", "reason": "Missing target"},
    )
    assert response.status_code == 422


# --- Domain Permission / Approval Authority / Delegation Policy / Runtime --


@pytest.fixture
async def seeded_organization(db_session: AsyncSession) -> str:
    organization = Organization(
        organization_code="BA09-API-ORG", organization_name="BA-09 API Org", organization_type="CORPORATE",
    )
    db_session.add(organization)
    await db_session.commit()
    return str(organization.id)


def test_check_approval_authority_dependencies_clean(client: TestClient, seeded_organization: str) -> None:
    establish_response = client.post(
        "/approval-authorities",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "authority_name": "V1",
            "approval_strategy": "ANY_ONE",
            "scope_type": "GLOBAL",
        },
    )
    authority_id = establish_response.json()["id"]

    response = client.post(f"/approval-authorities/{authority_id}/dependency-check", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["has_conflicts"] is False


def test_check_delegation_policy_dependencies_clean(client: TestClient, seeded_organization: str) -> None:
    establish_response = client.post(
        "/delegation-policies",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "policy_name": "V1",
            "delegation_type": "EMERGENCY",
            "scope_type": "ORGANIZATION",
        },
    )
    policy_id = establish_response.json()["id"]

    response = client.post(f"/delegation-policies/{policy_id}/dependency-check", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["has_conflicts"] is False


@pytest.fixture
async def seeded_membership_and_domain(db_session: AsyncSession) -> tuple[str, str]:
    person = Person(first_name="BA09", last_name="DPAPI", display_name="BA09 DP API")
    organization = Organization(
        organization_code="BA09-API-DP-ORG", organization_name="BA-09 API DP Org", organization_type="CORPORATE",
    )
    role = Role(role_code="BA09_API_DP_ROLE", role_name="BA-09 API DP Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    domain = Domain(domain_name="Finance")
    db_session.add_all([membership, domain])
    await db_session.commit()

    return str(membership.id), str(domain.id)


def test_check_domain_permission_dependencies_clean(client: TestClient, seeded_membership_and_domain) -> None:
    membership_id, domain_id = seeded_membership_and_domain
    establish_response = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )
    grant_id = establish_response.json()["id"]

    response = client.post(f"/domain-permissions/{grant_id}/dependency-check", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["has_conflicts"] is False


def test_check_runtime_assignment_policy_dependencies_clean(client: TestClient, seeded_organization: str) -> None:
    establish_response = client.post(
        "/runtime-assignment-policies",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "policy_name": "V1",
            "assignment_target_type": "BUSINESS_ROLE",
        },
    )
    policy_id = establish_response.json()["id"]

    response = client.post(f"/runtime-assignment-policies/{policy_id}/dependency-check", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["has_conflicts"] is False
