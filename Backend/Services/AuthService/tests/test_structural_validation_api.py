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


def _seed_resolved_review(client: TestClient, proposal_id: str) -> str:
    created = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "review_position": "Supportive."},
    )
    assert created.status_code == 201
    review_id = created.json()["id"]
    resolved = client.post(f"/structural-reviews/{review_id}/resolve-concerns", headers=_auth_headers(), json={})
    assert resolved.status_code == 200
    return review_id


def test_validate_transition_readiness_succeeds_for_platform_admin(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-VALIDATE-NODE-001")
    review_id = _seed_resolved_review(client, proposal_id)

    response = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": proposal_id,
            "structural_review_id": review_id,
            "readiness_notes": "All concerns resolved; ready.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["structural_proposal_id"] == proposal_id
    assert body["structural_review_id"] == review_id
    assert body["status"] == "CREATED"


def test_validate_transition_readiness_allows_notes_to_be_omitted(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-VALIDATE-NODE-002")
    review_id = _seed_resolved_review(client, proposal_id)

    response = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "structural_review_id": review_id},
    )

    assert response.status_code == 201
    assert response.json()["readiness_notes"] is None


def test_validate_transition_readiness_rejects_unknown_proposal(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-VALIDATE-NODE-003")
    review_id = _seed_resolved_review(client, proposal_id)

    response = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": "99999999-9999-9999-9999-999999999999",
            "structural_review_id": review_id,
        },
    )

    assert response.status_code == 404


def test_validate_transition_readiness_rejects_unknown_review(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-VALIDATE-NODE-004")

    response = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": proposal_id,
            "structural_review_id": "99999999-9999-9999-9999-999999999999",
        },
    )

    assert response.status_code == 404


def test_validate_transition_readiness_rejects_review_for_a_different_proposal(client: TestClient) -> None:
    proposal_one = _seed_proposal(client, "API-VALIDATE-NODE-005")
    proposal_two = _seed_proposal(client, "API-VALIDATE-NODE-006")
    review_of_proposal_two = _seed_resolved_review(client, proposal_two)

    response = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_one, "structural_review_id": review_of_proposal_two},
    )

    assert response.status_code == 409


def test_validate_transition_readiness_rejects_unresolved_concerns(client: TestClient) -> None:
    """Mandatory business rule: BR-C005-007 hard-enforced at the API layer."""
    proposal_id = _seed_proposal(client, "API-VALIDATE-NODE-007")
    created = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "review_position": "Pending review."},
    )
    review_id = created.json()["id"]

    response = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "structural_review_id": review_id},
    )

    assert response.status_code == 409
    assert "BR-C005-007" in response.json()["detail"]


def test_validate_transition_readiness_requires_authorization_header(client: TestClient) -> None:
    response = client.post(
        "/structural-validations",
        json={
            "structural_proposal_id": "99999999-9999-9999-9999-999999999999",
            "structural_review_id": "99999999-9999-9999-9999-999999999999",
        },
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_validate_transition_readiness_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.post(
        "/structural-validations",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={
            "structural_proposal_id": "99999999-9999-9999-9999-999999999999",
            "structural_review_id": "99999999-9999-9999-9999-999999999999",
        },
    )

    assert response.status_code == 403


def test_validate_transition_readiness_rejects_missing_required_field(client: TestClient) -> None:
    response = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={"readiness_notes": "Missing proposal and review ids."},
    )

    assert response.status_code == 422


def test_validate_transition_readiness_does_not_require_tenant_header(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-VALIDATE-NODE-008")
    review_id = _seed_resolved_review(client, proposal_id)

    response = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "structural_review_id": review_id},
    )

    assert response.status_code == 201
