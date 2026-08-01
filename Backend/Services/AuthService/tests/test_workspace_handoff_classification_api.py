import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from repositories.organization_repository import OrganizationRepository
from repositories.person_repository import PersonRepository
from repositories.role_repository import RoleRepository
from schemas.membership import EstablishMembershipRequest
from services.membership_service import MembershipService


def _access_token(person_id: str, role_code: str = "ESG_MANAGER") -> str:
    """Mirrors test_identity_api.py's own _access_token() convention."""
    claims = {
        "person_id": person_id,
        "identity_id": str(uuid.uuid4()),
        "organization_id": "33333333-3333-3333-3333-333333333333",
        "membership_id": "44444444-4444-4444-4444-444444444444",
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth_headers(person_id: str, role_code: str = "ESG_MANAGER") -> dict[str, str]:
    return {"Authorization": f"Bearer {_access_token(person_id, role_code)}"}


@pytest.fixture
async def seeded_active_membership(db_session: AsyncSession) -> tuple[Person, Membership]:
    person = Person(first_name="Tomas", last_name="Rivera", display_name="Tomas Rivera")
    organization = Organization(
        organization_code="WS_HANDOFF_API_TEST_ORG", organization_name="Workspace Handoff API Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="WS_HANDOFF_API_TEST_ROLE", role_name="Workspace Handoff API Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership_service = MembershipService(
        MembershipRepository(db_session),
        PersonRepository(db_session),
        OrganizationRepository(db_session),
        RoleRepository(db_session),
        OrganizationNodeRepository(db_session),
    )
    established = await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    return person, established


# ---------------------------------------------------------------------------
# BA-03 — POST /workspaces/classify-handoff-rejection (EX-C008-11)
# ---------------------------------------------------------------------------

def test_classify_handoff_rejection_capability_scoped(
    client: TestClient, seeded_active_membership
) -> None:
    person, membership = seeded_active_membership

    response = client.post(
        "/workspaces/classify-handoff-rejection",
        json={
            "membership_id": str(membership.id),
            "rejecting_capability": "C-007",
            "stated_reason": "Membership hand-off could not confirm the presented Workspace Context.",
        },
        headers=_auth_headers(str(person.id)),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "CAPABILITY_SCOPED_INSUFFICIENCY"
    assert body["context_preserved"] is True


def test_classify_handoff_rejection_integrity_signal_for_unknown_membership(
    client: TestClient,
) -> None:
    response = client.post(
        "/workspaces/classify-handoff-rejection",
        json={
            "membership_id": str(uuid.uuid4()),
            "rejecting_capability": "C-007",
            "stated_reason": "Workspace hand-off rejected this context.",
        },
        headers=_auth_headers(str(uuid.uuid4())),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "INTEGRITY_SIGNAL"
    assert body["context_preserved"] is False
    assert body["routed_to"] is not None


def test_classify_handoff_rejection_rejects_empty_reason(
    client: TestClient, seeded_active_membership
) -> None:
    person, membership = seeded_active_membership

    response = client.post(
        "/workspaces/classify-handoff-rejection",
        json={
            "membership_id": str(membership.id),
            "rejecting_capability": "C-007",
            "stated_reason": "",
        },
        headers=_auth_headers(str(person.id)),
    )

    assert response.status_code == 422


def test_classify_handoff_rejection_requires_authentication(
    client: TestClient, seeded_active_membership
) -> None:
    _person, membership = seeded_active_membership

    response = client.post(
        "/workspaces/classify-handoff-rejection",
        json={
            "membership_id": str(membership.id),
            "rejecting_capability": "C-007",
            "stated_reason": "x",
        },
    )

    assert response.status_code == 400
