import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
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
async def seeded_person_organization_role(db_session: AsyncSession) -> tuple[Person, Organization, Role]:
    person = Person(first_name="Wren", last_name="Okafor", display_name="Wren Okafor")
    organization = Organization(
        organization_code="WS_API_TEST_ORG", organization_name="Workspace API Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="WS_API_TEST_ROLE", role_name="Workspace API Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()
    return person, organization, role


async def _establish_membership(db_session: AsyncSession, person: Person, organization: Organization, role: Role) -> None:
    membership_service = MembershipService(
        MembershipRepository(db_session),
        PersonRepository(db_session),
        OrganizationRepository(db_session),
        RoleRepository(db_session),
        OrganizationNodeRepository(db_session),
    )
    await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )


# ---------------------------------------------------------------------------
# BA-01 — GET /workspaces/candidates (EX-C008-01/02)
# ---------------------------------------------------------------------------

async def test_get_candidates_returns_empty_list_when_no_memberships(
    client: TestClient, db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, _organization, _role = seeded_person_organization_role

    response = client.get("/workspaces/candidates", headers=_auth_headers(str(person.id)))

    assert response.status_code == 200
    assert response.json()["candidates"] == []


async def test_get_candidates_returns_candidates_for_active_memberships(
    client: TestClient, db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    await _establish_membership(db_session, person, organization, role)

    response = client.get("/workspaces/candidates", headers=_auth_headers(str(person.id)))

    assert response.status_code == 200
    candidates = response.json()["candidates"]
    assert len(candidates) == 1
    assert candidates[0]["organization_id"] == str(organization.id)
    assert candidates[0]["organization_name"] == organization.organization_name
    assert candidates[0]["role_code"] == role.role_code


async def test_get_candidates_requires_authentication(client: TestClient) -> None:
    response = client.get("/workspaces/candidates")

    assert response.status_code == 400


async def test_get_candidates_does_not_require_tenant_header(
    client: TestClient, db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, _organization, _role = seeded_person_organization_role

    response = client.get("/workspaces/candidates", headers=_auth_headers(str(person.id)))

    assert response.status_code != 400


async def test_get_candidates_only_returns_the_callers_own_memberships(
    client: TestClient, db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    await _establish_membership(db_session, person, organization, role)
    other_person = Person(first_name="Other", last_name="Caller", display_name="Other Caller")
    db_session.add(other_person)
    await db_session.commit()

    response = client.get("/workspaces/candidates", headers=_auth_headers(str(other_person.id)))

    assert response.status_code == 200
    assert response.json()["candidates"] == []
