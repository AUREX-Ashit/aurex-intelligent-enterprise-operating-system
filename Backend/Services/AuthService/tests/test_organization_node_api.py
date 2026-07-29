import uuid
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt

from config import settings


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
    """
    Builds a signed access token with the given role_code claim, bypassing
    a real /auth/login round-trip — this test module is exercising
    Establish Organization Node's authorization dependency, not the login
    flow (already covered by test_auth.py). Mirrors test_organization_api.
    py's own _access_token helper exactly.
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


def test_establish_organization_node_succeeds_for_platform_admin(client: TestClient) -> None:
    response = client.post(
        "/organization-nodes",
        headers=_auth_headers(),
        json={
            "node_code": "API-NODE-001",
            "node_name": "API Test Node",
            "node_type": "HOLDING",
            "legal_entity_name": "API Test Legal Entity",
            "business_unit": "API Operations",
            "sector": "Manufacturing",
            "operational_status": "ACTIVE",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["node_code"] == "API-NODE-001"
    assert body["node_name"] == "API Test Node"
    assert body["node_type"] == "HOLDING"
    assert body["legal_entity_name"] == "API Test Legal Entity"
    assert body["business_unit"] == "API Operations"
    assert body["sector"] == "Manufacturing"
    assert body["operational_status"] == "ACTIVE"
    assert body["active_flag"] is True
    assert "id" in body


def test_establish_organization_node_allows_optional_fields_to_be_omitted(client: TestClient) -> None:
    response = client.post(
        "/organization-nodes",
        headers=_auth_headers(),
        json={
            "node_code": "API-NODE-002",
            "node_name": "API Test Node Minimal",
            "node_type": "ENTITY",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["legal_entity_name"] is None
    assert body["business_unit"] is None
    assert body["sector"] is None
    assert body["operational_status"] is None


def test_establish_organization_node_rejects_duplicate_code(client: TestClient) -> None:
    payload = {
        "node_code": "API-NODE-003",
        "node_name": "API Test Node",
        "node_type": "HOLDING",
    }
    first = client.post("/organization-nodes", headers=_auth_headers(), json=payload)
    assert first.status_code == 201

    second = client.post("/organization-nodes", headers=_auth_headers(), json=payload)
    assert second.status_code == 409


def test_establish_organization_node_requires_authorization_header(client: TestClient) -> None:
    """No Authorization header at all -> 400, per dependencies.get_current_claims."""
    response = client.post(
        "/organization-nodes",
        json={
            "node_code": "API-NODE-004",
            "node_name": "API Test Node",
            "node_type": "HOLDING",
        },
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_establish_organization_node_rejects_invalid_token(client: TestClient) -> None:
    response = client.post(
        "/organization-nodes",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={
            "node_code": "API-NODE-005",
            "node_name": "API Test Node",
            "node_type": "HOLDING",
        },
    )

    assert response.status_code == 401


def test_establish_organization_node_rejects_non_platform_admin_role(client: TestClient) -> None:
    """Only PLATFORM_ADMIN may establish an organization node (same interim gate WP-01/02/03 all used)."""
    response = client.post(
        "/organization-nodes",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={
            "node_code": "API-NODE-006",
            "node_name": "API Test Node",
            "node_type": "HOLDING",
        },
    )

    assert response.status_code == 403


def test_establish_organization_node_rejects_missing_required_field(client: TestClient) -> None:
    response = client.post(
        "/organization-nodes",
        headers=_auth_headers(),
        json={"node_name": "Missing Code Node", "node_type": "HOLDING"},
    )

    assert response.status_code == 422


def test_establish_organization_node_rejects_empty_required_field(client: TestClient) -> None:
    response = client.post(
        "/organization-nodes",
        headers=_auth_headers(),
        json={
            "node_code": "",
            "node_name": "Empty Code Node",
            "node_type": "HOLDING",
        },
    )

    assert response.status_code == 422


def test_establish_organization_node_does_not_require_tenant_header(client: TestClient) -> None:
    """
    POST /organization-nodes is tenant-agnostic (middleware/tenant.py's
    exemption list) — OrganizationNode carries no organization_id column
    at all. No X-Tenant-ID header is sent here at all; if TenantMiddleware
    were not exempting this path, this would fail with 400 instead of 201.
    """
    response = client.post(
        "/organization-nodes",
        headers=_auth_headers(),
        json={
            "node_code": "API-NODE-007",
            "node_name": "API Test Node",
            "node_type": "HOLDING",
        },
    )

    assert response.status_code == 201


# ---------------------------------------------------------------------------
# BA-02 — Understand Structural Position
# ---------------------------------------------------------------------------

def test_get_organization_node_returns_details_for_platform_admin(client: TestClient) -> None:
    established = client.post(
        "/organization-nodes",
        headers=_auth_headers(),
        json={
            "node_code": "API-NODE-008",
            "node_name": "API View Node",
            "node_type": "HOLDING",
            "legal_entity_name": "API View Legal Entity",
        },
    )
    assert established.status_code == 201
    organization_node_id = established.json()["id"]

    response = client.get(f"/organization-nodes/{organization_node_id}", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == organization_node_id
    assert body["node_code"] == "API-NODE-008"
    assert body["legal_entity_name"] == "API View Legal Entity"


def test_get_organization_node_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.get(
        f"/organization-nodes/{uuid.uuid4()}",
        headers=_auth_headers(),
    )

    assert response.status_code == 404


def test_get_organization_node_requires_authorization_header(client: TestClient) -> None:
    response = client.get(f"/organization-nodes/{uuid.uuid4()}")

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_get_organization_node_rejects_invalid_token(client: TestClient) -> None:
    response = client.get(
        f"/organization-nodes/{uuid.uuid4()}",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401


def test_get_organization_node_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.get(
        f"/organization-nodes/{uuid.uuid4()}",
        headers=_auth_headers(role_code="ORG_ADMIN"),
    )

    assert response.status_code == 403


def test_get_organization_node_rejects_invalid_uuid(client: TestClient) -> None:
    response = client.get("/organization-nodes/not-a-uuid", headers=_auth_headers())

    assert response.status_code == 422


def test_get_organization_node_does_not_require_tenant_header(client: TestClient) -> None:
    """
    GET /organization-nodes/{id} is tenant-agnostic (middleware/tenant.py's
    prefix exemption for /organization-nodes/*), same basis as Establish
    Organization Node. No X-Tenant-ID header sent; a 404 (not 400) proves
    the request reached the handler rather than being blocked by the
    tenant-header check.
    """
    response = client.get(
        f"/organization-nodes/{uuid.uuid4()}",
        headers=_auth_headers(),
    )

    assert response.status_code == 404
