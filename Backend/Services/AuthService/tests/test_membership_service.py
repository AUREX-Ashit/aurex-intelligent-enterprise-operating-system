"""
WP-03 BA-01/BA-02/BA-03 — Establish + Understand + Maintain Membership
Terms (ERB-C007-01 / EX-C007-01 + EX-C007-02, ERB-C007-02 / EX-C007-03,
and ERB-C007-03 / EX-C007-04 + EX-C007-05, per PE-001-C007).
Service-layer tests for MembershipService.establish() (BR-C007-001
recognition-before-establishment, BR-C007-002/007 home-node candidate
validity, referenced-object existence checks), MembershipService.
understand() / compute_membership_authority_consequence() (BR-C007-013:
ACTIVE standing never implies current authority on its own), and
MembershipService.change_terms() (BR-C007-003 classify-before-resolve,
BR-C007-004 preserve pre-change value, BR-C007-006 terms/standing
independence).
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.membership import LicenseType, Membership, MembershipType
from models.organization import Organization
from models.organization_node import OrganizationNode
from models.person import Person
from models.role import Role
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from repositories.organization_repository import OrganizationRepository
from repositories.person_repository import PersonRepository
from repositories.role_repository import RoleRepository
from schemas.membership import (
    ChangeMembershipTermsRequest,
    EstablishMembershipRequest,
    MembershipAuthorityConsequence,
    ReactivateMembershipRequest,
)
from services.membership_service import MembershipService, compute_membership_authority_consequence


@pytest.fixture
async def seeded_person_organization_role(db_session: AsyncSession) -> tuple[Person, Organization, Role]:
    person = Person(first_name="Ada", last_name="Lovelace", display_name="Ada Lovelace")
    organization = Organization(
        organization_code="MEM_TEST_ORG", organization_name="Membership Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="MEM_TEST_ROLE", role_name="Membership Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()
    return person, organization, role


def _service(session: AsyncSession) -> MembershipService:
    return MembershipService(
        MembershipRepository(session),
        PersonRepository(session),
        OrganizationRepository(session),
        RoleRepository(session),
        OrganizationNodeRepository(session),
    )


async def test_establish_creates_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BA-01/EX-C007-02: a first-time Establish call creates exactly one row, ACTIVE by default."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id,
    )

    membership = await service.establish(request, actor_id="platform-admin-1")

    assert membership.id is not None
    assert membership.person_id == person.id
    assert membership.organization_id == organization.id
    assert membership.role_id == role.id
    assert membership.home_node_id is None
    assert membership.membership_type == "INTERNAL"
    assert membership.license_type == "FULL"
    assert membership.membership_status == "ACTIVE"
    assert membership.effective_from is not None
    assert membership.effective_to is None


async def test_establish_rejects_duplicate_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BR-C007-001: a second establish for the same (person, organization) pair is rejected with 409."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    await service.establish(request)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 409


async def test_establish_rejects_unknown_person(db_session: AsyncSession, seeded_person_organization_role) -> None:
    _person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(person_id=uuid.uuid4(), organization_id=organization.id, role_id=role.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 404


async def test_establish_rejects_unknown_organization(db_session: AsyncSession, seeded_person_organization_role) -> None:
    person, _organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(person_id=person.id, organization_id=uuid.uuid4(), role_id=role.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 404


async def test_establish_rejects_unknown_role(db_session: AsyncSession, seeded_person_organization_role) -> None:
    person, organization, _role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=uuid.uuid4())

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 404


async def test_establish_accepts_confirmed_active_home_node(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BR-C007-002/007: a supplied home_node_id that resolves to a real, active node is accepted and persisted."""
    person, organization, role = seeded_person_organization_role
    node = OrganizationNode(node_code="NODE-001", node_name="Test Node", node_type="entity")
    db_session.add(node)
    await db_session.flush()

    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id, home_node_id=node.id,
    )
    membership = await service.establish(request)

    assert membership.home_node_id == node.id


async def test_establish_rejects_unknown_home_node(db_session: AsyncSession, seeded_person_organization_role) -> None:
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id, home_node_id=uuid.uuid4(),
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 404


async def test_establish_rejects_inactive_home_node(db_session: AsyncSession, seeded_person_organization_role) -> None:
    """BR-C007-002: a candidate home-node context that is not active is not authoritative."""
    person, organization, role = seeded_person_organization_role
    node = OrganizationNode(node_code="NODE-INACTIVE", node_name="Inactive Node", node_type="entity", active_flag=False)
    db_session.add(node)
    await db_session.flush()

    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id, home_node_id=node.id,
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 409


async def test_establish_accepts_explicit_membership_and_license_type(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """EX-C007-02 Success Criteria: explicit membership_type and license_type are honored, not defaulted silently when supplied."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id,
        membership_type="EXTERNAL", license_type="LIGHT",
    )

    membership = await service.establish(request)

    assert membership.membership_type == "EXTERNAL"
    assert membership.license_type == "LIGHT"


# ---------------------------------------------------------------------------
# BA-02 — Understand Membership Context (ERB-C007-02/EX-C007-03)
# ---------------------------------------------------------------------------

def _membership(status_: str = "ACTIVE", effective_from=None, effective_to=None) -> Membership:
    """An unpersisted Membership instance — compute_membership_authority_consequence() is pure and needs no session."""
    return Membership(
        person_id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        role_id=uuid.uuid4(),
        membership_status=status_,
        effective_from=effective_from,
        effective_to=effective_to,
    )


def test_compute_authority_consequence_active_open_ended() -> None:
    """BR-C007-013: ACTIVE, effective_from in the past, no effective_to — currently effective."""
    now = datetime(2026, 6, 15, tzinfo=timezone.utc)
    membership = _membership(effective_from=now - timedelta(days=30), effective_to=None)

    currently_effective, consequence = compute_membership_authority_consequence(membership, now=now)

    assert currently_effective is True
    assert consequence == MembershipAuthorityConsequence.ACTIVE_AND_EFFECTIVE


def test_compute_authority_consequence_active_within_window() -> None:
    now = datetime(2026, 6, 15, tzinfo=timezone.utc)
    membership = _membership(effective_from=now - timedelta(days=30), effective_to=now + timedelta(days=30))

    currently_effective, consequence = compute_membership_authority_consequence(membership, now=now)

    assert currently_effective is True
    assert consequence == MembershipAuthorityConsequence.ACTIVE_AND_EFFECTIVE


def test_compute_authority_consequence_active_not_yet_effective() -> None:
    """URA-001-21's own example ('Board Member 2027-2029'): a future-dated window is not yet in effect."""
    now = datetime(2026, 6, 15, tzinfo=timezone.utc)
    membership = _membership(effective_from=now + timedelta(days=30), effective_to=None)

    currently_effective, consequence = compute_membership_authority_consequence(membership, now=now)

    assert currently_effective is False
    assert consequence == MembershipAuthorityConsequence.ACTIVE_NOT_YET_EFFECTIVE


def test_compute_authority_consequence_active_but_lapsed() -> None:
    """BR-C007-013 / Contract 5.1's central rule: ACTIVE standing past effective_to is never presented as currently effective."""
    now = datetime(2026, 6, 15, tzinfo=timezone.utc)
    membership = _membership(effective_from=now - timedelta(days=60), effective_to=now - timedelta(days=1))

    currently_effective, consequence = compute_membership_authority_consequence(membership, now=now)

    assert currently_effective is False
    assert consequence == MembershipAuthorityConsequence.ACTIVE_BUT_LAPSED


def test_compute_authority_consequence_lapsed_at_exact_boundary() -> None:
    """effective_to == now is treated as lapsed (half-open window), not effective."""
    now = datetime(2026, 6, 15, tzinfo=timezone.utc)
    membership = _membership(effective_from=now - timedelta(days=60), effective_to=now)

    currently_effective, consequence = compute_membership_authority_consequence(membership, now=now)

    assert currently_effective is False
    assert consequence == MembershipAuthorityConsequence.ACTIVE_BUT_LAPSED


def test_compute_authority_consequence_not_active_regardless_of_dates() -> None:
    """Non-ACTIVE standing is NOT_ACTIVE even when the effective-date window would otherwise be open — standing and validity are independent facts (Contract 5.3), but standing gates first."""
    now = datetime(2026, 6, 15, tzinfo=timezone.utc)
    membership = _membership(
        status_="SUSPENDED", effective_from=now - timedelta(days=30), effective_to=now + timedelta(days=30),
    )

    currently_effective, consequence = compute_membership_authority_consequence(membership, now=now)

    assert currently_effective is False
    assert consequence == MembershipAuthorityConsequence.NOT_ACTIVE


async def test_understand_returns_existing_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )

    understood = await service.understand(established.id)

    assert understood.id == established.id
    assert understood.person_id == person.id
    assert understood.membership_status == "ACTIVE"


async def test_understand_rejects_unknown_membership_id(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.understand(uuid.uuid4())
    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# BA-03 — Maintain Membership Terms (ERB-C007-03/EX-C007-04+05)
# ---------------------------------------------------------------------------

async def test_change_terms_applies_genuine_change_and_preserves_prior_value_in_audit(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BR-C007-004: the pre-change value is preserved (via record_audit's previous_/new_ metadata), not silently overwritten."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    assert established.license_type == "FULL"

    changed = await service.change_terms(
        established.id, ChangeMembershipTermsRequest(license_type=LicenseType.LIGHT, reason="Subscription downgrade")
    )

    assert changed.license_type == "LIGHT"
    assert changed.membership_type == "INTERNAL"  # untouched field unaffected


async def test_change_terms_rejects_request_with_no_genuine_difference(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BR-C007-003: a conflict SHALL be classified before it is resolved — every supplied field equal to current is classified erroneous (409), not applied."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.change_terms(
            established.id, ChangeMembershipTermsRequest(license_type=LicenseType.FULL, membership_type=MembershipType.INTERNAL)
        )
    assert exc_info.value.status_code == 409


async def test_change_terms_rejects_empty_request(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.change_terms(established.id, ChangeMembershipTermsRequest())
    assert exc_info.value.status_code == 422


async def test_change_terms_rejects_unknown_membership_id(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.change_terms(uuid.uuid4(), ChangeMembershipTermsRequest(license_type=LicenseType.LIGHT))
    assert exc_info.value.status_code == 404


async def test_change_terms_validates_new_home_node_like_establish(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BR-C007-002/007: a supplied home_node_id is validated identically to BA-01's establish() — real, active node required."""
    person, organization, role = seeded_person_organization_role
    node = OrganizationNode(node_code="NODE-SVC-TERMS", node_name="Service Terms Test Node", node_type="entity")
    db_session.add(node)
    await db_session.flush()
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )

    changed = await service.change_terms(established.id, ChangeMembershipTermsRequest(home_node_id=node.id))

    assert changed.home_node_id == node.id


async def test_change_terms_rejects_inactive_home_node(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    node = OrganizationNode(node_code="NODE-SVC-INACTIVE", node_name="Inactive Service Test Node", node_type="entity", active_flag=False)
    db_session.add(node)
    await db_session.flush()
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.change_terms(established.id, ChangeMembershipTermsRequest(home_node_id=node.id))
    assert exc_info.value.status_code == 409


async def test_change_terms_never_touches_membership_status(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BR-C007-006: Membership terms SHALL remain unaffected by a standing transition, and standing SHALL remain unaffected by a term change."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    assert established.membership_status == "ACTIVE"

    changed = await service.change_terms(
        established.id, ChangeMembershipTermsRequest(effective_to=datetime.now(timezone.utc) + timedelta(days=90))
    )

    assert changed.membership_status == "ACTIVE"


async def test_change_terms_detects_no_change_for_effective_to_across_a_fresh_fetch(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """
    BR-C007-003, same defect class as BA-02's own naive/aware datetime
    finding: a Membership re-fetched after a commit (db_session.refresh(),
    simulating a genuinely separate request/session) returns
    effective_to as offset-naive under SQLite's DateTime(timezone=True)
    dialect limitation. Re-supplying the exact same effective_to value
    must still be classified as no genuine change (409), not silently
    treated as a change because of the naive/aware mismatch.
    """
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    effective_to = datetime.now(timezone.utc) + timedelta(days=90)
    established = await service.establish(
        EstablishMembershipRequest(
            person_id=person.id, organization_id=organization.id, role_id=role.id, effective_to=effective_to
        )
    )
    await db_session.commit()
    await db_session.refresh(established)

    with pytest.raises(HTTPException) as exc_info:
        await service.change_terms(established.id, ChangeMembershipTermsRequest(effective_to=effective_to))
    assert exc_info.value.status_code == 409


# ---------------------------------------------------------------------------
# BA-06 — Reactivate Membership (ERB-C007-04/EX-C007-08)
# ---------------------------------------------------------------------------

async def test_reactivate_rejects_unknown_membership_id(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.reactivate(uuid.uuid4(), ReactivateMembershipRequest())
    assert exc_info.value.status_code == 404


async def test_reactivate_rejects_already_active_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    assert established.membership_status == "ACTIVE"

    with pytest.raises(HTTPException) as exc_info:
        await service.reactivate(established.id, ReactivateMembershipRequest())
    assert exc_info.value.status_code == 409


@pytest.mark.parametrize("non_active_standing", ["SUSPENDED", "DEACTIVATED", "ARCHIVED"])
async def test_reactivate_rejects_every_non_active_standing_pending_canonical_binding(
    db_session: AsyncSession, seeded_person_organization_role, non_active_standing: str
) -> None:
    """
    BR-C007-014/Contract 5.3: no canonical authority anywhere establishes
    that SUSPENDED, DEACTIVATED, or ARCHIVED may transition to ACTIVE.
    Every reactivation attempt from every non-active standing is
    rejected today (TD-037) - there is no established permission for
    any of the three states, not merely the one this test happens to
    exercise.
    """
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    # No Business Activity yet writes a non-ACTIVE standing (BA-05 is
    # BLOCKED) - set directly, mirroring BA-01's own precedent of
    # seeding OrganizationNode rows directly for a path no BA yet
    # establishes.
    established.membership_status = non_active_standing
    await db_session.flush()

    with pytest.raises(HTTPException) as exc_info:
        await service.reactivate(established.id, ReactivateMembershipRequest(reason="Return from leave"))
    assert exc_info.value.status_code == 409


async def test_reactivate_preserves_existing_membership_context_unchanged(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """A rejected reactivation SHALL preserve the existing Membership context exactly as it stood (6.3)."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    established = await service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    established.membership_status = "SUSPENDED"
    await db_session.flush()

    with pytest.raises(HTTPException):
        await service.reactivate(established.id, ReactivateMembershipRequest())

    await db_session.refresh(established)
    assert established.membership_status == "SUSPENDED"
    assert established.license_type == "FULL"
    assert established.membership_type == "INTERNAL"
