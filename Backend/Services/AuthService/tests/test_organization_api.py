from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt

from config import settings


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
    """
    Builds a signed access token with the given role_code claim, bypassing
    a real /auth/login round-trip — this test module is exercising
    Establish Organization's authorization dependency, not the login flow
    (already covered by test_auth.py). Uses the real settings.jwt_secret_key
    / settings.jwt_algorithm so decode_access_token() verifies it exactly
    as it would a real token.
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


def test_establish_organization_succeeds_for_platform_admin(client: TestClient) -> None:
    response = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={
            "organization_code": "API-ORG-001",
            "organization_name": "API Test Org",
            "organization_type": "CORPORATE",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["organization_code"] == "API-ORG-001"
    assert body["status"] == "ACTIVE"
    assert body["is_active"] is True
    assert "id" in body


def test_establish_organization_rejects_duplicate_code(client: TestClient) -> None:
    payload = {
        "organization_code": "API-ORG-002",
        "organization_name": "API Test Org",
        "organization_type": "CORPORATE",
    }
    first = client.post("/organizations", headers=_auth_headers(), json=payload)
    assert first.status_code == 201

    second = client.post("/organizations", headers=_auth_headers(), json=payload)
    assert second.status_code == 409


def test_establish_organization_requires_authorization_header(client: TestClient) -> None:
    """No Authorization header at all -> 400, per dependencies.get_current_claims."""
    response = client.post(
        "/organizations",
        json={
            "organization_code": "API-ORG-003",
            "organization_name": "API Test Org",
            "organization_type": "CORPORATE",
        },
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_establish_organization_rejects_invalid_token(client: TestClient) -> None:
    response = client.post(
        "/organizations",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={
            "organization_code": "API-ORG-004",
            "organization_name": "API Test Org",
            "organization_type": "CORPORATE",
        },
    )

    assert response.status_code == 401


def test_establish_organization_rejects_non_platform_admin_role(client: TestClient) -> None:
    """
    IRA-001 §2.7: only PLATFORM_ADMIN may establish an organization.
    A validly-signed token for any other role must be rejected with 403,
    not silently allowed.
    """
    response = client.post(
        "/organizations",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={
            "organization_code": "API-ORG-005",
            "organization_name": "API Test Org",
            "organization_type": "CORPORATE",
        },
    )

    assert response.status_code == 403


def test_establish_organization_rejects_missing_required_field(client: TestClient) -> None:
    response = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={"organization_name": "Missing Code Org", "organization_type": "CORPORATE"},
    )

    assert response.status_code == 422


def test_establish_organization_rejects_empty_required_field(client: TestClient) -> None:
    response = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={
            "organization_code": "",
            "organization_name": "Empty Code Org",
            "organization_type": "CORPORATE",
        },
    )

    assert response.status_code == 422


def test_establish_organization_does_not_require_tenant_header(client: TestClient) -> None:
    """
    POST /organizations is tenant-agnostic (middleware/tenant.py's
    exemption list) — establishing a brand-new Organization has no
    existing tenant to scope to. No X-Tenant-ID header is sent here at
    all; if TenantMiddleware were not exempting this path, this would
    fail with 400 ("Header 'X-Tenant-ID' is required...") instead of 201.
    """
    response = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={
            "organization_code": "API-ORG-006",
            "organization_name": "API Test Org",
            "organization_type": "CORPORATE",
        },
    )

    assert response.status_code == 201
