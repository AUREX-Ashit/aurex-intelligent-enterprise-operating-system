import uuid
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.organization import Organization


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


# ---------------------------------------------------------------------------
# BA-02 — View Organization Details
# ---------------------------------------------------------------------------

def test_view_organization_returns_details_for_platform_admin(client: TestClient) -> None:
    established = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={
            "organization_code": "API-ORG-007",
            "organization_name": "API View Org",
            "organization_type": "CORPORATE",
            "description": "Created for the view test.",
        },
    )
    assert established.status_code == 201
    organization_id = established.json()["id"]

    response = client.get(f"/organizations/{organization_id}", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == organization_id
    assert body["organization_code"] == "API-ORG-007"
    assert body["description"] == "Created for the view test."
    assert body["status"] == "ACTIVE"


def test_view_organization_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.get(
        f"/organizations/{uuid.uuid4()}",
        headers=_auth_headers(),
    )

    assert response.status_code == 404


def test_view_organization_requires_authorization_header(client: TestClient) -> None:
    response = client.get(f"/organizations/{uuid.uuid4()}")

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_view_organization_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.get(
        f"/organizations/{uuid.uuid4()}",
        headers=_auth_headers(role_code="ORG_ADMIN"),
    )

    assert response.status_code == 403


def test_view_organization_rejects_invalid_uuid(client: TestClient) -> None:
    response = client.get("/organizations/not-a-uuid", headers=_auth_headers())

    assert response.status_code == 422


def test_view_organization_does_not_require_tenant_header(client: TestClient) -> None:
    """
    GET /organizations/{id} is tenant-agnostic (middleware/tenant.py's
    prefix exemption for /organizations/*), same basis as Establish
    Organization. No X-Tenant-ID header sent; a 404 (not 400) proves the
    request reached the handler rather than being blocked by the
    tenant-header check.
    """
    response = client.get(
        f"/organizations/{uuid.uuid4()}",
        headers=_auth_headers(),
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# BA-04 — Update Organization Profile
# ---------------------------------------------------------------------------

def test_update_organization_succeeds_for_platform_admin(client: TestClient) -> None:
    established = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={
            "organization_code": "API-ORG-008",
            "organization_name": "Original Org",
            "organization_type": "CORPORATE",
            "description": "Before update.",
        },
    )
    assert established.status_code == 201
    organization_id = established.json()["id"]

    response = client.put(
        f"/organizations/{organization_id}",
        headers=_auth_headers(),
        json={
            "organization_name": "Updated Org",
            "organization_type": "SUBSIDIARY",
            "description": "After update.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == organization_id
    assert body["organization_code"] == "API-ORG-008"
    assert body["organization_name"] == "Updated Org"
    assert body["organization_type"] == "SUBSIDIARY"
    assert body["description"] == "After update."
    assert body["status"] == "ACTIVE"


def test_update_organization_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.put(
        f"/organizations/{uuid.uuid4()}",
        headers=_auth_headers(),
        json={"organization_name": "Ghost Org", "organization_type": "CORPORATE"},
    )

    assert response.status_code == 404


def test_update_organization_requires_authorization_header(client: TestClient) -> None:
    response = client.put(
        f"/organizations/{uuid.uuid4()}",
        json={"organization_name": "Ghost Org", "organization_type": "CORPORATE"},
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_update_organization_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.put(
        f"/organizations/{uuid.uuid4()}",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={"organization_name": "Ghost Org", "organization_type": "CORPORATE"},
    )

    assert response.status_code == 403


def test_update_organization_rejects_missing_required_field(client: TestClient) -> None:
    established = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={"organization_code": "API-ORG-009", "organization_name": "Org", "organization_type": "CORPORATE"},
    )
    organization_id = established.json()["id"]

    response = client.put(
        f"/organizations/{organization_id}",
        headers=_auth_headers(),
        json={"organization_type": "CORPORATE"},
    )

    assert response.status_code == 422


def test_update_organization_rejects_empty_required_field(client: TestClient) -> None:
    established = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={"organization_code": "API-ORG-010", "organization_name": "Org", "organization_type": "CORPORATE"},
    )
    organization_id = established.json()["id"]

    response = client.put(
        f"/organizations/{organization_id}",
        headers=_auth_headers(),
        json={"organization_name": "", "organization_type": "CORPORATE"},
    )

    assert response.status_code == 422


def test_update_organization_does_not_accept_organization_code_change(client: TestClient) -> None:
    """
    organization_code is not a field on UpdateOrganizationProfileRequest —
    sending it is silently ignored by Pydantic (extra fields dropped by
    default), proving the immutable natural key cannot be changed through
    this endpoint.
    """
    established = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={"organization_code": "API-ORG-011", "organization_name": "Org", "organization_type": "CORPORATE"},
    )
    organization_id = established.json()["id"]

    response = client.put(
        f"/organizations/{organization_id}",
        headers=_auth_headers(),
        json={"organization_code": "SHOULD-NOT-APPLY", "organization_name": "Renamed Org", "organization_type": "CORPORATE"},
    )

    assert response.status_code == 200
    assert response.json()["organization_code"] == "API-ORG-011"


def test_update_organization_rejects_invalid_uuid(client: TestClient) -> None:
    response = client.put(
        "/organizations/not-a-uuid",
        headers=_auth_headers(),
        json={"organization_name": "Org", "organization_type": "CORPORATE"},
    )

    assert response.status_code == 422


def test_update_organization_does_not_require_tenant_header(client: TestClient) -> None:
    """PUT /organizations/{id} is covered by the same /organizations/* prefix exemption as GET."""
    established = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={"organization_code": "API-ORG-012", "organization_name": "Org", "organization_type": "CORPORATE"},
    )
    organization_id = established.json()["id"]

    response = client.put(
        f"/organizations/{organization_id}",
        headers=_auth_headers(),
        json={"organization_name": "Org Renamed", "organization_type": "CORPORATE"},
    )

    assert response.status_code == 200


# ---------------------------------------------------------------------------
# BA-05 — Activate Organization
# ---------------------------------------------------------------------------

async def test_activate_organization_succeeds_for_platform_admin(
    client: TestClient, db_session: AsyncSession
) -> None:
    """
    No Suspend Business Activity exists yet (BA-06), so the SUSPENDED
    starting state is seeded directly via the shared test db_session
    (the same session TestClient's dependency override uses — see
    test_health.py's test_ready_reports_ready_after_bootstrap for the
    existing precedent of mixing these two fixtures), not through a
    public API endpoint.
    """
    established = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={"organization_code": "API-ORG-013", "organization_name": "Suspended Org", "organization_type": "CORPORATE"},
    )
    organization_id = established.json()["id"]

    organization = await db_session.get(Organization, uuid.UUID(organization_id))
    organization.status = "SUSPENDED"
    await db_session.flush()

    response = client.post(f"/organizations/{organization_id}/activate", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == organization_id
    assert body["status"] == "ACTIVE"


def test_activate_organization_rejects_already_active(client: TestClient) -> None:
    established = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={"organization_code": "API-ORG-014", "organization_name": "Already Active Org", "organization_type": "CORPORATE"},
    )
    organization_id = established.json()["id"]

    response = client.post(f"/organizations/{organization_id}/activate", headers=_auth_headers())

    assert response.status_code == 409


def test_activate_organization_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.post(f"/organizations/{uuid.uuid4()}/activate", headers=_auth_headers())

    assert response.status_code == 404


def test_activate_organization_requires_authorization_header(client: TestClient) -> None:
    response = client.post(f"/organizations/{uuid.uuid4()}/activate")

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_activate_organization_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.post(
        f"/organizations/{uuid.uuid4()}/activate",
        headers=_auth_headers(role_code="ORG_ADMIN"),
    )

    assert response.status_code == 403


def test_activate_organization_rejects_invalid_uuid(client: TestClient) -> None:
    response = client.post("/organizations/not-a-uuid/activate", headers=_auth_headers())

    assert response.status_code == 422


def test_activate_organization_does_not_require_tenant_header(client: TestClient) -> None:
    """PUT/POST /organizations/{id}/* is covered by the same /organizations/* prefix exemption as GET."""
    established = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={"organization_code": "API-ORG-015", "organization_name": "Org", "organization_type": "CORPORATE"},
    )
    organization_id = established.json()["id"]

    # Already ACTIVE -> 409, but a 409 (not 400) proves the request reached
    # the handler rather than being blocked by the tenant-header check.
    response = client.post(f"/organizations/{organization_id}/activate", headers=_auth_headers())

    assert response.status_code == 409


# ---------------------------------------------------------------------------
# BA-03 — Search & List Organizations
# ---------------------------------------------------------------------------

def _establish(client: TestClient, code: str, name: str) -> dict:
    response = client.post(
        "/organizations",
        headers=_auth_headers(),
        json={"organization_code": code, "organization_name": name, "organization_type": "CORPORATE"},
    )
    assert response.status_code == 201
    return response.json()


def test_search_organizations_returns_a_page_with_total(client: TestClient) -> None:
    _establish(client, "LIST-001", "List Org One")
    _establish(client, "LIST-002", "List Org Two")

    response = client.get("/organizations", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 2
    assert body["skip"] == 0
    assert body["limit"] == 20
    codes = {item["organization_code"] for item in body["items"]}
    assert "LIST-001" in codes and "LIST-002" in codes


def test_search_organizations_filters_by_query_text(client: TestClient) -> None:
    _establish(client, "QRY-001", "Zephyr Industries")
    _establish(client, "QRY-002", "Marble Holdings")

    response = client.get("/organizations", headers=_auth_headers(), params={"q": "zephyr"})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["organization_code"] == "QRY-001"


def test_search_organizations_filters_by_status(client: TestClient) -> None:
    _establish(client, "STAT-001", "Status Org")

    response = client.get("/organizations", headers=_auth_headers(), params={"status": "SUSPENDED"})

    assert response.status_code == 200
    body = response.json()
    assert all(item["status"] == "SUSPENDED" for item in body["items"])


def test_search_organizations_respects_pagination_params(client: TestClient) -> None:
    for i in range(3):
        _establish(client, f"PG-{i:03d}", f"Pagination Org {i}")

    response = client.get(
        "/organizations",
        headers=_auth_headers(),
        params={"q": "Pagination Org", "skip": 1, "limit": 1, "sort_by": "organization_code", "sort_order": "asc"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert body["skip"] == 1
    assert body["limit"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["organization_code"] == "PG-001"


def test_search_organizations_rejects_limit_over_100(client: TestClient) -> None:
    response = client.get("/organizations", headers=_auth_headers(), params={"limit": 101})

    assert response.status_code == 422


def test_search_organizations_rejects_negative_skip(client: TestClient) -> None:
    response = client.get("/organizations", headers=_auth_headers(), params={"skip": -1})

    assert response.status_code == 422


def test_search_organizations_rejects_invalid_sort_by(client: TestClient) -> None:
    response = client.get("/organizations", headers=_auth_headers(), params={"sort_by": "not_a_real_field"})

    assert response.status_code == 422


def test_search_organizations_requires_authorization_header(client: TestClient) -> None:
    response = client.get("/organizations")

    assert response.status_code == 400


def test_search_organizations_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.get("/organizations", headers=_auth_headers(role_code="ORG_ADMIN"))

    assert response.status_code == 403


def test_search_organizations_does_not_require_tenant_header(client: TestClient) -> None:
    """GET /organizations (exact-match exemption, unchanged since BA-01) is tenant-agnostic."""
    response = client.get("/organizations", headers=_auth_headers())

    assert response.status_code == 200
