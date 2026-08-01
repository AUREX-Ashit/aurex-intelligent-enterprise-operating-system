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


def _access_token(membership_id: str, organization_id: str, role_code: str = "ESG_MANAGER") -> str:
    """Mirrors test_identity_api.py's own _access_token() convention."""
    claims = {
        "person_id": str(uuid.uuid4()),
        "identity_id": str(uuid.uuid4()),
        "organization_id": organization_id,
        "membership_id": membership_id,
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth_headers(membership_id: str, organization_id: str, role_code: str = "ESG_MANAGER") -> dict[str, str]:
    return {"Authorization": f"Bearer {_access_token(membership_id, organization_id, role_code)}"}


@pytest.fixture
async def seeded_active_membership(db_session: AsyncSession) -> tuple[Organization, Membership]:
    person = Person(first_name="Priya", last_name="Menon", display_name="Priya Menon")
    organization = Organization(
        organization_code="WS_STATUS_API_TEST_ORG", organization_name="Workspace Status API Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="WS_STATUS_API_TEST_ROLE", role_name="Workspace Status API Test Role")
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
    return organization, established


# ---------------------------------------------------------------------------
# BA-02 — POST /workspaces/refresh-status (EX-C008-10)
# ---------------------------------------------------------------------------

def test_refresh_status_returns_current(client: TestClient, seeded_active_membership) -> None:
    organization, membership = seeded_active_membership

    response = client.post(
        "/workspaces/refresh-status",
        headers=_auth_headers(str(membership.id), str(organization.id)),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "CURRENT"
    assert body["membership_id"] == str(membership.id)
    assert body["organization_id"] == str(organization.id)


def test_refresh_status_returns_unresolved_for_unknown_membership(client: TestClient) -> None:
    unknown_membership_id = str(uuid.uuid4())
    organization_id = str(uuid.uuid4())

    response = client.post(
        "/workspaces/refresh-status",
        headers=_auth_headers(unknown_membership_id, organization_id),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "UNRESOLVED"


def test_refresh_status_requires_authentication(client: TestClient) -> None:
    response = client.post("/workspaces/refresh-status")

    assert response.status_code == 400


def test_refresh_status_does_not_require_tenant_header(client: TestClient, seeded_active_membership) -> None:
    organization, membership = seeded_active_membership

    response = client.post(
        "/workspaces/refresh-status",
        headers=_auth_headers(str(membership.id), str(organization.id)),
    )

    assert response.status_code != 400
