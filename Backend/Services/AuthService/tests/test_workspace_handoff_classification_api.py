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


def _access_token(person_id: str, role_code: str = "PLATFORM_ADMIN") -> str:
    """
    Mirrors test_access_evaluation_api.py's own PLATFORM_ADMIN-default
    convention — this endpoint is gated by require_platform_admin (see
    routers/workspace.py's own docstring, TD-113), the same interim gate
    /access-evaluations/ /domain-permissions already use, unlike BA-01/
    BA-02's own authenticated-only endpoints.
    """
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


def _auth_headers(person_id: str, role_code: str = "PLATFORM_ADMIN") -> dict[str, str]:
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


def test_classify_handoff_rejection_rejects_non_platform_admin(
    client: TestClient, seeded_active_membership
) -> None:
    """
    TD-113 / V&V Audit Finding 2 remediation: a caller-supplied
    membership_id is never verified against the caller's own claims (the
    endpoint classifies a hand-off reported by a dependent capability,
    not necessarily the caller's own Membership) — an unrestricted
    caller could otherwise learn another tenant's own Membership status.
    Gated by PLATFORM_ADMIN, the same interim measure /access-evaluations
    and /domain-permissions already use, until a real dependent-capability
    trust mechanism exists.
    """
    person, membership = seeded_active_membership

    response = client.post(
        "/workspaces/classify-handoff-rejection",
        json={
            "membership_id": str(membership.id),
            "rejecting_capability": "C-007",
            "stated_reason": "x",
        },
        headers=_auth_headers(str(person.id), role_code="ESG_MANAGER"),
    )

    assert response.status_code == 403


async def test_classify_handoff_rejection_cross_tenant_status_requires_platform_admin(
    client: TestClient, db_session: AsyncSession
) -> None:
    """
    Empirical negative control mirroring the V&V Audit's own from-scratch
    probe: two fully unrelated tenants, no shared Person/Organization/
    Membership. A non-admin caller in Tenant A must not be able to learn
    Tenant B's own Membership status via this endpoint at all — the fix
    is the PLATFORM_ADMIN gate itself, not a per-request tenant check
    (this endpoint's own purpose requires querying Memberships the caller
    does not own).
    """
    person_a = Person(first_name="Tenant", last_name="A", display_name="Tenant A")
    organization_a = Organization(
        organization_code="WS_HANDOFF_TENANT_A", organization_name="Tenant A Org", organization_type="CORPORATE",
    )
    role_a = Role(role_code="WS_HANDOFF_TENANT_A_ROLE", role_name="Tenant A Role")
    person_b = Person(first_name="Tenant", last_name="B", display_name="Tenant B")
    organization_b = Organization(
        organization_code="WS_HANDOFF_TENANT_B", organization_name="Tenant B Org", organization_type="CORPORATE",
    )
    role_b = Role(role_code="WS_HANDOFF_TENANT_B_ROLE", role_name="Tenant B Role")
    db_session.add_all([person_a, organization_a, role_a, person_b, organization_b, role_b])
    await db_session.flush()

    membership_service = MembershipService(
        MembershipRepository(db_session),
        PersonRepository(db_session),
        OrganizationRepository(db_session),
        RoleRepository(db_session),
        OrganizationNodeRepository(db_session),
    )
    membership_b = await membership_service.establish(
        EstablishMembershipRequest(person_id=person_b.id, organization_id=organization_b.id, role_id=role_b.id)
    )

    response = client.post(
        "/workspaces/classify-handoff-rejection",
        json={
            "membership_id": str(membership_b.id),
            "rejecting_capability": "C-007",
            "stated_reason": "x",
        },
        headers=_auth_headers(str(person_a.id), role_code="ESG_MANAGER"),
    )

    assert response.status_code == 403
