import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.structural_validation_repository import StructuralValidationRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from repositories.structural_review_repository import StructuralReviewRepository
from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.structural_validation import ValidateTransitionReadinessRequest
from schemas.structural_review import CreateStructuralReviewRequest, ResolveStructuralReviewConcernsRequest
from schemas.structural_change_intent import FrameStructuralChangeIntentRequest
from schemas.organization_node import EstablishOrganizationNodeRequest
from schemas.structural_proposal import ShapeStructuralProposalRequest
from services.structural_validation_service import StructuralValidationService
from services.structural_review_service import StructuralReviewService
from services.structural_change_intent_service import StructuralChangeIntentService
from services.organization_node_service import OrganizationNodeService
from services.structural_proposal_service import StructuralProposalService


def _service(session: AsyncSession) -> StructuralValidationService:
    return StructuralValidationService(
        StructuralValidationRepository(session),
        StructuralProposalRepository(session),
        StructuralReviewRepository(session),
    )


def _review_service(session: AsyncSession) -> StructuralReviewService:
    return StructuralReviewService(
        StructuralReviewRepository(session),
        StructuralProposalRepository(session),
    )


async def _seed_proposal(session: AsyncSession, node_code: str = "APAC-HOLD-401"):
    intent = await StructuralChangeIntentService(StructuralChangeIntentRepository(session)).frame_change_intent(
        FrameStructuralChangeIntentRequest(
            change_rationale="Observed structural gap.",
            target_outcome="Target structural outcome.",
        )
    )
    node = await OrganizationNodeService(OrganizationNodeRepository(session)).establish(
        EstablishOrganizationNodeRequest(node_code=node_code, node_name="APAC Holding", node_type="HOLDING")
    )
    proposal = await StructuralProposalService(
        StructuralProposalRepository(session),
        StructuralChangeIntentRepository(session),
        OrganizationNodeRepository(session),
    ).shape_proposal(
        ShapeStructuralProposalRequest(
            structural_change_intent_id=intent.id,
            target_organization_node_id=node.id,
            proposed_outcome_description="Consolidate under this holding node.",
        )
    )
    return proposal


async def _seed_resolved_review(session: AsyncSession, proposal_id):
    review_service = _review_service(session)
    review = await review_service.create_review(
        CreateStructuralReviewRequest(structural_proposal_id=proposal_id, review_position="Supportive.")
    )
    return await review_service.resolve_concerns(review.id, ResolveStructuralReviewConcernsRequest())


async def test_validate_transition_readiness_creates_validation(db_session: AsyncSession) -> None:
    """Business Activity Contract (WP-04 BA-07, ADR-012, IRA-004 §26): a valid, resolved review yields a CREATED validation."""
    proposal = await _seed_proposal(db_session)
    review = await _seed_resolved_review(db_session, proposal.id)
    service = _service(db_session)

    validation = await service.validate_transition_readiness(
        ValidateTransitionReadinessRequest(
            structural_proposal_id=proposal.id,
            structural_review_id=review.id,
            readiness_notes="All concerns resolved; ready.",
        ),
        actor_id="platform-admin-1",
    )

    assert validation.id is not None
    assert validation.structural_proposal_id == proposal.id
    assert validation.structural_review_id == review.id
    assert validation.readiness_notes == "All concerns resolved; ready."
    assert validation.status == "CREATED"


async def test_validate_transition_readiness_allows_notes_to_be_omitted(db_session: AsyncSession) -> None:
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-402")
    review = await _seed_resolved_review(db_session, proposal.id)
    service = _service(db_session)

    validation = await service.validate_transition_readiness(
        ValidateTransitionReadinessRequest(structural_proposal_id=proposal.id, structural_review_id=review.id)
    )

    assert validation.readiness_notes is None


async def test_validate_transition_readiness_rejects_unknown_proposal(db_session: AsyncSession) -> None:
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-403")
    review = await _seed_resolved_review(db_session, proposal.id)
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.validate_transition_readiness(
            ValidateTransitionReadinessRequest(structural_proposal_id=uuid.uuid4(), structural_review_id=review.id)
        )

    assert exc_info.value.status_code == 404


async def test_validate_transition_readiness_rejects_unknown_review(db_session: AsyncSession) -> None:
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-404")
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.validate_transition_readiness(
            ValidateTransitionReadinessRequest(structural_proposal_id=proposal.id, structural_review_id=uuid.uuid4())
        )

    assert exc_info.value.status_code == 404


async def test_validate_transition_readiness_rejects_review_for_a_different_proposal(db_session: AsyncSession) -> None:
    proposal_one = await _seed_proposal(db_session, node_code="APAC-HOLD-405")
    proposal_two = await _seed_proposal(db_session, node_code="APAC-HOLD-406")
    review_of_proposal_two = await _seed_resolved_review(db_session, proposal_two.id)
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.validate_transition_readiness(
            ValidateTransitionReadinessRequest(
                structural_proposal_id=proposal_one.id, structural_review_id=review_of_proposal_two.id
            )
        )

    assert exc_info.value.status_code == 409


async def test_validate_transition_readiness_rejects_unresolved_concerns(db_session: AsyncSession) -> None:
    """Mandatory business rule: BR-C005-007 hard-enforced — an unresolved review (still CREATED) is rejected with 409."""
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-407")
    review = await _review_service(db_session).create_review(
        CreateStructuralReviewRequest(structural_proposal_id=proposal.id, review_position="Pending review.")
    )
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.validate_transition_readiness(
            ValidateTransitionReadinessRequest(structural_proposal_id=proposal.id, structural_review_id=review.id)
        )

    assert exc_info.value.status_code == 409
    assert "BR-C005-007" in exc_info.value.detail
