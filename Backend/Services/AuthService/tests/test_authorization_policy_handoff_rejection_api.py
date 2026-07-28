"""
WP-02 BA-10 — Resolve Dependent Capability Authorization Policy
Hand-off Rejection (ERB-C003-03 / EX-C003-10). API-layer tests for the
five new POST /{resource}/{id}/handoff-rejection endpoints — Role
covered for both classification branches plus shared 404/403/400
behavior; the other four types covered once each for the clean/
capability-scoped path, since the underlying service logic is
identical (see the service-layer test file for the full branch
coverage).
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


def test_report_role_handoff_rejection_capability_scoped(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA10_API_ROLE_1", "role_name": "V1"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(
        f"/roles/{role_id}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-002", "stated_reason": "Could not resolve a valid grant."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "CAPABILITY_SCOPED_INSUFFICIENCY"
    assert body["object_preserved"] is True
    assert body["routed_to"] is None


def test_report_role_handoff_rejection_integrity_signal_for_retired_role(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA10_API_ROLE_2", "role_name": "V1"}
    )
    role_id = establish_response.json()["id"]
    client.post(f"/roles/{role_id}/retire", headers=_auth_headers())

    response = client.post(
        f"/roles/{role_id}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-002", "stated_reason": "Cannot rely on this role."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "INTEGRITY_SIGNAL"
    assert body["object_preserved"] is False
    assert body["routed_to"] is not None


def test_report_role_handoff_rejection_rejects_unknown_role(client: TestClient) -> None:
    response = client.post(
        f"/roles/{uuid.uuid4()}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-002", "stated_reason": "X"},
    )
    assert response.status_code == 404


def test_report_role_handoff_rejection_rejects_non_platform_admin(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA10_API_ROLE_AUTH", "role_name": "V1"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(
        f"/roles/{role_id}/handoff-rejection",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"reporting_capability": "C-002", "stated_reason": "X"},
    )
    assert response.status_code == 403


def test_report_role_handoff_rejection_requires_authorization_header(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA10_API_ROLE_NOAUTH", "role_name": "V1"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(
        f"/roles/{role_id}/handoff-rejection",
        json={"reporting_capability": "C-002", "stated_reason": "X"},
    )
    assert response.status_code == 400


def test_report_role_handoff_rejection_requires_stated_reason(client: TestClient) -> None:
    establish_response = client.post(
        "/roles", headers=_auth_headers(), json={"role_code": "BA10_API_ROLE_NOREASON", "role_name": "V1"}
    )
    role_id = establish_response.json()["id"]

    response = client.post(
        f"/roles/{role_id}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-002", "stated_reason": ""},
    )
    assert response.status_code == 422


# --- Domain Permission / Approval Authority / Delegation Policy / Runtime --


@pytest.fixture
async def seeded_organization(db_session: AsyncSession) -> str:
    organization = Organization(
        organization_code="BA10-API-ORG", organization_name="BA-10 API Org", organization_type="CORPORATE",
    )
    db_session.add(organization)
    await db_session.commit()
    return str(organization.id)


def test_report_approval_authority_handoff_rejection_capability_scoped(client: TestClient, seeded_organization: str) -> None:
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

    response = client.post(
        f"/approval-authorities/{authority_id}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-002", "stated_reason": "Could not resolve."},
    )

    assert response.status_code == 200
    assert response.json()["classification"] == "CAPABILITY_SCOPED_INSUFFICIENCY"


def test_report_delegation_policy_handoff_rejection_capability_scoped(client: TestClient, seeded_organization: str) -> None:
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

    response = client.post(
        f"/delegation-policies/{policy_id}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-002", "stated_reason": "Could not resolve."},
    )

    assert response.status_code == 200
    assert response.json()["classification"] == "CAPABILITY_SCOPED_INSUFFICIENCY"


@pytest.fixture
async def seeded_membership_and_domain(db_session: AsyncSession) -> tuple[str, str]:
    person = Person(first_name="BA10", last_name="DPAPI", display_name="BA10 DP API")
    organization = Organization(
        organization_code="BA10-API-DP-ORG", organization_name="BA-10 API DP Org", organization_type="CORPORATE",
    )
    role = Role(role_code="BA10_API_DP_ROLE", role_name="BA-10 API DP Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    domain = Domain(domain_name="Finance")
    db_session.add_all([membership, domain])
    await db_session.commit()

    return str(membership.id), str(domain.id)


def test_report_domain_permission_handoff_rejection_capability_scoped(client: TestClient, seeded_membership_and_domain) -> None:
    membership_id, domain_id = seeded_membership_and_domain
    establish_response = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )
    grant_id = establish_response.json()["id"]

    response = client.post(
        f"/domain-permissions/{grant_id}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-002", "stated_reason": "Could not resolve."},
    )

    assert response.status_code == 200
    assert response.json()["classification"] == "CAPABILITY_SCOPED_INSUFFICIENCY"


def test_report_runtime_assignment_policy_handoff_rejection_capability_scoped(client: TestClient, seeded_organization: str) -> None:
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

    response = client.post(
        f"/runtime-assignment-policies/{policy_id}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-002", "stated_reason": "Could not resolve."},
    )

    assert response.status_code == 200
    assert response.json()["classification"] == "CAPABILITY_SCOPED_INSUFFICIENCY"
