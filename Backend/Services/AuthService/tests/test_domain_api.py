import uuid
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt

from config import settings


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


def test_list_domains_returns_empty_catalog_before_seeding(client: TestClient) -> None:
    """No domains exist until MDP-001 §B2a seeds the 7 platform defaults — an empty list is the correct response, not an error."""
    response = client.get("/domains", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json() == []


def test_get_domain_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.get(f"/domains/{uuid.uuid4()}", headers=_auth_headers())

    assert response.status_code == 404


def test_list_domains_requires_authorization_header(client: TestClient) -> None:
    response = client.get("/domains")

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_list_domains_rejects_invalid_token(client: TestClient) -> None:
    response = client.get("/domains", headers={"Authorization": "Bearer not-a-real-token"})

    assert response.status_code == 401


def test_list_domains_rejects_non_platform_admin(client: TestClient) -> None:
    response = client.get("/domains", headers=_auth_headers(role_code="ESG_MANAGER"))

    assert response.status_code == 403


def test_get_domain_rejects_non_platform_admin(client: TestClient) -> None:
    response = client.get(
        f"/domains/{uuid.uuid4()}", headers=_auth_headers(role_code="ESG_MANAGER")
    )

    assert response.status_code == 403
