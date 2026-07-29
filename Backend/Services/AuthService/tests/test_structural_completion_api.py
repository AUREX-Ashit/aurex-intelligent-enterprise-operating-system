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


def _seed_validation(client: TestClient, node_code: str) -> str:
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
    proposal_id = proposal.json()["id"]
    review = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "review_position": "Supportive."},
    )
    assert review.status_code == 201
    review_id = review.json()["id"]
    resolved = client.post(f"/structural-reviews/{review_id}/resolve-concerns", headers=_auth_headers(), json={})
    assert resolved.status_code == 200
    validation = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "structural_review_id": review_id},
    )
    assert validation.status_code == 201
    return validation.json()["id"]


def test_complete_structural_transition_succeeds_for_platform_admin(client: TestClient) -> None:
    validation_id = _seed_validation(client, "API-COMPLETE-NODE-001")

    response = client.post(
        "/structural-completions",
        headers=_auth_headers(),
        json={
            "structural_validation_id": validation_id,
            "completion_notes": "Structural transition completed.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["structural_validation_id"] == validation_id
    assert body["status"] == "CREATED"


def test_complete_structural_transition_allows_notes_to_be_omitted(client: TestClient) -> None:
    validation_id = _seed_validation(client, "API-COMPLETE-NODE-002")

    response = client.post(
        "/structural-completions",
        headers=_auth_headers(),
        json={"structural_validation_id": validation_id},
    )

    assert response.status_code == 201
    assert response.json()["completion_notes"] is None


def test_complete_structural_transition_rejects_unknown_validation(client: TestClient) -> None:
    response = client.post(
        "/structural-completions",
        headers=_auth_headers(),
        json={"structural_validation_id": "99999999-9999-9999-9999-999999999999"},
    )

    assert response.status_code == 404


def test_complete_structural_transition_rejects_duplicate_completion(client: TestClient) -> None:
    validation_id = _seed_validation(client, "API-COMPLETE-NODE-003")
    first = client.post(
        "/structural-completions", headers=_auth_headers(), json={"structural_validation_id": validation_id}
    )
    assert first.status_code == 201

    second = client.post(
        "/structural-completions", headers=_auth_headers(), json={"structural_validation_id": validation_id}
    )

    assert second.status_code == 409


def test_complete_structural_transition_requires_authorization_header(client: TestClient) -> None:
    response = client.post(
        "/structural-completions",
        json={"structural_validation_id": "99999999-9999-9999-9999-999999999999"},
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_complete_structural_transition_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.post(
        "/structural-completions",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={"structural_validation_id": "99999999-9999-9999-9999-999999999999"},
    )

    assert response.status_code == 403


def test_complete_structural_transition_rejects_missing_required_field(client: TestClient) -> None:
    response = client.post(
        "/structural-completions",
        headers=_auth_headers(),
        json={"completion_notes": "Missing structural_validation_id."},
    )

    assert response.status_code == 422


def test_complete_structural_transition_does_not_require_tenant_header(client: TestClient) -> None:
    validation_id = _seed_validation(client, "API-COMPLETE-NODE-004")

    response = client.post(
        "/structural-completions",
        headers=_auth_headers(),
        json={"structural_validation_id": validation_id},
    )

    assert response.status_code == 201


def test_complete_structural_transition_does_not_mutate_organization_node(client: TestClient) -> None:
    """Option A scope, verified at the API layer: the target node's own fields are unchanged after completion."""
    node = client.post(
        "/organization-nodes",
        headers=_auth_headers(),
        json={"node_code": "API-COMPLETE-NODE-005", "node_name": "API Completion Node", "node_type": "HOLDING"},
    )
    node_id = node.json()["id"]
    before = client.get(f"/organization-nodes/{node_id}", headers=_auth_headers()).json()

    intent = client.post(
        "/structural-change-intents",
        headers=_auth_headers(),
        json={"change_rationale": "Observed structural gap.", "target_outcome": "Target structural outcome."},
    )
    proposal = client.post(
        "/structural-proposals",
        headers=_auth_headers(),
        json={
            "structural_change_intent_id": intent.json()["id"],
            "target_organization_node_id": node_id,
            "proposed_outcome_description": "Consolidate under this holding node.",
        },
    )
    proposal_id = proposal.json()["id"]
    review = client.post(
        "/structural-reviews",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "review_position": "Supportive."},
    )
    review_id = review.json()["id"]
    client.post(f"/structural-reviews/{review_id}/resolve-concerns", headers=_auth_headers(), json={})
    validation = client.post(
        "/structural-validations",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "structural_review_id": review_id},
    )
    validation_id = validation.json()["id"]

    completed = client.post(
        "/structural-completions", headers=_auth_headers(), json={"structural_validation_id": validation_id}
    )
    assert completed.status_code == 201

    after = client.get(f"/organization-nodes/{node_id}", headers=_auth_headers()).json()
    assert after["node_name"] == before["node_name"]
    assert after["operational_status"] == before["operational_status"]
    assert after["active_flag"] == before["active_flag"]


# ---------------------------------------------------------------------------
# BA-09 — Continue from Resulting Structure
# ---------------------------------------------------------------------------

def test_get_structural_completion_returns_details_for_platform_admin(client: TestClient) -> None:
    validation_id = _seed_validation(client, "API-COMPLETE-NODE-006")
    created = client.post(
        "/structural-completions",
        headers=_auth_headers(),
        json={"structural_validation_id": validation_id, "completion_notes": "Completed."},
    )
    assert created.status_code == 201
    completion_id = created.json()["id"]

    response = client.get(f"/structural-completions/{completion_id}", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == completion_id
    assert body["structural_validation_id"] == validation_id
    assert body["completion_notes"] == "Completed."


def test_get_structural_completion_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.get(
        "/structural-completions/99999999-9999-9999-9999-999999999999",
        headers=_auth_headers(),
    )

    assert response.status_code == 404


def test_get_structural_completion_requires_authorization_header(client: TestClient) -> None:
    response = client.get("/structural-completions/99999999-9999-9999-9999-999999999999")

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_get_structural_completion_rejects_invalid_token(client: TestClient) -> None:
    response = client.get(
        "/structural-completions/99999999-9999-9999-9999-999999999999",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401


def test_get_structural_completion_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.get(
        "/structural-completions/99999999-9999-9999-9999-999999999999",
        headers=_auth_headers(role_code="ORG_ADMIN"),
    )

    assert response.status_code == 403


def test_get_structural_completion_rejects_invalid_uuid(client: TestClient) -> None:
    response = client.get("/structural-completions/not-a-uuid", headers=_auth_headers())

    assert response.status_code == 422


def test_get_structural_completion_does_not_require_tenant_header(client: TestClient) -> None:
    """
    GET /structural-completions/{id} is tenant-agnostic (the existing
    /structural-completions/* prefix exemption added for BA-08, no
    middleware change required for BA-09). No X-Tenant-ID header sent;
    a 404 (not 400) proves the request reached the handler rather than
    being blocked by the tenant-header check.
    """
    response = client.get(
        f"/structural-completions/{'99999999-9999-9999-9999-999999999999'}",
        headers=_auth_headers(),
    )

    assert response.status_code == 404
