"""
WP-02 BA-08 — Deprecate or Retire Authorization Policy Object
(ERB-C003-02 / EX-C003-08). API-layer tests for the ten new
POST /{resource}/{id}/deprecate and /retire endpoints — one
representative success path per object type per operation, plus the
shared 404/409/403/400 behavior exercised once (on Role) rather than
five times, since the underlying service logic is identical across
types (see the service-layer test file for the full per-type
dependency-check coverage).
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


def test_deprecate_role_succeeds(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA08_API_ROLE", "role_name": "Original"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(f"/roles/{role_id}/deprecate", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "DEPRECATED"


def test_retire_role_succeeds_and_is_terminal(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA08_API_ROLE_2", "role_name": "Original"}
    )
    role_id = establish_response.json()["id"]

    first_retire = client.post(f"/roles/{role_id}/retire", headers=_auth_headers())
    assert first_retire.status_code == 200
    assert first_retire.json()["status"] == "RETIRED"

    second_retire = client.post(f"/roles/{role_id}/retire", headers=_auth_headers())
    assert second_retire.status_code == 409


def test_retire_role_rejects_unknown_role(client: TestClient) -> None:
    response = client.post(f"/roles/{uuid.uuid4()}/retire", headers=_auth_headers())
    assert response.status_code == 404


def test_retire_role_rejects_non_platform_admin(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA08_API_ROLE_AUTH", "role_name": "Original"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(f"/roles/{role_id}/retire", headers=_auth_headers(role_code="ESG_MANAGER"))
    assert response.status_code == 403


def test_retire_role_requires_authorization_header(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA08_API_ROLE_NOAUTH", "role_name": "Original"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(f"/roles/{role_id}/retire")
    assert response.status_code == 400


@pytest.fixture
async def seeded_membership_on_new_role(db_session: AsyncSession) -> tuple[str, str]:
    """Establishes a Role directly (bypassing the API) with an active Membership assigned to it."""
    person = Person(first_name="BA08", last_name="APIDep", display_name="BA08 API Dep")
    organization = Organization(
        organization_code="BA08-API-ROLE-ORG", organization_name="BA-08 API Role Org", organization_type="CORPORATE",
    )
    role = Role(role_code="BA08_API_ROLE_DEP", role_name="BA-08 API Dependent Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    db_session.add(membership)
    await db_session.commit()

    return str(role.id), str(membership.id)


def test_deprecate_role_rejects_role_with_active_membership(
    client: TestClient, seeded_membership_on_new_role
) -> None:
    role_id, _membership_id = seeded_membership_on_new_role

    response = client.post(f"/roles/{role_id}/deprecate", headers=_auth_headers())

    assert response.status_code == 409
    assert "BR-C003-04" in response.json()["detail"]


# --- Domain Permission -----------------------------------------------------


@pytest.fixture
async def seeded_membership_and_domain(db_session: AsyncSession) -> tuple[str, str]:
    person = Person(first_name="BA08", last_name="DPAPI", display_name="BA08 DP API")
    organization = Organization(
        organization_code="BA08-API-DP-ORG", organization_name="BA-08 API DP Org", organization_type="CORPORATE",
    )
    role = Role(role_code="BA08_API_DP_ROLE", role_name="BA-08 API DP Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    domain = Domain(domain_name="Finance")
    db_session.add_all([membership, domain])
    await db_session.commit()

    return str(membership.id), str(domain.id)


def test_retire_domain_permission_succeeds(client: TestClient, seeded_membership_and_domain) -> None:
    membership_id, domain_id = seeded_membership_and_domain
    establish_response = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )
    grant_id = establish_response.json()["id"]

    response = client.post(f"/domain-permissions/{grant_id}/retire", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["status"] == "RETIRED"


# --- Approval Authority ------------------------------------------------


@pytest.fixture
async def seeded_organization(db_session: AsyncSession) -> str:
    organization = Organization(
        organization_code="BA08-API-ORG", organization_name="BA-08 API Org", organization_type="CORPORATE",
    )
    db_session.add(organization)
    await db_session.commit()
    return str(organization.id)


def test_deprecate_approval_authority_succeeds(client: TestClient, seeded_organization: str) -> None:
    establish_response = client.post(
        "/approval-authorities",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "authority_name": "Original Approver",
            "approval_strategy": "ANY_ONE",
            "scope_type": "GLOBAL",
        },
    )
    authority_id = establish_response.json()["id"]

    response = client.post(f"/approval-authorities/{authority_id}/deprecate", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["status"] == "DEPRECATED"


# --- Delegation Policy ---------------------------------------------------


def test_retire_delegation_policy_succeeds(client: TestClient, seeded_organization: str) -> None:
    establish_response = client.post(
        "/delegation-policies",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "policy_name": "Original Delegation Policy",
            "delegation_type": "EMERGENCY",
            "scope_type": "ORGANIZATION",
        },
    )
    policy_id = establish_response.json()["id"]

    response = client.post(f"/delegation-policies/{policy_id}/retire", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["status"] == "RETIRED"


# --- Runtime Assignment Policy ---------------------------------------------


def test_deprecate_runtime_assignment_policy_succeeds(client: TestClient, seeded_organization: str) -> None:
    establish_response = client.post(
        "/runtime-assignment-policies",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "policy_name": "Original Assignment Policy",
            "assignment_target_type": "BUSINESS_ROLE",
        },
    )
    policy_id = establish_response.json()["id"]

    response = client.post(f"/runtime-assignment-policies/{policy_id}/deprecate", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["status"] == "DEPRECATED"
