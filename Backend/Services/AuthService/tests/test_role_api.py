from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt

from config import settings


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
    """
    Builds a signed access token with the given role_code claim, mirroring
    test_organization_api.py's _access_token() exactly — this module
    exercises Establish Role's authorization dependency, not the login flow.
    """
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


def test_establish_role_succeeds_for_platform_admin(client: TestClient) -> None:
    response = client.post(
        "/roles",
        headers=_auth_headers(),
        json={
            "role_code": "API-ROLE-001",
            "role_name": "API Test Role",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["role_code"] == "API-ROLE-001"
    assert body["role_name"] == "API Test Role"
    assert body["is_system_role"] is False
    assert "id" in body


def test_establish_system_role_succeeds_for_platform_admin(client: TestClient) -> None:
    response = client.post(
        "/roles",
        headers=_auth_headers(),
        json={
            "role_code": "API-ROLE-SYS-001",
            "role_name": "API Test System Role",
            "is_system_role": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["is_system_role"] is True


def test_establish_role_rejects_duplicate_code(client: TestClient) -> None:
    payload = {"role_code": "API-ROLE-002", "role_name": "API Test Role"}
    first = client.post("/roles", headers=_auth_headers(), json=payload)
    assert first.status_code == 201

    second = client.post("/roles", headers=_auth_headers(), json=payload)
    assert second.status_code == 409


def test_establish_role_requires_authorization_header(client: TestClient) -> None:
    """No Authorization header at all -> 400, per dependencies.get_current_claims."""
    response = client.post(
        "/roles",
        json={"role_code": "API-ROLE-003", "role_name": "API Test Role"},
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_establish_role_rejects_invalid_token(client: TestClient) -> None:
    response = client.post(
        "/roles",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={"role_code": "API-ROLE-004", "role_name": "API Test Role"},
    )

    assert response.status_code == 401


def test_establish_role_rejects_non_platform_admin(client: TestClient) -> None:
    """
    IRA-002 §2.7's stated simplification: only PLATFORM_ADMIN is gated
    on today, pending ADR-002's resolution of the canonical role
    catalog — any other role_code claim is rejected with 403.
    """
    response = client.post(
        "/roles",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"role_code": "API-ROLE-005", "role_name": "API Test Role"},
    )

    assert response.status_code == 403


def test_establish_role_rejects_missing_role_name(client: TestClient) -> None:
    response = client.post(
        "/roles",
        headers=_auth_headers(),
        json={"role_code": "API-ROLE-006"},
    )

    assert response.status_code == 422
