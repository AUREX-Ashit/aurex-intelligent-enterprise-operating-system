"""
WP-03 BA-01/BA-02/BA-03 — Establish + Understand + Maintain Membership
Terms (ERB-C007-01 / EX-C007-01 + EX-C007-02, ERB-C007-02 / EX-C007-03,
and ERB-C007-03 / EX-C007-04 + EX-C007-05, per PE-001-C007). API-layer
tests for POST /memberships, GET /memberships/{membership_id}, and
POST /memberships/{membership_id}/terms.
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.membership import Membership
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


# ---------------------------------------------------------------------------
# BA-03 — Maintain Membership Terms (ERB-C007-03/EX-C007-04+05)
# ---------------------------------------------------------------------------

@pytest.fixture
async def seeded_inactive_organization_node(db_session: AsyncSession) -> str:
    node = OrganizationNode(node_code="NODE-API-INACTIVE", node_name="Inactive API Test Node", node_type="entity", active_flag=False)
    db_session.add(node)
    await db_session.commit()
    return str(node.id)


def test_change_terms_succeeds_for_platform_admin(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/terms",
        headers=_auth_headers(),
        json={"license_type": "LIGHT", "reason": "Downgraded per subscription change"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["license_type"] == "LIGHT"
    assert body["membership_type"] == "INTERNAL"  # untouched field unchanged


def test_change_terms_rejects_no_actual_change(
    client: TestClient, seeded_person_organization_role
) -> None:
    """BR-C007-003: every supplied term already matches the current value — classified erroneous, not a genuine change."""
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/terms",
        headers=_auth_headers(),
        json={"license_type": "FULL", "membership_type": "INTERNAL"},
    )

    assert response.status_code == 409


def test_change_terms_rejects_empty_request(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(f"/memberships/{established['id']}/terms", headers=_auth_headers(), json={})

    assert response.status_code == 422


def test_change_terms_rejects_unknown_membership_id(client: TestClient) -> None:
    response = client.post(
        f"/memberships/{uuid.uuid4()}/terms", headers=_auth_headers(), json={"license_type": "LIGHT"},
    )
    assert response.status_code == 404


def test_change_terms_with_valid_home_node(
    client: TestClient, seeded_person_organization_role, seeded_organization_node
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    node_id = seeded_organization_node
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/terms", headers=_auth_headers(), json={"home_node_id": node_id},
    )

    assert response.status_code == 200
    assert response.json()["home_node_id"] == node_id


def test_change_terms_rejects_unknown_home_node(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/terms",
        headers=_auth_headers(),
        json={"home_node_id": str(uuid.uuid4())},
    )

    assert response.status_code == 404


def test_change_terms_rejects_inactive_home_node(
    client: TestClient, seeded_person_organization_role, seeded_inactive_organization_node
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    node_id = seeded_inactive_organization_node
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/terms", headers=_auth_headers(), json={"home_node_id": node_id},
    )

    assert response.status_code == 409


def test_change_terms_leaves_membership_status_unaffected(
    client: TestClient, seeded_person_organization_role
) -> None:
    """BR-C007-006: Membership terms and standing are governed independently — a term change never touches membership_status."""
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()
    assert established["membership_status"] == "ACTIVE"

    response = client.post(
        f"/memberships/{established['id']}/terms", headers=_auth_headers(), json={"license_type": "LIGHT"},
    )

    assert response.json()["membership_status"] == "ACTIVE"


def test_change_terms_rejects_non_platform_admin(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/terms",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"license_type": "LIGHT"},
    )

    assert response.status_code == 403


def test_change_terms_requires_authorization_header(client: TestClient) -> None:
    response = client.post(f"/memberships/{uuid.uuid4()}/terms", json={"license_type": "LIGHT"})
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# BA-06 — Reactivate Membership (ERB-C007-04/EX-C007-08)
# ---------------------------------------------------------------------------

@pytest.fixture
async def seeded_suspended_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> str:
    """
    No Business Activity yet writes a non-ACTIVE membership_status
    (BA-05 is BLOCKED) - seeded directly, mirroring the same
    direct-data-setup precedent BA-01's own OrganizationNode fixtures
    already use for a path no BA yet establishes.
    """
    person_id, organization_id, role_id = seeded_person_organization_role
    membership = Membership(
        person_id=uuid.UUID(person_id),
        organization_id=uuid.UUID(organization_id),
        role_id=uuid.UUID(role_id),
        membership_status="SUSPENDED",
    )
    db_session.add(membership)
    await db_session.commit()
    return str(membership.id)


def test_reactivate_membership_rejects_unknown_id(client: TestClient) -> None:
    response = client.post(
        f"/memberships/{uuid.uuid4()}/reactivate", headers=_auth_headers(), json={},
    )
    assert response.status_code == 404


def test_reactivate_membership_rejects_already_active(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/reactivate", headers=_auth_headers(), json={},
    )

    assert response.status_code == 409


def test_reactivate_membership_rejects_suspended_pending_canonical_binding(
    client: TestClient, seeded_suspended_membership
) -> None:
    """BR-C007-014/Contract 5.3: no canonical authority establishes that SUSPENDED may transition to ACTIVE (TD-037)."""
    membership_id = seeded_suspended_membership

    response = client.post(
        f"/memberships/{membership_id}/reactivate",
        headers=_auth_headers(),
        json={"reason": "Return from leave"},
    )

    assert response.status_code == 409


def test_reactivate_membership_preserves_existing_context_unchanged(
    client: TestClient, seeded_suspended_membership
) -> None:
    """A rejected reactivation SHALL preserve the existing Membership context exactly as it stood (6.3)."""
    membership_id = seeded_suspended_membership

    client.post(f"/memberships/{membership_id}/reactivate", headers=_auth_headers(), json={})
    response = client.get(f"/memberships/{membership_id}", headers=_auth_headers())

    assert response.json()["membership_status"] == "SUSPENDED"


def test_reactivate_membership_rejects_non_platform_admin(
    client: TestClient, seeded_suspended_membership
) -> None:
    membership_id = seeded_suspended_membership

    response = client.post(
        f"/memberships/{membership_id}/reactivate",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={},
    )

    assert response.status_code == 403


def test_reactivate_membership_requires_authorization_header(client: TestClient) -> None:
    response = client.post(f"/memberships/{uuid.uuid4()}/reactivate", json={})
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# BA-07 — Surface Multi-Organization Membership Awareness (ERB-C007-05/EX-C007-09)
# ---------------------------------------------------------------------------

def test_multi_organization_awareness_rejects_unknown_person(
    client: TestClient, seeded_person_organization_role
) -> None:
    _person_id, organization_id, _role_id = seeded_person_organization_role

    response = client.get(
        "/memberships/multi-organization-awareness",
        headers=_auth_headers(),
        params={"person_id": str(uuid.uuid4()), "organization_id": organization_id},
    )

    assert response.status_code == 404


def test_multi_organization_awareness_rejects_unknown_organization(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, _organization_id, _role_id = seeded_person_organization_role

    response = client.get(
        "/memberships/multi-organization-awareness",
        headers=_auth_headers(),
        params={"person_id": person_id, "organization_id": str(uuid.uuid4())},
    )

    assert response.status_code == 404


def test_multi_organization_awareness_returns_false_when_no_other_memberships(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    )

    response = client.get(
        "/memberships/multi-organization-awareness",
        headers=_auth_headers(),
        params={"person_id": person_id, "organization_id": organization_id},
    )

    assert response.status_code == 200
    assert response.json()["has_memberships_in_other_organizations"] is False


@pytest.fixture
async def seeded_other_organization(db_session: AsyncSession) -> str:
    other_organization = Organization(
        organization_code="MEM_API_TEST_ORG_OTHER", organization_name="Other API Test Org", organization_type="CORPORATE",
    )
    db_session.add(other_organization)
    await db_session.commit()
    return str(other_organization.id)


def test_multi_organization_awareness_returns_true_when_other_memberships_exist(
    client: TestClient, seeded_person_organization_role, seeded_other_organization
) -> None:
    """BR-C007-008: the establishing Organization learns only that other Memberships exist, never which."""
    person_id, organization_id, role_id = seeded_person_organization_role
    other_organization_id = seeded_other_organization
    client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    )
    client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": other_organization_id, "role_id": role_id},
    )

    response = client.get(
        "/memberships/multi-organization-awareness",
        headers=_auth_headers(),
        params={"person_id": person_id, "organization_id": organization_id},
    )

    assert response.status_code == 200
    assert response.json()["has_memberships_in_other_organizations"] is True


def test_multi_organization_awareness_rejects_non_platform_admin(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, _role_id = seeded_person_organization_role

    response = client.get(
        "/memberships/multi-organization-awareness",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        params={"person_id": person_id, "organization_id": organization_id},
    )

    assert response.status_code == 403


def test_multi_organization_awareness_requires_authorization_header(client: TestClient) -> None:
    response = client.get(
        "/memberships/multi-organization-awareness",
        params={"person_id": str(uuid.uuid4()), "organization_id": str(uuid.uuid4())},
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# BA-08 — Present Person's Own Cross-Organization Membership View (ERB-C007-05/EX-C007-10)
# ---------------------------------------------------------------------------

SELF_PERSON_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
"""Matches _access_token()'s own hardcoded 'person_id' claim, so the self-service /my-portfolio endpoint can be exercised against a real Person row."""


@pytest.fixture
async def seeded_self_person_organization_role(db_session: AsyncSession) -> tuple[str, str, str]:
    person = Person(id=SELF_PERSON_ID, first_name="Self", last_name="Caller", display_name="Self Caller")
    organization = Organization(
        organization_code="MEM_API_TEST_SELF_ORG", organization_name="Self Portfolio Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="MEM_API_TEST_SELF_ROLE", role_name="Self Portfolio Test Role")
    db_session.add_all([person, organization, role])
    await db_session.commit()
    return str(person.id), str(organization.id), str(role.id)


def test_present_own_portfolio_returns_empty_list_when_no_memberships(client: TestClient) -> None:
    response = client.get("/memberships/my-portfolio", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["memberships"] == []


def test_present_own_portfolio_returns_full_detail_for_own_membership(
    client: TestClient, seeded_self_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_self_person_organization_role
    assert person_id == str(SELF_PERSON_ID)
    client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    )

    response = client.get("/memberships/my-portfolio", headers=_auth_headers())

    assert response.status_code == 200
    memberships = response.json()["memberships"]
    assert len(memberships) == 1
    assert memberships[0]["organization_id"] == organization_id
    assert memberships[0]["membership_status"] == "ACTIVE"


def test_present_own_portfolio_never_returns_a_different_persons_membership(
    client: TestClient, seeded_person_organization_role
) -> None:
    """Confirms no cross-Person leakage: seeded_person_organization_role creates a *different* Person than SELF_PERSON_ID."""
    person_id, organization_id, role_id = seeded_person_organization_role
    assert person_id != str(SELF_PERSON_ID)
    client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    )

    response = client.get("/memberships/my-portfolio", headers=_auth_headers())

    assert response.status_code == 200
    assert response.json()["memberships"] == []


def test_present_own_portfolio_does_not_require_platform_admin(client: TestClient) -> None:
    """BR-C007-009: any authenticated caller may see their own portfolio - no role gate, unlike every other WP-03 endpoint."""
    response = client.get("/memberships/my-portfolio", headers=_auth_headers(role_code="ESG_MANAGER"))

    assert response.status_code == 200


def test_present_own_portfolio_requires_authorization_header(client: TestClient) -> None:
    response = client.get("/memberships/my-portfolio")
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# BA-09 — Preserve Membership Context Across Enterprise Journeys (ERB-C007-06/EX-C007-11)
# ---------------------------------------------------------------------------
#
# No new endpoint - EX-C007-11's own carry-forward/recompute-live
# requirement is the identical mechanism Contract 5.5 groups with
# BA-02's own understand() (see the service-layer tests' own module
# comment for the full textual basis). These API-level tests prove the
# same property end-to-end through GET /memberships/{membership_id},
# simulating a Membership continuing across two Enterprise Journey
# points with a term change in between.

def test_preserve_membership_context_recomputes_freshly_across_repeated_carry_forward_reads(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    first_journey_read = client.get(f"/memberships/{established['id']}", headers=_auth_headers()).json()
    assert first_journey_read["license_type"] == "FULL"
    assert first_journey_read["currently_effective"] is True

    client.post(
        f"/memberships/{established['id']}/terms", headers=_auth_headers(), json={"license_type": "LIGHT"},
    )

    second_journey_read = client.get(f"/memberships/{established['id']}", headers=_auth_headers()).json()
    assert second_journey_read["license_type"] == "LIGHT"
    assert second_journey_read["currently_effective"] is True


def test_preserve_membership_context_never_carries_forward_a_lapsed_authority_consequence(
    client: TestClient, seeded_person_organization_role
) -> None:
    """Contract 5.5: an expired Membership is never carried forward as currently effective."""
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()
    lapsed_effective_to = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    client.post(
        f"/memberships/{established['id']}/terms",
        headers=_auth_headers(),
        json={"effective_to": lapsed_effective_to},
    )

    journey_read = client.get(f"/memberships/{established['id']}", headers=_auth_headers()).json()

    assert journey_read["currently_effective"] is False
    assert journey_read["authority_consequence"] == "ACTIVE_BUT_LAPSED"


# ---------------------------------------------------------------------------
# BA-10 — Hand Off Membership Context to a Dependent Capability (ERB-C007-06/EX-C007-12)
# ---------------------------------------------------------------------------

def test_hand_off_rejects_unknown_membership_id(client: TestClient) -> None:
    response = client.post(
        f"/memberships/{uuid.uuid4()}/hand-off",
        headers=_auth_headers(),
        json={"dependent_capability": "C-003", "outcome": "ACCEPTED"},
    )
    assert response.status_code == 404


def test_hand_off_rejects_returned_without_reason(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/hand-off",
        headers=_auth_headers(),
        json={"dependent_capability": "C-002", "outcome": "RETURNED"},
    )

    assert response.status_code == 422


def test_hand_off_accepted_returns_bounded_context_with_fresh_authority_consequence(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/hand-off",
        headers=_auth_headers(),
        json={"dependent_capability": "C-003", "outcome": "ACCEPTED"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["dependent_capability"] == "C-003"
    assert body["outcome"] == "ACCEPTED"
    assert body["reason"] is None
    assert body["membership_context"]["id"] == established["id"]
    assert body["membership_context"]["currently_effective"] is True
    assert body["membership_context"]["authority_consequence"] == "ACTIVE_AND_EFFECTIVE"


def test_hand_off_returned_with_reason_does_not_alter_membership(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/hand-off",
        headers=_auth_headers(),
        json={
            "dependent_capability": "C-008",
            "outcome": "RETURNED",
            "reason": "Membership context supplied is insufficient for this need.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == "RETURNED"
    assert body["reason"] == "Membership context supplied is insufficient for this need."

    unchanged = client.get(f"/memberships/{established['id']}", headers=_auth_headers()).json()
    assert unchanged["membership_status"] == "ACTIVE"
    assert unchanged["license_type"] == "FULL"


def test_hand_off_rejects_invalid_dependent_capability(
    client: TestClient, seeded_person_organization_role
) -> None:
    """Contract 5.10 names exactly C-003/C-002/C-008 - no open-ended 'any other' value, unlike WP-02's own analogous field."""
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/hand-off",
        headers=_auth_headers(),
        json={"dependent_capability": "C-999", "outcome": "ACCEPTED"},
    )

    assert response.status_code == 422


def test_hand_off_rejects_non_platform_admin(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    response = client.post(
        f"/memberships/{established['id']}/hand-off",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"dependent_capability": "C-003", "outcome": "ACCEPTED"},
    )

    assert response.status_code == 403


def test_hand_off_requires_authorization_header(client: TestClient) -> None:
    response = client.post(
        f"/memberships/{uuid.uuid4()}/hand-off",
        json={"dependent_capability": "C-003", "outcome": "ACCEPTED"},
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# BA-11 — Continue from Membership Context Decision (ERB-C007-06/EX-C007-13)
# ---------------------------------------------------------------------------
#
# No new endpoint - see the service-layer tests' own module comment for
# the full textual basis. These API-level tests prove the same
# property end-to-end: a write endpoint's own response body already
# serves as EX-C007-13's own "continuation context," matching an
# independent subsequent GET, so a receiving Enterprise Experience
# never needs to reconstruct it.

def test_establish_response_serves_as_continuation_context_without_refetch(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role

    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    refetched = client.get(f"/memberships/{established['id']}", headers=_auth_headers()).json()
    assert established["person_id"] == refetched["person_id"]
    assert established["organization_id"] == refetched["organization_id"]
    assert established["membership_status"] == refetched["membership_status"]


def test_change_terms_response_serves_as_continuation_context_without_refetch(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    changed = client.post(
        f"/memberships/{established['id']}/terms", headers=_auth_headers(), json={"license_type": "LIGHT"},
    ).json()

    refetched = client.get(f"/memberships/{established['id']}", headers=_auth_headers()).json()
    assert changed["license_type"] == refetched["license_type"] == "LIGHT"


def test_hand_off_response_serves_as_continuation_context_without_refetch(
    client: TestClient, seeded_person_organization_role
) -> None:
    person_id, organization_id, role_id = seeded_person_organization_role
    established = client.post(
        "/memberships",
        headers=_auth_headers(),
        json={"person_id": person_id, "organization_id": organization_id, "role_id": role_id},
    ).json()

    handed_off = client.post(
        f"/memberships/{established['id']}/hand-off",
        headers=_auth_headers(),
        json={"dependent_capability": "C-003", "outcome": "ACCEPTED"},
    ).json()

    refetched = client.get(f"/memberships/{established['id']}", headers=_auth_headers()).json()
    assert handed_off["membership_context"]["membership_status"] == refetched["membership_status"]
    assert handed_off["membership_context"]["currently_effective"] is True
