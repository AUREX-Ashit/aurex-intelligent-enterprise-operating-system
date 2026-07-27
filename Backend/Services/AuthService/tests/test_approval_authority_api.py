import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.domain import Domain
from models.organization import Organization


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
    """Mirrors test_role_api.py's _access_token() exactly."""
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
async def seeded_organization_and_domain(db_session: AsyncSession) -> tuple[str, str]:
    organization = Organization(
        organization_code="AA-API-TEST-ORG",
        organization_name="Approval Authority API Test Org",
        organization_type="CORPORATE",
    )
    domain = Domain(domain_name="Finance")
    db_session.add_all([organization, domain])
    await db_session.commit()
    return str(organization.id), str(domain.id)


def test_establish_approval_authority_global_scope_succeeds(
    client: TestClient, seeded_organization_and_domain
) -> None:
    organization_id, _domain_id = seeded_organization_and_domain

    response = client.post(
        "/approval-authorities",
        headers=_auth_headers(),
        json={
            "organization_id": organization_id,
            "authority_name": "Global Framework Approval",
            "approval_strategy": "ANY_ONE",
            "scope_type": "GLOBAL",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["scope_type"] == "GLOBAL"
    assert body["domain_id"] is None
    assert "id" in body


def test_establish_approval_authority_domain_scope_succeeds(
    client: TestClient, seeded_organization_and_domain
) -> None:
    organization_id, domain_id = seeded_organization_and_domain

    response = client.post(
        "/approval-authorities",
        headers=_auth_headers(),
        json={
            "organization_id": organization_id,
            "authority_name": "Revenue CDE Approval",
            "approval_strategy": "MAJORITY",
            "majority_threshold_pct": 66,
            "scope_type": "DOMAIN",
            "domain_id": domain_id,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["scope_type"] == "DOMAIN"
    assert body["domain_id"] == domain_id


def test_establish_approval_authority_object_scope_succeeds(
    client: TestClient, seeded_organization_and_domain
) -> None:
    organization_id, _domain_id = seeded_organization_and_domain

    response = client.post(
        "/approval-authorities",
        headers=_auth_headers(),
        json={
            "organization_id": organization_id,
            "authority_name": "Revenue CDE Approval",
            "approval_strategy": "ALL",
            "scope_type": "OBJECT",
            "object_type": "revenue_cde",
            "object_id": str(uuid.uuid4()),
        },
    )

    assert response.status_code == 201
    assert response.json()["scope_type"] == "OBJECT"


def test_establish_approval_authority_rejects_ambiguous_scope(
    client: TestClient, seeded_organization_and_domain
) -> None:
    """GLOBAL scope with a Domain anchor set — the dual-stated case EX-C003-03 forbids."""
    organization_id, domain_id = seeded_organization_and_domain

    response = client.post(
        "/approval-authorities",
        headers=_auth_headers(),
        json={
            "organization_id": organization_id,
            "authority_name": "Global Framework Approval",
            "approval_strategy": "ANY_ONE",
            "scope_type": "GLOBAL",
            "domain_id": domain_id,
        },
    )

    assert response.status_code == 422


def test_establish_approval_authority_rejects_domain_scope_missing_domain_id(
    client: TestClient, seeded_organization_and_domain
) -> None:
    organization_id, _domain_id = seeded_organization_and_domain

    response = client.post(
        "/approval-authorities",
        headers=_auth_headers(),
        json={
            "organization_id": organization_id,
            "authority_name": "Revenue CDE Approval",
            "approval_strategy": "MAJORITY",
            "scope_type": "DOMAIN",
        },
    )

    assert response.status_code == 422


def test_establish_approval_authority_rejects_unknown_organization(
    client: TestClient,
) -> None:
    response = client.post(
        "/approval-authorities",
        headers=_auth_headers(),
        json={
            "organization_id": str(uuid.uuid4()),
            "authority_name": "Global Framework Approval",
            "approval_strategy": "ANY_ONE",
            "scope_type": "GLOBAL",
        },
    )

    assert response.status_code == 404


def test_establish_approval_authority_requires_authorization_header(
    client: TestClient, seeded_organization_and_domain
) -> None:
    organization_id, _domain_id = seeded_organization_and_domain

    response = client.post(
        "/approval-authorities",
        json={
            "organization_id": organization_id,
            "authority_name": "Global Framework Approval",
            "approval_strategy": "ANY_ONE",
            "scope_type": "GLOBAL",
        },
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_establish_approval_authority_rejects_non_platform_admin(
    client: TestClient, seeded_organization_and_domain
) -> None:
    organization_id, _domain_id = seeded_organization_and_domain

    response = client.post(
        "/approval-authorities",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={
            "organization_id": organization_id,
            "authority_name": "Global Framework Approval",
            "approval_strategy": "ANY_ONE",
            "scope_type": "GLOBAL",
        },
    )

    assert response.status_code == 403
