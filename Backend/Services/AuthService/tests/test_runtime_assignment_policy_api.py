import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.organization import Organization


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
    """Mirrors test_delegation_policy_api.py's _access_token() exactly."""
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


@pytest.fixture
async def seeded_organization(db_session: AsyncSession) -> str:
    organization = Organization(
        organization_code="RAP-POLICY-API-TEST-ORG",
        organization_name="Runtime Assignment Policy API Test Org",
        organization_type="CORPORATE",
    )
    db_session.add(organization)
    await db_session.commit()
    return str(organization.id)


def test_establish_runtime_assignment_policy_business_role_target_succeeds(
    client: TestClient, seeded_organization: str
) -> None:
    response = client.post(
        "/runtime-assignment-policies",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "policy_name": "Revenue CDE Review Assignment Policy",
            "assignment_target_type": "BUSINESS_ROLE",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["assignment_target_type"] == "BUSINESS_ROLE"
    assert body["configured_lifecycle_states"] == [
        "CREATED", "ASSIGNED", "ACCEPTED", "IN_PROGRESS", "COMPLETED",
        "REJECTED", "ESCALATED", "EXPIRED", "ARCHIVED",
    ]
    assert body["escalation_policy_id"] is None
    assert "id" in body


def test_establish_runtime_assignment_policy_with_custom_lifecycle_states_succeeds(
    client: TestClient, seeded_organization: str
) -> None:
    response = client.post(
        "/runtime-assignment-policies",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "policy_name": "Board Approval Assignment Policy",
            "assignment_target_type": "GROUP",
            "configured_lifecycle_states": [
                "CREATED", "ASSIGNED", "ACCEPTED", "IN_PROGRESS", "COMPLETED",
                "REJECTED", "ESCALATED", "EXPIRED", "ARCHIVED", "BOARD_APPROVED",
            ],
        },
    )

    assert response.status_code == 201
    assert "BOARD_APPROVED" in response.json()["configured_lifecycle_states"]


def test_establish_runtime_assignment_policy_with_escalation_reference_succeeds(
    client: TestClient, seeded_organization: str
) -> None:
    escalation_policy_id = str(uuid.uuid4())

    response = client.post(
        "/runtime-assignment-policies",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "policy_name": "Escalating Review Assignment Policy",
            "assignment_target_type": "NAMED_USER",
            "escalation_policy_id": escalation_policy_id,
        },
    )

    assert response.status_code == 201
    assert response.json()["escalation_policy_id"] == escalation_policy_id


def test_establish_runtime_assignment_policy_rejects_invalid_target_type(
    client: TestClient, seeded_organization: str
) -> None:
    response = client.post(
        "/runtime-assignment-policies",
        headers=_auth_headers(),
        json={
            "organization_id": seeded_organization,
            "policy_name": "Revenue CDE Review Assignment Policy",
            "assignment_target_type": "NOT_A_REAL_TARGET",
        },
    )

    assert response.status_code == 422


def test_establish_runtime_assignment_policy_rejects_unknown_organization(
    client: TestClient,
) -> None:
    response = client.post(
        "/runtime-assignment-policies",
        headers=_auth_headers(),
        json={
            "organization_id": str(uuid.uuid4()),
            "policy_name": "Revenue CDE Review Assignment Policy",
            "assignment_target_type": "BUSINESS_ROLE",
        },
    )

    assert response.status_code == 404


def test_establish_runtime_assignment_policy_requires_authorization_header(
    client: TestClient, seeded_organization: str
) -> None:
    response = client.post(
        "/runtime-assignment-policies",
        json={
            "organization_id": seeded_organization,
            "policy_name": "Revenue CDE Review Assignment Policy",
            "assignment_target_type": "BUSINESS_ROLE",
        },
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_establish_runtime_assignment_policy_rejects_non_platform_admin(
    client: TestClient, seeded_organization: str
) -> None:
    response = client.post(
        "/runtime-assignment-policies",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={
            "organization_id": seeded_organization,
            "policy_name": "Revenue CDE Review Assignment Policy",
            "assignment_target_type": "BUSINESS_ROLE",
        },
    )

    assert response.status_code == 403
