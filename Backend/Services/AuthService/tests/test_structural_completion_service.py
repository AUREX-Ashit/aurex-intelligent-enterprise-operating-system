import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.structural_completion_repository import StructuralCompletionRepository
from repositories.structural_validation_repository import StructuralValidationRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from repositories.structural_review_repository import StructuralReviewRepository
from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.structural_completion import CompleteStructuralTransitionRequest
from schemas.structural_validation import ValidateTransitionReadinessRequest
from schemas.structural_review import CreateStructuralReviewRequest, ResolveStructuralReviewConcernsRequest
from schemas.structural_change_intent import FrameStructuralChangeIntentRequest
from schemas.organization_node import EstablishOrganizationNodeRequest
from schemas.structural_proposal import ShapeStructuralProposalRequest
from services.structural_completion_service import StructuralCompletionService
from services.structural_validation_service import StructuralValidationService
from services.structural_review_service import StructuralReviewService
from services.structural_change_intent_service import StructuralChangeIntentService
from services.organization_node_service import OrganizationNodeService
from services.structural_proposal_service import StructuralProposalService


def _service(session: AsyncSession) -> StructuralCompletionService:
    return StructuralCompletionService(
        StructuralCompletionRepository(session),
        StructuralValidationRepository(session),
    )


async def _seed_validation(session: AsyncSession, node_code: str = "APAC-HOLD-501"):
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
    review_service = StructuralReviewService(StructuralReviewRepository(session), StructuralProposalRepository(session))
    review = await review_service.create_review(
        CreateStructuralReviewRequest(structural_proposal_id=proposal.id, review_position="Supportive.")
    )
    resolved_review = await review_service.resolve_concerns(review.id, ResolveStructuralReviewConcernsRequest())
    validation_service = StructuralValidationService(
        StructuralValidationRepository(session),
        StructuralProposalRepository(session),
        StructuralReviewRepository(session),
    )
    validation = await validation_service.validate_transition_readiness(
        ValidateTransitionReadinessRequest(
            structural_proposal_id=proposal.id, structural_review_id=resolved_review.id
        )
    )
    return validation


async def test_complete_structural_transition_creates_completion(db_session: AsyncSession) -> None:
    """Business Activity Contract (WP-04 BA-08, ADR-013, IRA-004 §27): a valid validation yields a CREATED completion."""
    validation = await _seed_validation(db_session)
    service = _service(db_session)

    completion = await service.complete_structural_transition(
        CompleteStructuralTransitionRequest(
            structural_validation_id=validation.id,
            completion_notes="Structural transition completed.",
        ),
        actor_id="platform-admin-1",
    )

    assert completion.id is not None
    assert completion.structural_validation_id == validation.id
    assert completion.completion_notes == "Structural transition completed."
    assert completion.status == "CREATED"


async def test_complete_structural_transition_allows_notes_to_be_omitted(db_session: AsyncSession) -> None:
    validation = await _seed_validation(db_session, node_code="APAC-HOLD-502")
    service = _service(db_session)

    completion = await service.complete_structural_transition(
        CompleteStructuralTransitionRequest(structural_validation_id=validation.id)
    )

    assert completion.completion_notes is None


async def test_complete_structural_transition_rejects_unknown_validation(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.complete_structural_transition(
            CompleteStructuralTransitionRequest(structural_validation_id=uuid.uuid4())
        )

    assert exc_info.value.status_code == 404


async def test_complete_structural_transition_rejects_duplicate_completion(db_session: AsyncSession) -> None:
    """Guarded transition, not idempotent — a second completion attempt is a 409, per this Business Activity's own documented decision."""
    validation = await _seed_validation(db_session, node_code="APAC-HOLD-503")
    service = _service(db_session)
    await service.complete_structural_transition(
        CompleteStructuralTransitionRequest(structural_validation_id=validation.id)
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.complete_structural_transition(
            CompleteStructuralTransitionRequest(structural_validation_id=validation.id)
        )

    assert exc_info.value.status_code == 409


async def test_complete_structural_transition_does_not_mutate_organization_node(db_session: AsyncSession) -> None:
    """
    Option A scope, verified directly: completing a transition leaves
    the target OrganizationNode's own fields untouched.
    """
    node_repo = OrganizationNodeRepository(db_session)
    validation = await _seed_validation(db_session, node_code="APAC-HOLD-504")
    proposal_repo = StructuralProposalRepository(db_session)
    validation_row = await StructuralValidationRepository(db_session).get_by_id(validation.id)
    proposal = await proposal_repo.get_by_id(validation_row.structural_proposal_id)
    node_before = await node_repo.get_by_id(proposal.target_organization_node_id)
    snapshot = (node_before.node_name, node_before.operational_status, node_before.active_flag)

    service = _service(db_session)
    await service.complete_structural_transition(
        CompleteStructuralTransitionRequest(structural_validation_id=validation.id)
    )

    node_after = await node_repo.get_by_id(proposal.target_organization_node_id)
    assert (node_after.node_name, node_after.operational_status, node_after.active_flag) == snapshot


# ---------------------------------------------------------------------------
# BA-09 — Continue from Resulting Structure
# ---------------------------------------------------------------------------

async def test_get_details_returns_the_completed_structural_transition(db_session: AsyncSession) -> None:
    """BA-09: fetching by id returns exactly the completion created by BA-08's own complete_structural_transition()."""
    validation = await _seed_validation(db_session, node_code="APAC-HOLD-505")
    service = _service(db_session)
    created = await service.complete_structural_transition(
        CompleteStructuralTransitionRequest(
            structural_validation_id=validation.id, completion_notes="Completed."
        )
    )

    fetched = await service.get_details(created.id)

    assert fetched.id == created.id
    assert fetched.structural_validation_id == validation.id
    assert fetched.completion_notes == "Completed."
    assert fetched.status == "CREATED"


async def test_get_details_raises_404_for_unknown_id(db_session: AsyncSession) -> None:
    """BA-09: a well-formed but non-existent id is a 404, not a 500 or an empty success."""
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_details(uuid.uuid4())

    assert exc_info.value.status_code == 404
