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
async def seeded_membership_and_domain(db_session: AsyncSession) -> tuple[str, str]:
    person = Person(first_name="Dom", last_name="Owner", display_name="Dom Owner")
    organization = Organization(
        organization_code="DP-API-TEST-ORG",
        organization_name="Domain Permission API Test Org",
        organization_type="CORPORATE",
    )
    role = Role(role_code="DP_API_TEST_ROLE", role_name="Domain Permission API Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    domain = Domain(domain_name="Finance")
    db_session.add_all([membership, domain])
    await db_session.commit()

    return str(membership.id), str(domain.id)


def test_establish_domain_permission_succeeds_for_platform_admin(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id = seeded_membership_and_domain

    response = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={
            "membership_id": membership_id,
            "domain_id": domain_id,
            "permission_level": "APPROVE",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["membership_id"] == membership_id
    assert body["domain_id"] == domain_id
    assert body["permission_level"] == "APPROVE"
    assert "id" in body


def test_establish_domain_permission_rejects_duplicate_active_grant(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id = seeded_membership_and_domain
    payload = {"membership_id": membership_id, "domain_id": domain_id, "permission_level": "EDIT"}

    first = client.post("/domain-permissions", headers=_auth_headers(), json=payload)
    assert first.status_code == 201

    second = client.post("/domain-permissions", headers=_auth_headers(), json=payload)
    assert second.status_code == 409


def test_establish_domain_permission_rejects_unknown_domain(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, _domain_id = seeded_membership_and_domain

    response = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={
            "membership_id": membership_id,
            "domain_id": str(uuid.uuid4()),
            "permission_level": "VIEW",
        },
    )

    assert response.status_code == 404


def test_establish_domain_permission_requires_authorization_header(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id = seeded_membership_and_domain

    response = client.post(
        "/domain-permissions",
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_establish_domain_permission_rejects_non_platform_admin(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id = seeded_membership_and_domain

    response = client.post(
        "/domain-permissions",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )

    assert response.status_code == 403


def test_establish_domain_permission_rejects_invalid_permission_level(
    client: TestClient, seeded_membership_and_domain
) -> None:
    """permission_level must be one of URA-001-47's eight values."""
    membership_id, domain_id = seeded_membership_and_domain

    response = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "NOT_A_REAL_LEVEL"},
    )

    assert response.status_code == 422


def test_get_domain_permission_by_id_succeeds_for_platform_admin(
    client: TestClient, seeded_membership_and_domain
) -> None:
    """BA-01/EX-C003-11 single-item branch."""
    membership_id, domain_id = seeded_membership_and_domain
    created = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()

    response = client.get(f"/domain-permissions/{created['id']}", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_domain_permission_by_id_rejects_unknown_id(client: TestClient) -> None:
    response = client.get(f"/domain-permissions/{uuid.uuid4()}", headers=_auth_headers())

    assert response.status_code == 404


def test_get_domain_permission_by_id_requires_authorization_header(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id = seeded_membership_and_domain
    created = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()

    response = client.get(f"/domain-permissions/{created['id']}")

    assert response.status_code == 400


def test_get_domain_permission_by_id_rejects_non_platform_admin(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id = seeded_membership_and_domain
    created = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()

    response = client.get(f"/domain-permissions/{created['id']}", headers=_auth_headers(role_code="ESG_MANAGER"))

    assert response.status_code == 403


def test_list_domain_permissions_with_no_filters_returns_all(
    client: TestClient, seeded_membership_and_domain
) -> None:
    """BA-01/EX-C003-11 list branch."""
    membership_id, domain_id = seeded_membership_and_domain
    client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )
    client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "EDIT"},
    )

    response = client.get("/domain-permissions", headers=_auth_headers())

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_domain_permissions_filters_by_domain_id(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id = seeded_membership_and_domain
    client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )

    response = client.get(f"/domain-permissions?domain_id={domain_id}", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["domain_id"] == domain_id


def test_list_domain_permissions_filters_by_status(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id = seeded_membership_and_domain
    created = client.post(
        "/domain-permissions",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()
    client.post(f"/domain-permissions/{created['id']}/deprecate", headers=_auth_headers())

    active_response = client.get("/domain-permissions?status=ACTIVE", headers=_auth_headers())
    deprecated_response = client.get("/domain-permissions?status=DEPRECATED", headers=_auth_headers())

    assert active_response.json() == []
    assert len(deprecated_response.json()) == 1
    assert deprecated_response.json()[0]["id"] == created["id"]


def test_list_domain_permissions_requires_authorization_header(client: TestClient) -> None:
    response = client.get("/domain-permissions")

    assert response.status_code == 400


def test_list_domain_permissions_rejects_non_platform_admin(client: TestClient) -> None:
    response = client.get("/domain-permissions", headers=_auth_headers(role_code="ESG_MANAGER"))

    assert response.status_code == 403
