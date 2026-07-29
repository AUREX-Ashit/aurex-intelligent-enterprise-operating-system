import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.structural_review_repository import StructuralReviewRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.structural_review import CreateStructuralReviewRequest, ResolveStructuralReviewConcernsRequest
from schemas.structural_change_intent import FrameStructuralChangeIntentRequest
from schemas.organization_node import EstablishOrganizationNodeRequest
from schemas.structural_proposal import ShapeStructuralProposalRequest
from services.structural_review_service import StructuralReviewService
from services.structural_change_intent_service import StructuralChangeIntentService
from services.organization_node_service import OrganizationNodeService
from services.structural_proposal_service import StructuralProposalService


def _service(session: AsyncSession) -> StructuralReviewService:
    return StructuralReviewService(
        StructuralReviewRepository(session),
        StructuralProposalRepository(session),
    )


async def _seed_proposal(session: AsyncSession, node_code: str = "APAC-HOLD-301"):
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


async def test_create_review_creates_structural_review(db_session: AsyncSession) -> None:
    """Business Activity Contract (WP-04 BA-06, ADR-011, IRA-004 §25): a valid review is persisted with status CREATED."""
    proposal = await _seed_proposal(db_session)
    service = _service(db_session)

    review = await service.create_review(
        CreateStructuralReviewRequest(
            structural_proposal_id=proposal.id,
            review_position="Broadly supportive, pending confirmation.",
            concerns="Uncertain whether affected personnel require a home-node review.",
        ),
        actor_id="platform-admin-1",
    )

    assert review.id is not None
    assert review.structural_proposal_id == proposal.id
    assert review.review_position == "Broadly supportive, pending confirmation."
    assert review.concerns == "Uncertain whether affected personnel require a home-node review."
    assert review.status == "CREATED"


async def test_create_review_allows_concerns_to_be_omitted(db_session: AsyncSession) -> None:
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-302")
    service = _service(db_session)

    review = await service.create_review(
        CreateStructuralReviewRequest(
            structural_proposal_id=proposal.id,
            review_position="No concerns.",
        )
    )

    assert review.concerns is None


async def test_create_review_rejects_unknown_structural_proposal(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.create_review(
            CreateStructuralReviewRequest(
                structural_proposal_id=uuid.uuid4(),
                review_position="No concerns.",
            )
        )

    assert exc_info.value.status_code == 404


async def test_resolve_concerns_transitions_status_and_appends_resolution(db_session: AsyncSession) -> None:
    """
    Append-safe concerns (SS41.16): the original concerns text is
    preserved, not overwritten, when resolution_notes is supplied.
    """
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-303")
    service = _service(db_session)
    review = await service.create_review(
        CreateStructuralReviewRequest(
            structural_proposal_id=proposal.id,
            review_position="Broadly supportive.",
            concerns="Reporting currency mapping unconfirmed.",
        )
    )

    resolved = await service.resolve_concerns(
        review.id,
        ResolveStructuralReviewConcernsRequest(resolution_notes="Confirmed with Finance; no change required."),
        actor_id="platform-admin-1",
    )

    assert resolved.status == "CONCERNS_RESOLVED"
    assert "Reporting currency mapping unconfirmed." in resolved.concerns
    assert "Confirmed with Finance; no change required." in resolved.concerns


async def test_resolve_concerns_without_notes_only_transitions_status(db_session: AsyncSession) -> None:
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-304")
    service = _service(db_session)
    review = await service.create_review(
        CreateStructuralReviewRequest(
            structural_proposal_id=proposal.id,
            review_position="No concerns.",
        )
    )

    resolved = await service.resolve_concerns(review.id, ResolveStructuralReviewConcernsRequest())

    assert resolved.status == "CONCERNS_RESOLVED"
    assert resolved.concerns is None


async def test_resolve_concerns_rejects_unknown_review(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.resolve_concerns(uuid.uuid4(), ResolveStructuralReviewConcernsRequest())

    assert exc_info.value.status_code == 404


async def test_resolve_concerns_rejects_already_resolved_review(db_session: AsyncSession) -> None:
    """Guarded transition, not idempotent — a second resolution attempt is a 409, per this Business Activity's own documented decision."""
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-305")
    service = _service(db_session)
    review = await service.create_review(
        CreateStructuralReviewRequest(
            structural_proposal_id=proposal.id,
            review_position="No concerns.",
        )
    )
    await service.resolve_concerns(review.id, ResolveStructuralReviewConcernsRequest())

    with pytest.raises(HTTPException) as exc_info:
        await service.resolve_concerns(review.id, ResolveStructuralReviewConcernsRequest())

    assert exc_info.value.status_code == 409
