import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.approval_authority import ApprovalAuthority
from models.domain import Domain
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
    """Mirrors test_domain_permission_api.py's _access_token() exactly."""
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
async def seeded_membership_and_domain(db_session: AsyncSession) -> tuple[str, str, str]:
    person = Person(first_name="Access", last_name="Subject", display_name="Access Subject")
    organization = Organization(
        organization_code="AE-API-TEST-ORG",
        organization_name="Access Evaluation API Test Org",
        organization_type="CORPORATE",
    )
    role = Role(role_code="AE_API_TEST_ROLE", role_name="Access Evaluation API Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    domain = Domain(domain_name="Finance")
    db_session.add_all([membership, domain])
    await db_session.commit()

    return str(membership.id), str(domain.id), str(organization.id)


@pytest.fixture
async def seeded_domain_with_approval_authority(
    db_session: AsyncSession, seeded_membership_and_domain
) -> tuple[str, str]:
    membership_id, domain_id, organization_id = seeded_membership_and_domain
    approval_authority = ApprovalAuthority(
        organization_id=uuid.UUID(organization_id),
        authority_name="Finance Domain Approval",
        approval_strategy="ANY_ONE",
        scope_type="DOMAIN",
        domain_id=uuid.UUID(domain_id),
    )
    db_session.add(approval_authority)
    await db_session.commit()

    return membership_id, domain_id


# ---------------------------------------------------------------------------
# BA-01 — Evaluate Access for a Governed Request
# ---------------------------------------------------------------------------

def test_evaluate_access_returns_201_and_unresolved_for_unknown_membership(
    client: TestClient, seeded_membership_and_domain
) -> None:
    _membership_id, domain_id, _org_id = seeded_membership_and_domain

    response = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": str(uuid.uuid4()), "domain_id": domain_id, "permission_level": "VIEW"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["outcome_type"] == "UNRESOLVED"
    assert body["validity_status"] == "CREATED"


def test_evaluate_access_returns_deferred_when_approval_authority_governs_domain(
    client: TestClient, seeded_domain_with_approval_authority
) -> None:
    membership_id, domain_id = seeded_domain_with_approval_authority

    response = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "APPROVE"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["outcome_type"] == "DEFERRED"
    assert body["approval_authority_id"] is not None


def test_evaluate_access_returns_501_when_no_approval_authority_governs_domain(
    client: TestClient, seeded_membership_and_domain
) -> None:
    """IRA-005 S12: an ACTIVE membership with no governing Approval Authority is explicitly out of scope, never a fabricated decision."""
    membership_id, domain_id, _org_id = seeded_membership_and_domain

    response = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )

    assert response.status_code == 501


def test_evaluate_access_rejects_unknown_domain(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, _domain_id, _org_id = seeded_membership_and_domain

    response = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": str(uuid.uuid4()), "permission_level": "VIEW"},
    )

    assert response.status_code == 404


def test_evaluate_access_requires_authorization_header(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id, _org_id = seeded_membership_and_domain

    response = client.post(
        "/access-evaluations",
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )

    assert response.status_code == 400


def test_evaluate_access_rejects_non_platform_admin(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id, _org_id = seeded_membership_and_domain

    response = client.post(
        "/access-evaluations",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "VIEW"},
    )

    assert response.status_code == 403


def test_evaluate_access_rejects_invalid_permission_level(
    client: TestClient, seeded_membership_and_domain
) -> None:
    membership_id, domain_id, _org_id = seeded_membership_and_domain

    response = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": membership_id, "domain_id": domain_id, "permission_level": "NOT_A_REAL_LEVEL"},
    )

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# BA-02 — Preserve and Bound Access Evaluation Outcome Validity
# ---------------------------------------------------------------------------

def test_preserve_and_expire_lifecycle(
    client: TestClient, seeded_membership_and_domain
) -> None:
    _membership_id, domain_id, _org_id = seeded_membership_and_domain
    created = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": str(uuid.uuid4()), "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()
    outcome_id = created["id"]

    preserve_response = client.post(
        f"/access-evaluations/{outcome_id}/preserve", headers=_auth_headers(), json={}
    )
    assert preserve_response.status_code == 200
    assert preserve_response.json()["validity_status"] == "PRESERVED"

    duplicate_preserve = client.post(
        f"/access-evaluations/{outcome_id}/preserve", headers=_auth_headers(), json={}
    )
    assert duplicate_preserve.status_code == 409

    expire_response = client.post(
        f"/access-evaluations/{outcome_id}/expire", headers=_auth_headers(), json={}
    )
    assert expire_response.status_code == 200
    assert expire_response.json()["validity_status"] == "EXPIRED"


def test_preserve_rejects_unknown_outcome(client: TestClient) -> None:
    response = client.post(
        f"/access-evaluations/{uuid.uuid4()}/preserve", headers=_auth_headers(), json={}
    )

    assert response.status_code == 404


def test_expire_rejects_outcome_that_was_never_preserved(
    client: TestClient, seeded_membership_and_domain
) -> None:
    """TD-081: a CREATED (never preserved) outcome may not be expired directly."""
    _membership_id, domain_id, _org_id = seeded_membership_and_domain
    created = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": str(uuid.uuid4()), "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()
    outcome_id = created["id"]

    response = client.post(
        f"/access-evaluations/{outcome_id}/expire", headers=_auth_headers(), json={}
    )

    assert response.status_code == 409


# ---------------------------------------------------------------------------
# BA-03 — Detect and Resolve Access Context Change
# ---------------------------------------------------------------------------

def test_context_change_invalidates_outcome(
    client: TestClient, seeded_membership_and_domain
) -> None:
    _membership_id, domain_id, _org_id = seeded_membership_and_domain
    created = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": str(uuid.uuid4()), "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()
    outcome_id = created["id"]

    response = client.post(
        f"/access-evaluations/{outcome_id}/context-change",
        headers=_auth_headers(),
        json={"changed_fact": "Membership standing changed."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["invalidated"] is True
    assert body["re_evaluation_required"] is True


def test_context_change_rejects_non_live_outcome(
    client: TestClient, seeded_membership_and_domain
) -> None:
    """TD-081: a second context-change against an already-invalidated outcome is rejected."""
    _membership_id, domain_id, _org_id = seeded_membership_and_domain
    created = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": str(uuid.uuid4()), "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()
    outcome_id = created["id"]
    client.post(
        f"/access-evaluations/{outcome_id}/context-change",
        headers=_auth_headers(),
        json={"changed_fact": "First change."},
    )

    response = client.post(
        f"/access-evaluations/{outcome_id}/context-change",
        headers=_auth_headers(),
        json={"changed_fact": "Second change."},
    )

    assert response.status_code == 409


# ---------------------------------------------------------------------------
# BA-04 — Resolve Dependent Capability Access Hand-off Rejection
# ---------------------------------------------------------------------------

def test_handoff_rejection_classifies_live_outcome(
    client: TestClient, seeded_membership_and_domain
) -> None:
    _membership_id, domain_id, _org_id = seeded_membership_and_domain
    created = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": str(uuid.uuid4()), "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()
    outcome_id = created["id"]

    response = client.post(
        f"/access-evaluations/{outcome_id}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-007", "stated_reason": "Scope mismatch."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "CAPABILITY_SCOPED_INSUFFICIENCY"
    assert body["object_preserved"] is True


def test_handoff_rejection_classifies_invalidated_outcome_as_integrity_signal(
    client: TestClient, seeded_membership_and_domain
) -> None:
    """TD-081: the non-live (invalidated) branch, mirrored from the unit-level test."""
    _membership_id, domain_id, _org_id = seeded_membership_and_domain
    created = client.post(
        "/access-evaluations",
        headers=_auth_headers(),
        json={"membership_id": str(uuid.uuid4()), "domain_id": domain_id, "permission_level": "VIEW"},
    ).json()
    outcome_id = created["id"]
    client.post(
        f"/access-evaluations/{outcome_id}/context-change",
        headers=_auth_headers(),
        json={"changed_fact": "Context changed."},
    )

    response = client.post(
        f"/access-evaluations/{outcome_id}/handoff-rejection",
        headers=_auth_headers(),
        json={"reporting_capability": "C-007", "stated_reason": "Object looks stale."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "INTEGRITY_SIGNAL"
    assert body["object_preserved"] is False
    assert body["routed_to"] == "BA-01 (Evaluate Access for a Governed Request)"
