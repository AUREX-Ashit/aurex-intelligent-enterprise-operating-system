import uuid
from fastapi.testclient import TestClient

def test_health_check_endpoint(client: TestClient) -> None:
    """
    Validates general routing and health check feedback.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_login_without_tenant_header_falls_back_to_auto_discovery(client: TestClient) -> None:
    """
    WP-00A: X-Tenant-ID is optional on /auth/login by design (routers/auth.py's
    own docstring — omitted means auto-select on a single membership, or an
    OrganizationSelectionResponse on multiple). A nonexistent identity with no
    header therefore resolves as 401 Invalid credentials, not 400 — this test
    previously asserted the header was mandatory, which stopped matching
    routers/auth.py once the auto-discovery flow was implemented.
    """
    response = client.post(
        "/auth/login",
        json={"email": "test@corpstage.com", "password": "superPassword123"}
    )
    assert response.status_code == 401


def test_login_invalid_tenant_uuid(client: TestClient) -> None:
    """
    Asserts request is blocked when X-Tenant-ID is non-compliant with UUID RFC 4122.
    """
    headers = {"X-Tenant-ID": "invalid-uuid-format"}
    response = client.post(
        "/auth/login",
        headers=headers,
        json={"email": "test@corpstage.com", "password": "superPassword123"}
    )
    assert response.status_code == 400
    assert "UUID" in response.json()["detail"]


def test_login_validation_failure(client: TestClient) -> None:
    """
    Asserts validation failure logs on invalid credentials schemas.
    """
    headers = {"X-Tenant-ID": str(uuid.uuid4())}
    # Email field is structurally invalid
    response = client.post(
        "/auth/login",
        headers=headers,
        json={"email": "not-an-email", "password": "short"}
    )
    assert response.status_code == 422
    assert "detail" in response.json()


def test_refresh_token_missing_authorization(client: TestClient) -> None:
    """
    Asserts request is blocked when authorization token is missing.
    """
    response = client.post("/auth/refresh")
    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]
