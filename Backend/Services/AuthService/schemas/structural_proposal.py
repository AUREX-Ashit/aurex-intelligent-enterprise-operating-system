from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ShapeStructuralProposalRequest(BaseModel):
    """
    Request body for Shape Structural Proposal (WP-04 BA-04, C-005,
    ERB-C005-04/EX-C005-05). Creates revision 1 of a new proposal.
    """
    structural_change_intent_id: UUID = Field(..., description="The Structural Change Intent (SCI-000001) this proposal realizes")
    target_organization_node_id: UUID = Field(..., description="The EnterpriseNode this proposal targets (ADR-007: EnterpriseNode-only v1 scope)")
    proposed_outcome_description: str = Field(..., min_length=1, description="The intended structural result")

    model_config = {
        "json_schema_extra": {
            "example": {
                "structural_change_intent_id": "11111111-1111-1111-1111-111111111111",
                "target_organization_node_id": "22222222-2222-2222-2222-222222222222",
                "proposed_outcome_description": "Consolidate the three newly-acquired APAC entities under this holding node.",
            }
        }
    }


class RefineStructuralProposalRequest(BaseModel):
    """
    Request body for Refine Structural Proposal (WP-04 BA-04, C-005,
    ERB-C005-04/EX-C005-06). Creates the next revision of an existing
    proposal. structural_change_intent_id and target_organization_node_id
    are not accepted here — BR-C005-004 requires every revision remain
    traceable to the same originating Change Intent, and the target is
    immutable across a proposal's own revisions; only the proposed
    outcome itself may be revised.
    """
    proposed_outcome_description: str = Field(..., min_length=1, description="The revised intended structural result")


class StructuralProposalResponse(BaseModel):
    """Shape/Refine Structural Proposal's success response — one revision."""
    id: UUID
    proposal_id: UUID
    revision_number: int
    structural_change_intent_id: UUID
    target_organization_node_id: UUID
    proposed_outcome_description: str
    status: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
