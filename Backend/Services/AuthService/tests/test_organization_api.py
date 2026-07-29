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


def _establish_and_activate(
    client: TestClient,
    organization_code: str,
    organization_name: str,
    organization_type: str = "CORPORATE",
    description: str | None = None,
) -> dict:
    """
    Test-only helper (IRA-001A): BA-02 through BA-07's own API tests need
    a real, ACTIVE Organization to exercise against — POST /organizations
    no longer exists (establishment moved to
    POST /organization-establishment-attempts, BR-C004-01). Establishes
    an attempt, then activates it via the governed no-domain path, and
    returns the resulting Organization response body unchanged in shape
    from every downstream test's own assertions.
    """
    established = client.post(
        "/organization-establishment-attempts",
        headers=_auth_headers(),
        json={
            "organization_code": organization_code,
            "organization_name": organization_name,
            "organization_type": organization_type,
            "description": description,
        },
    )
    assert established.status_code == 201
    attempt_id = established.json()["id"]

    activated = client.post(
        f"/organization-establishment-attempts/{attempt_id}/activate",
        headers=_auth_headers(),
        json={"no_domain_activation_reason": "Test fixture: no domain to claim."},
    )
    assert activated.status_code == 201
    return activated.json()


# ---------------------------------------------------------------------------
# BA-01 — Establish Organization Identity (amended, IRA-001A)
# ---------------------------------------------------------------------------

def test_establish_organization_creates_attempt_not_organization(client: TestClient) -> None:
    response = client.post(
        "/organization-establishment-attempts",
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
    assert body["domain_verification_status"] == "NOT_CLAIMED"
    assert body["activated_organization_id"] is None
    assert "id" in body
    assert "status" not in body


def test_establish_organization_rejects_duplicate_code(client: TestClient) -> None:
    payload = {
        "organization_code": "API-ORG-002",
        "organization_name": "API Test Org",
        "organization_type": "CORPORATE",
    }
    first = client.post("/organization-establishment-attempts", headers=_auth_headers(), json=payload)
    assert first.status_code == 201

    second = client.post("/organization-establishment-attempts", headers=_auth_headers(), json=payload)
    assert second.status_code == 409


def test_establish_organization_requires_authorization_header(client: TestClient) -> None:
    """No Authorization header at all -> 400, per dependencies.get_current_claims."""
    response = client.post(
        "/organization-establishment-attempts",
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
        "/organization-establishment-attempts",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={
            "organization_code": "API-ORG-004",
            "organization_name": "API Test Org",
            "organization_type": "CORPORATE",
        },
    )

    assert response.status_code == 401


def test_establish_organization_rejects_non_platform_admin_role(client: TestClient) -> None:
    """IRA-001 §2.7: only PLATFORM_ADMIN may establish an organization establishment attempt."""
    response = client.post(
        "/organization-establishment-attempts",
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
        "/organization-establishment-attempts",
        headers=_auth_headers(),
        json={"organization_name": "Missing Code Org", "organization_type": "CORPORATE"},
    )

    assert response.status_code == 422


def test_establish_organization_rejects_empty_required_field(client: TestClient) -> None:
    response = client.post(
        "/organization-establishment-attempts",
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
    POST /organization-establishment-attempts is tenant-agnostic
    (middleware/tenant.py's exemption list) — an establishment attempt has
    no organization_id column at all. No X-Tenant-ID header is sent here;
    if TenantMiddleware were not exempting this path, this would fail with
    400 instead of 201.
    """
    response = client.post(
        "/organization-establishment-attempts",
        headers=_auth_headers(),
        json={
            "organization_code": "API-ORG-006",
            "organization_name": "API Test Org",
            "organization_type": "CORPORATE",
        },
    )

    assert response.status_code == 201


# ---------------------------------------------------------------------------
# BA-01B — Verify Organization Domain Claim (new, IRA-001A)
# ---------------------------------------------------------------------------

def test_verify_domain_claim_succeeds_for_platform_admin(client: TestClient) -> None:
    established = client.post(
        "/organization-establishment-attempts",
        headers=_auth_headers(),
        json={
            "organization_code": "API-ORG-010",
            "organization_name": "API Domain Org",
            "organization_type": "CORPORATE",
            "primary_domain": "api-domain-org.example",
        },
    )
    attempt_id = established.json()["id"]

    response = client.post(
        f"/organization-establishment-attempts/{attempt_id}/verify-domain",
        headers=_auth_headers(),
        json={"verified": True},
    )

    assert response.status_code == 200
    assert response.json()["domain_verification_status"] == "VERIFIED"


def test_verify_domain_claim_returns_404_for_unknown_attempt(client: TestClient) -> None:
    response = client.post(
        f"/organization-establishment-attempts/{uuid.uuid4()}/verify-domain",
        headers=_auth_headers(),
        json={"verified": True},
    )

    assert response.status_code == 404


def test_verify_domain_claim_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.post(
        f"/organization-establishment-attempts/{uuid.uuid4()}/verify-domain",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={"verified": True},
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# BA-01C — Activate Organization, first-time (new, IRA-001A)
# ---------------------------------------------------------------------------

def test_activate_establishment_with_no_domain_reason_creates_active_organization(client: TestClient) -> None:
    established = client.post(
        "/organization-establishment-attempts",
        headers=_auth_headers(),
        json={
            "organization_code": "API-ORG-020",
            "organization_name": "API Activated Org",
            "organization_type": "CORPORATE",
        },
    )
    attempt_id = established.json()["id"]

    response = client.post(
        f"/organization-establishment-attempts/{attempt_id}/activate",
        headers=_auth_headers(),
        json={"no_domain_activation_reason": "No domain to claim."},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["organization_code"] == "API-ORG-020"
    assert body["status"] == "ACTIVE"
    assert body["is_active"] is True


def test_activate_establishment_rejects_without_verification_or_reason(client: TestClient) -> None:
    established = client.post(
        "/organization-establishment-attempts",
        headers=_auth_headers(),
        json={
            "organization_code": "API-ORG-021",
            "organization_name": "API Blocked Org",
            "organization_type": "CORPORATE",
            "primary_domain": "api-blocked-org.example",
        },
    )
    attempt_id = established.json()["id"]

    response = client.post(
        f"/organization-establishment-attempts/{attempt_id}/activate",
        headers=_auth_headers(),
        json={},
    )

    assert response.status_code == 409


def test_activate_establishment_returns_404_for_unknown_attempt(client: TestClient) -> None:
    response = client.post(
        f"/organization-establishment-attempts/{uuid.uuid4()}/activate",
        headers=_auth_headers(),
        json={"no_domain_activation_reason": "x"},
    )

    assert response.status_code == 404


def test_activate_establishment_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.post(
        f"/organization-establishment-attempts/{uuid.uuid4()}/activate",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={"no_domain_activation_reason": "x"},
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# BA-02 — View Organization Details
# ---------------------------------------------------------------------------

def test_view_organization_returns_details_for_platform_admin(client: TestClient) -> None:
    organization_id = _establish_and_activate(
        client, "API-ORG-007", "API View Org", "CORPORATE", description="Created for the view test."
    )["id"]

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
    organization_id = _establish_and_activate(
        client, "API-ORG-008", "Original Org", "CORPORATE", description="Before update."
    )["id"]

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
    organization_id = _establish_and_activate(client, "API-ORG-009", "Org", "CORPORATE")["id"]

    response = client.put(
        f"/organizations/{organization_id}",
        headers=_auth_headers(),
        json={"organization_type": "CORPORATE"},
    )

    assert response.status_code == 422


def test_update_organization_rejects_empty_required_field(client: TestClient) -> None:
    organization_id = _establish_and_activate(client, "API-ORG-010", "Org", "CORPORATE")["id"]

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
    organization_id = _establish_and_activate(client, "API-ORG-011", "Org", "CORPORATE")["id"]

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
    organization_id = _establish_and_activate(client, "API-ORG-012", "Org", "CORPORATE")["id"]

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
    organization_id = _establish_and_activate(client, "API-ORG-013", "Suspended Org", "CORPORATE")["id"]

    organization = await db_session.get(Organization, uuid.UUID(organization_id))
    organization.status = "SUSPENDED"
    await db_session.flush()

    response = client.post(f"/organizations/{organization_id}/activate", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == organization_id
    assert body["status"] == "ACTIVE"


def test_activate_organization_rejects_already_active(client: TestClient) -> None:
    organization_id = _establish_and_activate(client, "API-ORG-014", "Already Active Org", "CORPORATE")["id"]

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
    organization_id = _establish_and_activate(client, "API-ORG-015", "Org", "CORPORATE")["id"]

    # Already ACTIVE -> 409, but a 409 (not 400) proves the request reached
    # the handler rather than being blocked by the tenant-header check.
    response = client.post(f"/organizations/{organization_id}/activate", headers=_auth_headers())

    assert response.status_code == 409


# ---------------------------------------------------------------------------
# BA-06 — Suspend Organization
# ---------------------------------------------------------------------------

def test_suspend_organization_succeeds_for_platform_admin(client: TestClient) -> None:
    organization_id = _establish_and_activate(client, "API-ORG-016", "Active Org", "CORPORATE")["id"]

    response = client.post(f"/organizations/{organization_id}/suspend", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == organization_id
    assert body["status"] == "SUSPENDED"


def test_suspend_organization_rejects_already_suspended(client: TestClient) -> None:
    organization_id = _establish_and_activate(client, "API-ORG-017", "Org", "CORPORATE")["id"]
    first = client.post(f"/organizations/{organization_id}/suspend", headers=_auth_headers())
    assert first.status_code == 200

    second = client.post(f"/organizations/{organization_id}/suspend", headers=_auth_headers())

    assert second.status_code == 409


def test_suspend_organization_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.post(f"/organizations/{uuid.uuid4()}/suspend", headers=_auth_headers())

    assert response.status_code == 404


def test_suspend_organization_requires_authorization_header(client: TestClient) -> None:
    response = client.post(f"/organizations/{uuid.uuid4()}/suspend")

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_suspend_organization_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.post(
        f"/organizations/{uuid.uuid4()}/suspend",
        headers=_auth_headers(role_code="ORG_ADMIN"),
    )

    assert response.status_code == 403


def test_suspend_organization_rejects_invalid_uuid(client: TestClient) -> None:
    response = client.post("/organizations/not-a-uuid/suspend", headers=_auth_headers())

    assert response.status_code == 422


def test_suspend_organization_does_not_require_tenant_header(client: TestClient) -> None:
    """POST /organizations/{id}/suspend is covered by the same /organizations/* prefix exemption as GET."""
    organization_id = _establish_and_activate(client, "API-ORG-018", "Org", "CORPORATE")["id"]

    response = client.post(f"/organizations/{organization_id}/suspend", headers=_auth_headers())

    assert response.status_code == 200


def test_suspend_then_activate_round_trip_keeps_is_active_in_sync(client: TestClient) -> None:
    """
    TD-012 resolution, exercised end-to-end through the HTTP API: suspend
    sets is_active False, a subsequent activate sets it back to True.
    """
    established = _establish_and_activate(client, "API-ORG-019", "Org", "CORPORATE")
    organization_id = established["id"]
    assert established["is_active"] is True

    suspended = client.post(f"/organizations/{organization_id}/suspend", headers=_auth_headers())
    assert suspended.status_code == 200
    assert suspended.json()["is_active"] is False

    activated = client.post(f"/organizations/{organization_id}/activate", headers=_auth_headers())
    assert activated.status_code == 200
    assert activated.json()["is_active"] is True


# ---------------------------------------------------------------------------
# BA-07 — Retire Organization & Preserve Continuity
# ---------------------------------------------------------------------------

def test_retire_organization_succeeds_for_platform_admin(client: TestClient) -> None:
    organization_id = _establish_and_activate(client, "API-ORG-020", "Active Org", "CORPORATE")["id"]

    response = client.post(f"/organizations/{organization_id}/retire", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == organization_id
    assert body["status"] == "RETIRED"
    assert body["is_active"] is False


def test_retire_organization_succeeds_from_suspended(client: TestClient) -> None:
    """ERB-C004-07 Entry Context: retirement is also valid directly from SUSPENDED, not only ACTIVE."""
    organization_id = _establish_and_activate(client, "API-ORG-021", "Org", "CORPORATE")["id"]
    suspend_response = client.post(f"/organizations/{organization_id}/suspend", headers=_auth_headers())
    assert suspend_response.status_code == 200

    response = client.post(f"/organizations/{organization_id}/retire", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["status"] == "RETIRED"


def test_retire_organization_rejects_already_retired(client: TestClient) -> None:
    organization_id = _establish_and_activate(client, "API-ORG-022", "Org", "CORPORATE")["id"]
    first = client.post(f"/organizations/{organization_id}/retire", headers=_auth_headers())
    assert first.status_code == 200

    second = client.post(f"/organizations/{organization_id}/retire", headers=_auth_headers())

    assert second.status_code == 409


def test_retire_organization_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.post(f"/organizations/{uuid.uuid4()}/retire", headers=_auth_headers())

    assert response.status_code == 404


def test_retire_organization_requires_authorization_header(client: TestClient) -> None:
    response = client.post(f"/organizations/{uuid.uuid4()}/retire")

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_retire_organization_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.post(
        f"/organizations/{uuid.uuid4()}/retire",
        headers=_auth_headers(role_code="ORG_ADMIN"),
    )

    assert response.status_code == 403


def test_retire_organization_rejects_invalid_uuid(client: TestClient) -> None:
    response = client.post("/organizations/not-a-uuid/retire", headers=_auth_headers())

    assert response.status_code == 422


def test_retire_organization_does_not_require_tenant_header(client: TestClient) -> None:
    """POST /organizations/{id}/retire is covered by the same /organizations/* prefix exemption as GET."""
    organization_id = _establish_and_activate(client, "API-ORG-023", "Org", "CORPORATE")["id"]

    response = client.post(f"/organizations/{organization_id}/retire", headers=_auth_headers())

    assert response.status_code == 200


def test_activate_organization_rejects_retired_organization(client: TestClient) -> None:
    """Irreversibility invariant (PE-001-C004 §3.8), exercised through the HTTP API."""
    organization_id = _establish_and_activate(client, "API-ORG-024", "Org", "CORPORATE")["id"]
    retire_response = client.post(f"/organizations/{organization_id}/retire", headers=_auth_headers())
    assert retire_response.status_code == 200

    response = client.post(f"/organizations/{organization_id}/activate", headers=_auth_headers())

    assert response.status_code == 409
    # Confirm the organization did not silently flip back to ACTIVE.
    details = client.get(f"/organizations/{organization_id}", headers=_auth_headers())
    assert details.json()["status"] == "RETIRED"


def test_suspend_organization_rejects_retired_organization(client: TestClient) -> None:
    """Same irreversibility invariant, exercised against /suspend instead of /activate."""
    organization_id = _establish_and_activate(client, "API-ORG-025", "Org", "CORPORATE")["id"]
    retire_response = client.post(f"/organizations/{organization_id}/retire", headers=_auth_headers())
    assert retire_response.status_code == 200

    response = client.post(f"/organizations/{organization_id}/suspend", headers=_auth_headers())

    assert response.status_code == 409
    details = client.get(f"/organizations/{organization_id}", headers=_auth_headers())
    assert details.json()["status"] == "RETIRED"


def test_view_organization_still_returns_retired_organization_details(client: TestClient) -> None:
    """Continuity requirement: retirement SHALL NOT physically delete the Organization."""
    organization_id = _establish_and_activate(
        client, "API-ORG-026", "Preserved Org", "CORPORATE", description="Should survive retirement."
    )["id"]
    retire_response = client.post(f"/organizations/{organization_id}/retire", headers=_auth_headers())
    assert retire_response.status_code == 200

    response = client.get(f"/organizations/{organization_id}", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["organization_code"] == "API-ORG-026"
    assert body["organization_name"] == "Preserved Org"
    assert body["description"] == "Should survive retirement."
    assert body["status"] == "RETIRED"


def test_search_organizations_can_filter_by_retired_status(client: TestClient) -> None:
    """A RETIRED organization is still discoverable via Search & List — not hidden or deleted."""
    organization_id = _establish_and_activate(client, "API-ORG-027", "Findable Retired Org", "CORPORATE")["id"]
    retire_response = client.post(f"/organizations/{organization_id}/retire", headers=_auth_headers())
    assert retire_response.status_code == 200

    response = client.get("/organizations", headers=_auth_headers(), params={"status": "RETIRED", "q": "API-ORG-027"})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["organization_code"] == "API-ORG-027"


# ---------------------------------------------------------------------------
# BA-03 — Search & List Organizations
# ---------------------------------------------------------------------------

def _establish(client: TestClient, code: str, name: str) -> dict:
    return _establish_and_activate(client, code, name, "CORPORATE")


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


def test_search_organizations_status_filter_includes_and_excludes_mixed_statuses(client: TestClient) -> None:
    """
    TD-008 resolution, exercised end-to-end through the HTTP API: with
    Suspend Organization (BA-06) now available, prove the status filter
    correctly includes a SUSPENDED organization and excludes it from the
    ACTIVE filter, against a real mixed-status dataset.
    """
    active_org = _establish(client, "STAT-MIX-001", "Still Active Org")
    suspended_org = _establish(client, "STAT-MIX-002", "To Be Suspended Org")
    suspend_response = client.post(f"/organizations/{suspended_org['id']}/suspend", headers=_auth_headers())
    assert suspend_response.status_code == 200

    active_response = client.get(
        "/organizations", headers=_auth_headers(), params={"status": "ACTIVE", "q": "STAT-MIX"}
    )
    suspended_response = client.get(
        "/organizations", headers=_auth_headers(), params={"status": "SUSPENDED", "q": "STAT-MIX"}
    )

    active_codes = {item["organization_code"] for item in active_response.json()["items"]}
    suspended_codes = {item["organization_code"] for item in suspended_response.json()["items"]}
    assert active_codes == {active_org["organization_code"]}
    assert suspended_codes == {suspended_org["organization_code"]}


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
