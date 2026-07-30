import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.approval_authority import ApprovalAuthority
from models.domain import Domain
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role
from repositories.access_evaluation_outcome_repository import AccessEvaluationOutcomeRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from schemas.access_evaluation import (
    AccessHandoffRejectionClassification,
    DetectAccessContextChangeRequest,
    EvaluateAccessRequest,
    ReportAccessHandoffRejectionRequest,
)
from services.access_evaluation_service import AccessEvaluationService


@pytest.fixture
async def seeded_membership_and_domain(db_session: AsyncSession) -> tuple[Membership, Domain, Organization]:
    """Seeds one Person -> Organization -> Role -> Membership (ACTIVE) chain, plus one Domain."""
    person = Person(first_name="Access", last_name="Subject", display_name="Access Subject")
    organization = Organization(
        organization_code="AE-TEST-ORG",
        organization_name="Access Evaluation Test Org",
        organization_type="CORPORATE",
    )
    role = Role(role_code="AE_TEST_ROLE", role_name="Access Evaluation Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id)
    domain = Domain(domain_name="Finance")
    db_session.add_all([membership, domain])
    await db_session.flush()

    return membership, domain, organization


def _service(session: AsyncSession) -> AccessEvaluationService:
    return AccessEvaluationService(
        AccessEvaluationOutcomeRepository(session),
        MembershipRepository(session),
        DomainRepository(session),
    )


# ---------------------------------------------------------------------------
# BA-01 — Evaluate Access for a Governed Request
# ---------------------------------------------------------------------------

async def test_evaluate_rejects_unknown_domain(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    membership, _domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    request = EvaluateAccessRequest(
        membership_id=membership.id, domain_id=uuid.uuid4(), permission_level="VIEW"
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.evaluate(request)

    assert exc_info.value.status_code == 404


async def test_evaluate_produces_unresolved_outcome_for_unknown_membership(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """EX-C002-03: identity/membership standing cannot be confirmed -> UNRESOLVED."""
    _membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    request = EvaluateAccessRequest(
        membership_id=uuid.uuid4(), domain_id=domain.id, permission_level="VIEW"
    )

    outcome = await service.evaluate(request)

    assert outcome.outcome_type == "UNRESOLVED"
    assert outcome.validity_status == "CREATED"


async def test_evaluate_produces_unresolved_outcome_for_inactive_membership(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    membership, domain, _org = seeded_membership_and_domain
    membership.membership_status = "SUSPENDED"
    await db_session.flush()

    service = _service(db_session)
    request = EvaluateAccessRequest(
        membership_id=membership.id, domain_id=domain.id, permission_level="VIEW"
    )

    outcome = await service.evaluate(request)

    assert outcome.outcome_type == "UNRESOLVED"
    assert "SUSPENDED" in outcome.reason


async def test_evaluate_produces_deferred_outcome_when_approval_authority_governs_domain(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """EX-C002-04: an ACTIVE, DOMAIN-scoped Approval Authority governs the requested Domain -> DEFERRED."""
    membership, domain, organization = seeded_membership_and_domain
    approval_authority = ApprovalAuthority(
        organization_id=organization.id,
        authority_name="Finance Domain Approval",
        approval_strategy="ANY_ONE",
        scope_type="DOMAIN",
        domain_id=domain.id,
    )
    db_session.add(approval_authority)
    await db_session.flush()

    service = _service(db_session)
    request = EvaluateAccessRequest(
        membership_id=membership.id, domain_id=domain.id, permission_level="APPROVE"
    )

    outcome = await service.evaluate(request)

    assert outcome.outcome_type == "DEFERRED"
    assert outcome.approval_authority_id == approval_authority.id


async def test_evaluate_raises_501_when_no_approval_authority_governs_domain(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """
    IRA-005 S12: an ACTIVE membership with no governing Approval Authority
    would require a Permitted/Denied determination -- explicitly out of
    this Work Package's own authorized scope. Never a fabricated decision.
    """
    membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    request = EvaluateAccessRequest(
        membership_id=membership.id, domain_id=domain.id, permission_level="VIEW"
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.evaluate(request)

    assert exc_info.value.status_code == 501


# ---------------------------------------------------------------------------
# BA-02 — Preserve and Bound Access Evaluation Outcome Validity
# ---------------------------------------------------------------------------

async def test_preserve_transitions_created_to_preserved(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    _membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    outcome = await service.evaluate(
        EvaluateAccessRequest(membership_id=uuid.uuid4(), domain_id=domain.id, permission_level="VIEW")
    )

    preserved = await service.preserve(outcome.id)

    assert preserved.validity_status == "PRESERVED"


async def test_preserve_rejects_non_created_outcome(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    _membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    outcome = await service.evaluate(
        EvaluateAccessRequest(membership_id=uuid.uuid4(), domain_id=domain.id, permission_level="VIEW")
    )
    await service.preserve(outcome.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.preserve(outcome.id)

    assert exc_info.value.status_code == 409


async def test_preserve_rejects_unknown_outcome(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.preserve(uuid.uuid4())

    assert exc_info.value.status_code == 404


async def test_expire_transitions_preserved_to_expired(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    _membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    outcome = await service.evaluate(
        EvaluateAccessRequest(membership_id=uuid.uuid4(), domain_id=domain.id, permission_level="VIEW")
    )
    await service.preserve(outcome.id)

    expired = await service.expire(outcome.id)

    assert expired.validity_status == "EXPIRED"


async def test_expire_rejects_non_preserved_outcome(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """A CREATED (never preserved) outcome may not be expired directly."""
    _membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    outcome = await service.evaluate(
        EvaluateAccessRequest(membership_id=uuid.uuid4(), domain_id=domain.id, permission_level="VIEW")
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.expire(outcome.id)

    assert exc_info.value.status_code == 409


# ---------------------------------------------------------------------------
# BA-03 — Detect and Resolve Access Context Change
# ---------------------------------------------------------------------------

async def test_detect_context_change_invalidates_live_outcome(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    _membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    outcome = await service.evaluate(
        EvaluateAccessRequest(membership_id=uuid.uuid4(), domain_id=domain.id, permission_level="VIEW")
    )

    result = await service.detect_context_change(
        outcome.id, DetectAccessContextChangeRequest(changed_fact="Membership standing changed.")
    )

    assert result.invalidated is True
    assert result.re_evaluation_required is True


async def test_detect_context_change_rejects_non_live_outcome(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    _membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    outcome = await service.evaluate(
        EvaluateAccessRequest(membership_id=uuid.uuid4(), domain_id=domain.id, permission_level="VIEW")
    )
    await service.detect_context_change(
        outcome.id, DetectAccessContextChangeRequest(changed_fact="First change.")
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.detect_context_change(
            outcome.id, DetectAccessContextChangeRequest(changed_fact="Second change.")
        )

    assert exc_info.value.status_code == 409


# ---------------------------------------------------------------------------
# BA-04 — Resolve Dependent Capability Access Hand-off Rejection
# ---------------------------------------------------------------------------

async def test_resolve_handoff_rejection_classifies_live_outcome_as_capability_scoped_insufficiency(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    _membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    outcome = await service.evaluate(
        EvaluateAccessRequest(membership_id=uuid.uuid4(), domain_id=domain.id, permission_level="VIEW")
    )

    result = await service.resolve_handoff_rejection(
        outcome.id,
        ReportAccessHandoffRejectionRequest(reporting_capability="C-007", stated_reason="Scope mismatch."),
    )

    assert result.classification == AccessHandoffRejectionClassification.CAPABILITY_SCOPED_INSUFFICIENCY
    assert result.object_preserved is True
    assert result.routed_to is None


async def test_resolve_handoff_rejection_classifies_invalidated_outcome_as_integrity_signal(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """Mirrors WP-02 BA-10: the outcome's own current validity_status is the classification basis, never the reporting capability's stated reason."""
    _membership, domain, _org = seeded_membership_and_domain
    service = _service(db_session)
    outcome = await service.evaluate(
        EvaluateAccessRequest(membership_id=uuid.uuid4(), domain_id=domain.id, permission_level="VIEW")
    )
    await service.detect_context_change(
        outcome.id, DetectAccessContextChangeRequest(changed_fact="Context changed.")
    )

    result = await service.resolve_handoff_rejection(
        outcome.id,
        ReportAccessHandoffRejectionRequest(reporting_capability="C-007", stated_reason="Object looks stale."),
    )

    assert result.classification == AccessHandoffRejectionClassification.INTEGRITY_SIGNAL
    assert result.object_preserved is False
    assert result.routed_to == "BA-01 (Evaluate Access for a Governed Request)"


async def test_resolve_handoff_rejection_rejects_unknown_outcome(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.resolve_handoff_rejection(
            uuid.uuid4(),
            ReportAccessHandoffRejectionRequest(reporting_capability="C-007", stated_reason="n/a"),
        )

    assert exc_info.value.status_code == 404
