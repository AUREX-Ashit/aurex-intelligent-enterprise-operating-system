"""
WP-02 BA-07 — Version and Re-effective-Date Authorization Policy Object
(ERB-C003-02 / EX-C003-07). API-layer tests for the five new
POST /{resource}/{id}/versions endpoints — one representative success
path per object type, plus the shared 404/409/403/400 behavior exercised
once (on Role) rather than five times, since the underlying service
logic is identical across types (see the service-layer test file for
the full per-type amendable-field coverage).
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


def test_version_role_succeeds_and_preserves_prior_version(client: TestClient) -> None:
    establish_response = client.post(
        "/roles",
        headers=_auth_headers(),
        json={"role_code": "BA07_API_ROLE", "role_name": "Original"},
    )
    assert establish_response.status_code == 201
    role_id = establish_response.json()["id"]

    version_response = client.post(
        f"/roles/{role_id}/versions",
        headers=_auth_headers(),
        json={"role_name": "Amended"},
    )

    assert version_response.status_code == 201
    body = version_response.json()
    assert body["role_name"] == "Amended"
    assert body["version"] == 2
    assert body["status"] == "ACTIVE"
    assert body["supersedes_id"] == role_id


def test_version_role_rejects_a_second_amendment_of_the_now_superseded_original(client: TestClient) -> None:
    establish_response = client.post(
        "/roles",
        headers=_auth_headers(),
        json={"role_code": "BA07_API_ROLE_CONFLICT", "role_name": "Original"},
    )
    role_id = establish_response.json()["id"]
    client.post(f"/roles/{role_id}/versions", headers=_auth_headers(), json={"role_name": "V2"})

    conflict_response = client.post(
        f"/roles/{role_id}/versions",
        headers=_auth_headers(),
        json={"role_name": "V3"},
    )
    assert conflict_response.status_code == 409


def test_version_role_rejects_unknown_role(client: TestClient) -> None:
    response = client.post(
        f"/roles/{uuid.uuid4()}/versions",
        headers=_auth_headers(),
        json={"role_name": "X"},
    )
    assert response.status_code == 404


def test_version_role_rejects_non_platform_admin(client: TestClient) -> None:
    establish_response = client.post(
        "/roles",
        headers=_auth_headers(),
        json={"role_code": "BA07_API_ROLE_AUTH", "role_name": "Original"},
    )
    role_id = establish_response.json()["id"]

    response = client.post(
        f"/roles/{role_id}/versions",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"role_name": "X"},
    )
    assert response.status_code == 403


def test_version_role_requires_authorization_header(client: TestClient) -> None:
    establish_response = client.post(
        "/roles",
        headers=_auth_headers(),
        json={"role_code": "BA07_API_ROLE_NOAUTH", "role_name": "Original"},
    )
    role_id = establish_response.json()["id"]

    response = client.post(f"/roles/{role_id}/versions", json={"role_name": "X"})
    assert response.status_code == 400


# --- Domain Permission -----------------------------------------------------


@pytest.fixture
async def seeded_membership_and_domain(db_session: AsyncSession) -> tuple[str, str]:
    person = Person(first_name="BA07", last_name="Versioning", display_name="BA07 Versioning")
    organization = Organization(
        organization_code="BA07-API-DP-ORG", organization_name="BA-07 API DP Org", organization_type="CORPORATE",
    )
    role = Role(role_code="BA07_API_DP_ROLE", role_name="BA-07 API DP Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    domain = Domain(domain_name="Finance")
    db_session.add_all([membership, domain])
    await db_session.commit()

    return str(membership.id), str(domain.id)


def test_version_domain_permission_succeeds(client: TestClient, seeded_membership_and_domain) -> None:
    membership_id, domain_id = seeded_membership_and_domain
    establish_response = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )
    assert establish_response.status_code == 201
    grant_id = establish_response.json()["id"]

    version_response = client.post(
        f"/domain-permissions/{grant_id}/versions",
        headers=_auth_headers(),
        json={},
    )

    assert version_response.status_code == 201
    body = version_response.json()
    assert body["permission_level"] == "VIEW"
    assert body["version"] == 2
    assert body["supersedes_id"] == grant_id


# --- Approval Authority ------------------------------------------------


@pytest.fixture
async def seeded_organization(db_session: AsyncSession) -> str:
    organization = Organization(
        organization_code="BA07-API-AA-ORG", organization_name="BA-07 API AA Org", organization_type="CORPORATE",
    )
    db_session.add(organization)
    await db_session.commit()
    return str(organization.id)


def test_version_approval_authority_succeeds(client: TestClient, seeded_organization: str) -> None:
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
    assert establish_response.status_code == 201
    authority_id = establish_response.json()["id"]

    version_response = client.post(
        f"/approval-authorities/{authority_id}/versions",
        headers=_auth_headers(),
        json={"authority_name": "Amended Approver"},
    )

    assert version_response.status_code == 201
    body = version_response.json()
    assert body["authority_name"] == "Amended Approver"
    assert body["scope_type"] == "GLOBAL"
    assert body["version"] == 2


# --- Delegation Policy ---------------------------------------------------


def test_version_delegation_policy_succeeds(client: TestClient, seeded_organization: str) -> None:
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
    assert establish_response.status_code == 201
    policy_id = establish_response.json()["id"]

    version_response = client.post(
        f"/delegation-policies/{policy_id}/versions",
        headers=_auth_headers(),
        json={"sub_delegation_allowed": True},
    )

    assert version_response.status_code == 201
    body = version_response.json()
    assert body["sub_delegation_allowed"] is True
    assert body["delegation_type"] == "EMERGENCY"
    assert body["version"] == 2


# --- Runtime Assignment Policy ---------------------------------------------


def test_version_runtime_assignment_policy_succeeds(client: TestClient, seeded_organization: str) -> None:
    establish_response = client.post(
        "/runtime-assignment-policies",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "policy_name": "Original Assignment Policy",
            "assignment_target_type": "BUSINESS_ROLE",
        },
    )
    assert establish_response.status_code == 201
    policy_id = establish_response.json()["id"]

    version_response = client.post(
        f"/runtime-assignment-policies/{policy_id}/versions",
        headers=_auth_headers(),
        json={"policy_name": "Amended Assignment Policy"},
    )

    assert version_response.status_code == 201
    body = version_response.json()
    assert body["policy_name"] == "Amended Assignment Policy"
    assert body["assignment_target_type"] == "BUSINESS_ROLE"
    assert body["version"] == 2
