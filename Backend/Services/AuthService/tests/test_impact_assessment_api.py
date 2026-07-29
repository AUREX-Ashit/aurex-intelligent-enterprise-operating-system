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


def test_assess_structural_consequence_succeeds_for_platform_admin(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-IMPACT-NODE-001")

    response = client.post(
        "/impact-assessments",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": proposal_id,
            "impact_description": "Consolidation affects three existing reporting relationships.",
            "uncertainty_notes": "Downstream reporting currency mapping not yet confirmed.",
            "downstream_implications": "May require a Membership home-node review.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["structural_proposal_id"] == proposal_id
    assert body["impact_description"] == "Consolidation affects three existing reporting relationships."
    assert body["status"] == "CREATED"
    assert "id" in body


def test_assess_structural_consequence_allows_optional_fields_to_be_omitted(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-IMPACT-NODE-002")

    response = client.post(
        "/impact-assessments",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": proposal_id,
            "impact_description": "Minimal impact description.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["uncertainty_notes"] is None
    assert body["downstream_implications"] is None


def test_assess_structural_consequence_rejects_unknown_structural_proposal(client: TestClient) -> None:
    response = client.post(
        "/impact-assessments",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": "99999999-9999-9999-9999-999999999999",
            "impact_description": "Minimal impact description.",
        },
    )

    assert response.status_code == 404


def test_assess_structural_consequence_requires_authorization_header(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-IMPACT-NODE-003")

    response = client.post(
        "/impact-assessments",
        json={
            "structural_proposal_id": proposal_id,
            "impact_description": "Minimal impact description.",
        },
    )

    assert response.status_code == 400
    assert "Authorization" in response.json()["detail"]


def test_assess_structural_consequence_rejects_invalid_token(client: TestClient) -> None:
    response = client.post(
        "/impact-assessments",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={
            "structural_proposal_id": "99999999-9999-9999-9999-999999999999",
            "impact_description": "Minimal impact description.",
        },
    )

    assert response.status_code == 401


def test_assess_structural_consequence_rejects_non_platform_admin_role(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-IMPACT-NODE-004")

    response = client.post(
        "/impact-assessments",
        headers=_auth_headers(role_code="ORG_ADMIN"),
        json={
            "structural_proposal_id": proposal_id,
            "impact_description": "Minimal impact description.",
        },
    )

    assert response.status_code == 403


def test_assess_structural_consequence_rejects_missing_required_field(client: TestClient) -> None:
    response = client.post(
        "/impact-assessments",
        headers=_auth_headers(),
        json={"uncertainty_notes": "Missing structural_proposal_id and impact_description."},
    )

    assert response.status_code == 422


def test_assess_structural_consequence_rejects_empty_required_field(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-IMPACT-NODE-005")

    response = client.post(
        "/impact-assessments",
        headers=_auth_headers(),
        json={"structural_proposal_id": proposal_id, "impact_description": ""},
    )

    assert response.status_code == 422


def test_assess_structural_consequence_does_not_require_tenant_header(client: TestClient) -> None:
    proposal_id = _seed_proposal(client, "API-IMPACT-NODE-006")

    response = client.post(
        "/impact-assessments",
        headers=_auth_headers(),
        json={
            "structural_proposal_id": proposal_id,
            "impact_description": "Minimal impact description.",
        },
    )

    assert response.status_code == 201
