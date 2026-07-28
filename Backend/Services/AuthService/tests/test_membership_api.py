"""
WP-03 BA-01/BA-02 — Establish + Understand Membership Context
(ERB-C007-01 / EX-C007-01 + EX-C007-02, and ERB-C007-02 / EX-C007-03,
per PE-001-C007). API-layer tests for POST /memberships and
GET /memberships/{membership_id}.
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.organization import Organization
from models.organization_node import OrganizationNode
from models.person import Person
from models.role import Role


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


@pytest.fixture
async def seeded_person_organization_role(db_session: AsyncSession) -> tuple[str, str, str]:
    person = Person(first_name="Ada", last_name="Lovelace", display_name="Ada Lovelace")
    organization = Organization(
        organization_code="MEM_API_TEST_ORG", organization_name="Membership API Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="MEM_API_TEST_ROLE", role_name="Membership API Test Role")
    db_session.add_all([person, organization, role])
    await db_session.commit()
    return str(person.id), str(organization.id), str(role.id)


def test_establish_membership_succeeds_for_platform_admin(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role

    response = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["person_id"] == person_id
    assert body["organization_id"] == organization_id
    assert body["role_id"] == role_id
    assert body["home_node_id"] is None
    assert body["membership_type"] == "INTERNAL"
    assert body["license_type"] == "FULL"


def test_establish_membership_rejects_duplicate(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    payload = {"person_id": person_id, "organization_id": organization_id, "role_id": role_id}
    client.post("/memberships", headers=_auth_headers(), json=payload)

    response = client.post("/memberships", headers=_auth_headers(), json=payload)
    assert response.status_code == 409


def test_establish_membership_rejects_unknown_person(
    client: TestClient, seeded_person_organization_role
) -> None:
    _person_id, organization_id, role_id = seeded_person_organization_role
    response = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": str(uuid.uuid4()), "organization_id": organization_id, "role_id": role_id},
    )
    assert response.status_code == 404


@pytest.fixture
async def seeded_organization_node(db_session: AsyncSession) -> str:
    node = OrganizationNode(node_code="NODE-API-001", node_name="API Test Node", node_type="entity")
    db_session.add(node)
    await db_session.commit()
    return str(node.id)


def test_establish_membership_with_confirmed_home_node(
    client: TestClient, seeded_person_organization_role, seeded_organization_node
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    node_id = seeded_organization_node

    response = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={
            "person_id": person_id, "organization_id": organization_id, "role_id": role_id,
            "home_node_id": node_id,
        },
    )

    assert response.status_code == 201
    assert response.json()["home_node_id"] == node_id


def test_establish_membership_rejects_non_platform_admin(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    response = client.post(
        "/memberships",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    )
    assert response.status_code == 403


def test_establish_membership_requires_authorization_header(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    response = client.post(
        "/memberships",
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    )
    assert response.status_code == 400


def test_establish_membership_requires_role_id(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, _role_id = seeded_person_organization_role
    response = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id},
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# BA-02 — Understand Membership Context (ERB-C007-02/EX-C007-03)
# ---------------------------------------------------------------------------

def test_understand_membership_succeeds_for_platform_admin(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.get(f"/memberships/{established['id']}", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == established["id"]
    assert body["membership_status"] == "ACTIVE"
    assert body["currently_effective"] is True
    assert body["authority_consequence"] == "ACTIVE_AND_EFFECTIVE"


def test_understand_membership_reports_lapsed_membership_as_not_currently_effective(
    client: TestClient, seeded_person_organization_role
) -> None:
    """BR-C007-013: an ACTIVE Membership whose effective_to has already passed is never presented as currently effective."""
    person_id, organization_id, role_id = seeded_person_organization_role
    past = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={
            "person_id": person_id, "organization_id": organization_id, "role_id": role_id,
            "effective_to": past,
        },
    ).json()

    response = client.get(f"/memberships/{established['id']}", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["membership_status"] == "ACTIVE"
    assert body["currently_effective"] is False
    assert body["authority_consequence"] == "ACTIVE_BUT_LAPSED"


def test_understand_membership_rejects_unknown_id(client: TestClient) -> None:
    response = client.get(f"/memberships/{uuid.uuid4()}", headers=_auth_headers())
    assert response.status_code == 404


def test_understand_membership_rejects_non_platform_admin(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.get(f"/memberships/{established['id']}", headers=_auth_headers(role_code="ESG_MANAGER"))
    assert response.status_code == 403


def test_understand_membership_requires_authorization_header(client: TestClient) -> None:
    response = client.get(f"/memberships/{uuid.uuid4()}")
    assert response.status_code == 400
