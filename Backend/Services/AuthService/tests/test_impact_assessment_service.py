import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.impact_assessment_repository import ImpactAssessmentRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.impact_assessment import AssessStructuralConsequenceRequest
from schemas.structural_change_intent import FrameStructuralChangeIntentRequest
from schemas.organization_node import EstablishOrganizationNodeRequest
from schemas.structural_proposal import ShapeStructuralProposalRequest
from services.impact_assessment_service import ImpactAssessmentService
from services.structural_change_intent_service import StructuralChangeIntentService
from services.organization_node_service import OrganizationNodeService
from services.structural_proposal_service import StructuralProposalService


def _service(session: AsyncSession) -> ImpactAssessmentService:
    return ImpactAssessmentService(
        ImpactAssessmentRepository(session),
        StructuralProposalRepository(session),
    )


async def _seed_proposal(session: AsyncSession, node_code: str = "APAC-HOLD-201"):
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


async def test_assess_structural_consequence_creates_impact_assessment(db_session: AsyncSession) -> None:
    """Business Activity Contract (WP-04 BA-05, ADR-009, IRA-004 §23): a valid assessment is persisted with status CREATED."""
    proposal = await _seed_proposal(db_session)
    service = _service(db_session)

    assessment = await service.assess_structural_consequence(
        AssessStructuralConsequenceRequest(
            structural_proposal_id=proposal.id,
            impact_description="Consolidation affects three existing reporting relationships.",
            uncertainty_notes="Downstream reporting currency mapping not yet confirmed.",
            downstream_implications="May require a Membership home-node review.",
        ),
        actor_id="platform-admin-1",
    )

    assert assessment.id is not None
    assert assessment.structural_proposal_id == proposal.id
    assert assessment.impact_description == "Consolidation affects three existing reporting relationships."
    assert assessment.uncertainty_notes == "Downstream reporting currency mapping not yet confirmed."
    assert assessment.downstream_implications == "May require a Membership home-node review."
    assert assessment.status == "CREATED"


async def test_assess_structural_consequence_allows_optional_fields_to_be_omitted(db_session: AsyncSession) -> None:
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-202")
    service = _service(db_session)

    assessment = await service.assess_structural_consequence(
        AssessStructuralConsequenceRequest(
            structural_proposal_id=proposal.id,
            impact_description="Minimal impact description.",
        )
    )

    assert assessment.uncertainty_notes is None
    assert assessment.downstream_implications is None


async def test_assess_structural_consequence_rejects_unknown_structural_proposal(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.assess_structural_consequence(
            AssessStructuralConsequenceRequest(
                structural_proposal_id=uuid.uuid4(),
                impact_description="Minimal impact description.",
            )
        )

    assert exc_info.value.status_code == 404


async def test_assess_structural_consequence_does_not_deduplicate_identical_requests(db_session: AsyncSession) -> None:
    """No natural business key — two assessments against the same proposal each create their own distinct row."""
    proposal = await _seed_proposal(db_session, node_code="APAC-HOLD-203")
    service = _service(db_session)
    request = AssessStructuralConsequenceRequest(
        structural_proposal_id=proposal.id,
        impact_description="Minimal impact description.",
    )

    first = await service.assess_structural_consequence(request)
    second = await service.assess_structural_consequence(request)

    assert first.id != second.id
