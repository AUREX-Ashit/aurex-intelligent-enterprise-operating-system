from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt

from config import settings


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
    """
    Builds a signed access token with the given role_code claim, bypassing
    a real /auth/login round-trip — this test module is exercising Frame
    Structural Change Intent's authorization dependency, not the login
    flow. Mirrors test_organization_node_api.py's own _access_token
    helper exactly.
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


def test_frame_structural_change_intent_succeeds_for_platform_admin(client: TestClient) -> None:
    response = client.post(
        "/structural-change-intents",
        headers=_auth_headers(),
        json={
            "change_rationale": "APAC Holding's reporting structure no longer reflects the post-acquisition entity footprint.",
            "target_outcome": "Consolidate the three newly-acquired APAC entities under a single regional holding node.",
            "decision_boundary": "Must not alter any existing EU or Americas structural relationships.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["change_rationale"] == "APAC Holding's reporting structure no longer reflects the post-acquisition entity footprint."
    assert body["target_outcome"] == "Consolidate the three newly-acquired APAC entities under a single regional holding node."
    assert body["decision_boundary"] == "Must not alter any existing EU or Americas structural relationships."
    assert body["status"] == "CREATED"
    assert "id" in body


def test_frame_structural_change_intent_allows_decision_boundary_to_be_omitted(client: TestClient) -> None:
    response = client.post(
        "/structural-change-intents",
        headers=_auth_headers(),
        json={
            "change_rationale": "Observed structural gap.",
            "target_outcome": "Target structural outcome.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["decision_boundary"] is None


def test_frame_structural_change_intent_requires_authorization_header(client: TestClient) -> None:
    """No Authorization header at all -> 400, per dependencies.get_current_claims."""
    response = client.post(
        "/structural-change-intents",
        json={
            "change_rationale": "Observed structural gap.",
            "target_outcome": "Target structural outcome.",
        },
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_frame_structural_change_intent_rejects_invalid_token(client: TestClient) -> None:
    response = client.post(
        "/structural-change-intents",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={
            "change_rationale": "Observed structural gap.",
            "target_outcome": "Target structural outcome.",
        },
    )

    assert response.status_code == 401


def test_frame_structural_change_intent_rejects_non_platform_admin_role(client: TestClient) -> None:
    """Only PLATFORM_ADMIN may frame a structural change intent (same interim gate as every prior Business Activity)."""
    response = client.post(
        "/structural-change-intents",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={
            "change_rationale": "Observed structural gap.",
            "target_outcome": "Target structural outcome.",
        },
    )

    assert response.status_code == 403


def test_frame_structural_change_intent_rejects_missing_required_field(client: TestClient) -> None:
    response = client.post(
        "/structural-change-intents",
        headers=_auth_headers(),
        json={"decision_boundary": "Missing rationale and target outcome."},
    )

    assert response.status_code == 422


def test_frame_structural_change_intent_rejects_empty_required_field(client: TestClient) -> None:
    response = client.post(
        "/structural-change-intents",
        headers=_auth_headers(),
        json={
            "change_rationale": "",
            "target_outcome": "Target structural outcome.",
        },
    )

    assert response.status_code == 422


def test_frame_structural_change_intent_does_not_require_tenant_header(client: TestClient) -> None:
    """
    POST /structural-change-intents is tenant-agnostic (middleware/tenant.
    py's exemption list) — StructuralChangeIntent carries no
    organization_id column. No X-Tenant-ID header is sent here at all; if
    TenantMiddleware were not exempting this path, this would fail with
    400 instead of 201.
    """
    response = client.post(
        "/structural-change-intents",
        headers=_auth_headers(),
        json={
            "change_rationale": "Observed structural gap.",
            "target_outcome": "Target structural outcome.",
        },
    )

    assert response.status_code == 201


def test_frame_structural_change_intent_does_not_deduplicate_identical_requests(client: TestClient) -> None:
    """Deliberate difference from Establish Organization Node: no 409 for a repeated identical request."""
    payload = {
        "change_rationale": "Observed structural gap.",
        "target_outcome": "Target structural outcome.",
    }
    first = client.post("/structural-change-intents", headers=_auth_headers(), json=payload)
    second = client.post("/structural-change-intents", headers=_auth_headers(), json=payload)

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]
