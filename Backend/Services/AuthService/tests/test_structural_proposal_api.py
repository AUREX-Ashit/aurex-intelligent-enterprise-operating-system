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


def _seed_intent_and_node(client: TestClient, node_code: str) -> tuple[str, str]:
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
    return intent.json()["id"], node.json()["id"]


def test_shape_structural_proposal_succeeds_for_platform_admin(client: TestClient) -> None:
    intent_id, node_id = _seed_intent_and_node(client, "API-PROP-NODE-001")

    response = client.post(
        "/structural-proposals",
        headers=_auth_headers(),
        json={
            "structural_change_intent_id": intent_id,
            "target_organization_node_id": node_id,
            "proposed_outcome_description": "Consolidate under this holding node.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["proposal_id"] == body["id"]
    assert body["revision_number"] == 1
    assert body["status"] == "CREATED"
    assert body["structural_change_intent_id"] == intent_id
    assert body["target_organization_node_id"] == node_id


def test_shape_structural_proposal_rejects_unknown_structural_change_intent(client: TestClient) -> None:
    _, node_id = _seed_intent_and_node(client, "API-PROP-NODE-002")

    response = client.post(
        "/structural-proposals",
        headers=_auth_headers(),
        json={
            "structural_change_intent_id": "99999999-9999-9999-9999-999999999999",
            "target_organization_node_id": node_id,
            "proposed_outcome_description": "Consolidate under this holding node.",
        },
    )

    assert response.status_code == 404


def test_shape_structural_proposal_rejects_unknown_organization_node(client: TestClient) -> None:
    intent_id, _ = _seed_intent_and_node(client, "API-PROP-NODE-003")

    response = client.post(
        "/structural-proposals",
        headers=_auth_headers(),
        json={
            "structural_change_intent_id": intent_id,
            "target_organization_node_id": "99999999-9999-9999-9999-999999999999",
            "proposed_outcome_description": "Consolidate under this holding node.",
        },
    )

    assert response.status_code == 404


def test_shape_structural_proposal_requires_authorization_header(client: TestClient) -> None:
    intent_id, node_id = _seed_intent_and_node(client, "API-PROP-NODE-004")

    response = client.post(
        "/structural-proposals",
        json={
            "structural_change_intent_id": intent_id,
            "target_organization_node_id": node_id,
            "proposed_outcome_description": "Consolidate under this holding node.",
        },
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_shape_structural_proposal_rejects_non_platform_admin_role(client: TestClient) -> None:
    intent_id, node_id = _seed_intent_and_node(client, "API-PROP-NODE-005")

    response = client.post(
        "/structural-proposals",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={
            "structural_change_intent_id": intent_id,
            "target_organization_node_id": node_id,
            "proposed_outcome_description": "Consolidate under this holding node.",
        },
    )

    assert response.status_code == 403


def test_shape_structural_proposal_rejects_missing_required_field(client: TestClient) -> None:
    response = client.post(
        "/structural-proposals",
        headers=_auth_headers(),
        json={"proposed_outcome_description": "Missing intent and node."},
    )

    assert response.status_code == 422


def test_shape_structural_proposal_does_not_require_tenant_header(client: TestClient) -> None:
    intent_id, node_id = _seed_intent_and_node(client, "API-PROP-NODE-006")

    response = client.post(
        "/structural-proposals",
        headers=_auth_headers(),
        json={
            "structural_change_intent_id": intent_id,
            "target_organization_node_id": node_id,
            "proposed_outcome_description": "Consolidate under this holding node.",
        },
    )

    assert response.status_code == 201


def test_refine_structural_proposal_creates_revision_two(client: TestClient) -> None:
    intent_id, node_id = _seed_intent_and_node(client, "API-PROP-NODE-007")
    shaped = client.post(
        "/structural-proposals",
        headers=_auth_headers(),
        json={
            "structural_change_intent_id": intent_id,
            "target_organization_node_id": node_id,
            "proposed_outcome_description": "Original description.",
        },
    )
    proposal_id = shaped.json()["proposal_id"]

    response = client.post(
        f"/structural-proposals/{proposal_id}/revisions",
        headers=_auth_headers(),
        json={"proposed_outcome_description": "Refined description."},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["proposal_id"] == proposal_id
    assert body["revision_number"] == 2
    assert body["proposed_outcome_description"] == "Refined description."
    assert body["id"] != shaped.json()["id"]


def test_refine_structural_proposal_rejects_unknown_proposal_id(client: TestClient) -> None:
    response = client.post(
        "/structural-proposals/99999999-9999-9999-9999-999999999999/revisions",
        headers=_auth_headers(),
        json={"proposed_outcome_description": "Refined description."},
    )

    assert response.status_code == 404


def test_refine_structural_proposal_requires_authorization_header(client: TestClient) -> None:
    response = client.post(
        "/structural-proposals/99999999-9999-9999-9999-999999999999/revisions",
        json={"proposed_outcome_description": "Refined description."},
    )

    assert response.status_code == 400


def test_refine_structural_proposal_rejects_non_platform_admin_role(client: TestClient) -> None:
    response = client.post(
        "/structural-proposals/99999999-9999-9999-9999-999999999999/revisions",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={"proposed_outcome_description": "Refined description."},
    )

    assert response.status_code == 403


def test_refine_structural_proposal_does_not_require_tenant_header(client: TestClient) -> None:
    intent_id, node_id = _seed_intent_and_node(client, "API-PROP-NODE-008")
    shaped = client.post(
        "/structural-proposals",
        headers=_auth_headers(),
        json={
            "structural_change_intent_id": intent_id,
            "target_organization_node_id": node_id,
            "proposed_outcome_description": "Original description.",
        },
    )
    proposal_id = shaped.json()["proposal_id"]

    response = client.post(
        f"/structural-proposals/{proposal_id}/revisions",
        headers=_auth_headers(),
        json={"proposed_outcome_description": "Refined description."},
    )

    assert response.status_code == 201
