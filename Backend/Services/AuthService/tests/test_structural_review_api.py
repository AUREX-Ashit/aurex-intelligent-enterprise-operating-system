from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt

from config import settings


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
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


def _seed_proposal(client: TestClient, node_code: str) -> str:
    intent = client.post(
        "/structural-change-intents",
        headers=_auth_headers(),
        json={"change_rationale": "Observed structural gap.", "target_outcome": "Target structural outcome."},
    )
    assert intent.status_code == 201
    node = client.post(
        "/organization-nodes",
        headers=_auth_headers(),
        json={"node_code": node_code, "node_name": "API Test Node", "node_type": "HOLDING"},
    )
    assert node.status_code == 201
    proposal = client.post(
        "/structural-proposals",
        headers=_auth_headers(),
        json={
            "structural_change_intent_id": intent.json()["id"],
            "target_organization_node_id": node.json()["id"],
            "proposed_outcome_description": "Consolidate under this holding node.",
        },
    )
    assert proposal.status_code == 201
    return proposal.json()["id"]


def test_create_structural_review_succeeds_for_platform_admin(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-REVIEW-NODE-001")

    response = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": proposal_id,
            "review_position": "Broadly supportive, pending confirmation.",
            "concerns": "Uncertain whether affected personnel require a home-node review.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["structural_proposal_id"] == proposal_id
    assert body["status"] == "CREATED"
    assert "id" in body


def test_create_structural_review_allows_concerns_to_be_omitted(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-REVIEW-NODE-002")

    response = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "review_position": "No concerns."},
    )

    assert response.status_code == 201
    assert response.json()["concerns"] is None


def test_create_structural_review_rejects_unknown_structural_proposal(client: TestClient) -> None:
    response = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": "99999999-9999-9999-9999-999999999999",
            "review_position": "No concerns.",
        },
    )

    assert response.status_code == 404


def test_create_structural_review_requires_authorization_header(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-REVIEW-NODE-003")

    response = client.post(
        "/structural-reviews",
        json={"structural_proposal_id": proposal_id, "review_position": "No concerns."},
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_create_structural_review_rejects_non_platform_admin_role(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-REVIEW-NODE-004")

    response = client.post(
        "/structural-reviews",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={"structural_proposal_id": proposal_id, "review_position": "No concerns."},
    )

    assert response.status_code == 403


def test_create_structural_review_rejects_missing_required_field(client: TestClient) -> None:
    response = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={"concerns": "Missing structural_proposal_id and review_position."},
    )

    assert response.status_code == 422


def test_create_structural_review_does_not_require_tenant_header(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-REVIEW-NODE-005")

    response = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "review_position": "No concerns."},
    )

    assert response.status_code == 201


def test_resolve_structural_review_concerns_succeeds(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-REVIEW-NODE-006")
    created = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": proposal_id,
            "review_position": "Broadly supportive.",
            "concerns": "Reporting currency mapping unconfirmed.",
        },
    )
    review_id = created.json()["id"]

    response = client.post(
        f"/structural-reviews/{review_id}/resolve-concerns",
        headers=_auth_headers(),
        json={"resolution_notes": "Confirmed with Finance; no change required."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "CONCERNS_RESOLVED"
    assert "Reporting currency mapping unconfirmed." in body["concerns"]
    assert "Confirmed with Finance; no change required." in body["concerns"]


def test_resolve_structural_review_concerns_rejects_unknown_review(client: TestClient) -> None:
    response = client.post(
        "/structural-reviews/99999999-9999-9999-9999-999999999999/resolve-concerns",
        headers=_auth_headers(),
        json={},
    )

    assert response.status_code == 404


def test_resolve_structural_review_concerns_rejects_already_resolved(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-REVIEW-NODE-007")
    created = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "review_position": "No concerns."},
    )
    review_id = created.json()["id"]
    first = client.post(f"/structural-reviews/{review_id}/resolve-concerns", headers=_auth_headers(), json={})
    assert first.status_code == 200

    second = client.post(f"/structural-reviews/{review_id}/resolve-concerns", headers=_auth_headers(), json={})

    assert second.status_code == 409


def test_resolve_structural_review_concerns_requires_authorization_header(client: TestClient) -> None:
    response = client.post(
        "/structural-reviews/99999999-9999-9999-9999-999999999999/resolve-concerns",
        json={},
    )

    assert response.status_code == 400


def test_resolve_structural_review_concerns_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.post(
        "/structural-reviews/99999999-9999-9999-9999-999999999999/resolve-concerns",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={},
    )

    assert response.status_code == 403


def test_resolve_structural_review_concerns_does_not_require_tenant_header(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-REVIEW-NODE-008")
    created = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "review_position": "No concerns."},
    )
    review_id = created.json()["id"]

    response = client.post(f"/structural-reviews/{review_id}/resolve-concerns", headers=_auth_headers(), json={})

    assert response.status_code == 200
