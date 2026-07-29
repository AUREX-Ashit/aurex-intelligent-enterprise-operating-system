import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.structural_proposal_repository import StructuralProposalRepository
from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.structural_change_intent import FrameStructuralChangeIntentRequest
from schemas.organization_node import EstablishOrganizationNodeRequest
from schemas.structural_proposal import ShapeStructuralProposalRequest, RefineStructuralProposalRequest
from services.structural_change_intent_service import StructuralChangeIntentService
from services.organization_node_service import OrganizationNodeService
from services.structural_proposal_service import StructuralProposalService


def _service(session: AsyncSession) -> StructuralProposalService:
    return StructuralProposalService(
        StructuralProposalRepository(session),
        StructuralChangeIntentRepository(session),
        OrganizationNodeRepository(session),
    )


async def _seed_intent_and_node(session: AsyncSession, node_code: str = "APAC-HOLD-101"):
    intent = await StructuralChangeIntentService(StructuralChangeIntentRepository(session)).frame_change_intent(
        FrameStructuralChangeIntentRequest(
            change_rationale="Observed structural gap.",
            target_outcome="Target structural outcome.",
        )
    )
    node = await OrganizationNodeService(OrganizationNodeRepository(session)).establish(
        EstablishOrganizationNodeRequest(node_code=node_code, node_name="APAC Holding", node_type="HOLDING")
    )
    return intent, node


async def test_shape_proposal_creates_revision_one(db_session: AsyncSession) -> None:
    """Business Activity Contract (WP-04 BA-04, ADR-008, IRA-004 §22): Shape creates revision 1, proposal_id == id."""
    intent, node = await _seed_intent_and_node(db_session)
    service = _service(db_session)

    proposal = await service.shape_proposal(
        ShapeStructuralProposalRequest(
            structural_change_intent_id=intent.id,
            target_organization_node_id=node.id,
            proposed_outcome_description="Consolidate under this holding node.",
        ),
        actor_id="platform-admin-1",
    )

    assert proposal.id is not None
    assert proposal.proposal_id == proposal.id
    assert proposal.revision_number == 1
    assert proposal.status == "CREATED"
    assert proposal.structural_change_intent_id == intent.id
    assert proposal.target_organization_node_id == node.id
    assert proposal.proposed_outcome_description == "Consolidate under this holding node."


async def test_shape_proposal_rejects_unknown_structural_change_intent(db_session: AsyncSession) -> None:
    _, node = await _seed_intent_and_node(db_session, node_code="APAC-HOLD-102")
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.shape_proposal(
            ShapeStructuralProposalRequest(
                structural_change_intent_id=uuid.uuid4(),
                target_organization_node_id=node.id,
                proposed_outcome_description="Consolidate under this holding node.",
            )
        )

    assert exc_info.value.status_code == 404


async def test_shape_proposal_rejects_unknown_organization_node(db_session: AsyncSession) -> None:
    intent, _ = await _seed_intent_and_node(db_session, node_code="APAC-HOLD-103")
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.shape_proposal(
            ShapeStructuralProposalRequest(
                structural_change_intent_id=intent.id,
                target_organization_node_id=uuid.uuid4(),
                proposed_outcome_description="Consolidate under this holding node.",
            )
        )

    assert exc_info.value.status_code == 404


async def test_refine_proposal_creates_revision_two_and_supersedes_revision_one(db_session: AsyncSession) -> None:
    """
    Append-only Versioning Policy (IRA-004 §22): Refine inserts a new
    row (revision 2) and marks revision 1 SUPERSEDED — revision 1's own
    content is never altered.
    """
    intent, node = await _seed_intent_and_node(db_session, node_code="APAC-HOLD-104")
    service = _service(db_session)
    revision_one = await service.shape_proposal(
        ShapeStructuralProposalRequest(
            structural_change_intent_id=intent.id,
            target_organization_node_id=node.id,
            proposed_outcome_description="Original description.",
        )
    )

    revision_two = await service.refine_proposal(
        revision_one.proposal_id,
        RefineStructuralProposalRequest(proposed_outcome_description="Refined description."),
        actor_id="platform-admin-1",
    )

    assert revision_two.id != revision_one.id
    assert revision_two.proposal_id == revision_one.proposal_id
    assert revision_two.revision_number == 2
    assert revision_two.status == "CREATED"
    assert revision_two.proposed_outcome_description == "Refined description."
    assert revision_two.structural_change_intent_id == intent.id
    assert revision_two.target_organization_node_id == node.id

    refreshed_revision_one = await service.structural_proposal_repo.get_by_id(revision_one.id)
    assert refreshed_revision_one.status == "SUPERSEDED"
    assert refreshed_revision_one.proposed_outcome_description == "Original description."


async def test_refine_proposal_rejects_unknown_proposal_id(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.refine_proposal(
            uuid.uuid4(),
            RefineStructuralProposalRequest(proposed_outcome_description="Refined description."),
        )

    assert exc_info.value.status_code == 404


async def test_refine_proposal_operates_on_the_current_revision_after_multiple_refinements(
    db_session: AsyncSession,
) -> None:
    """A third revision supersedes the second, not the first — get_current_revision() always resolves the latest."""
    intent, node = await _seed_intent_and_node(db_session, node_code="APAC-HOLD-105")
    service = _service(db_session)
    revision_one = await service.shape_proposal(
        ShapeStructuralProposalRequest(
            structural_change_intent_id=intent.id,
            target_organization_node_id=node.id,
            proposed_outcome_description="v1",
        )
    )
    revision_two = await service.refine_proposal(
        revision_one.proposal_id, RefineStructuralProposalRequest(proposed_outcome_description="v2")
    )

    revision_three = await service.refine_proposal(
        revision_two.proposal_id, RefineStructuralProposalRequest(proposed_outcome_description="v3")
    )

    assert revision_three.revision_number == 3
    refreshed_revision_two = await service.structural_proposal_repo.get_by_id(revision_two.id)
    refreshed_revision_one = await service.structural_proposal_repo.get_by_id(revision_one.id)
    assert refreshed_revision_two.status == "SUPERSEDED"
    assert refreshed_revision_one.status == "SUPERSEDED"
