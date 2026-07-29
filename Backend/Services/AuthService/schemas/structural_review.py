from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateStructuralReviewRequest(BaseModel):
    """
    Request body for Review Proposed Structural Outcome (WP-04 BA-06,
    C-005, ERB-C005-06/EX-C005-08). structural_proposal_id references
    one specific proposal revision (structural_proposals.id), not a
    proposal_id lineage.
    """
    structural_proposal_id: UUID = Field(..., description="The specific proposal revision this review is created against")
    review_position: str = Field(..., min_length=1, description="The reviewer's overall stance")
    concerns: str | None = Field(None, description="Contextual concerns raised during review")

    model_config = {
        "json_schema_extra": {
            "example": {
                "structural_proposal_id": "11111111-1111-1111-1111-111111111111",
                "review_position": "Broadly supportive, pending confirmation of reporting currency mapping.",
                "concerns": "Uncertain whether affected personnel require a home-node review before completion.",
            }
        }
    }


class ResolveStructuralReviewConcernsRequest(BaseModel):
    """
    Request body for Resolve Structural Review Concerns (WP-04 BA-06,
    C-005, ERB-C005-06/EX-C005-09). Updates the same Review Context row
    only — does not create or mutate any StructuralProposal revision
    (that remains exclusively BA-04's own scope).
    """
    resolution_notes: str | None = Field(None, description="Rationale for how the concerns were resolved — appended to, never overwriting, the original concerns")


class StructuralReviewResponse(BaseModel):
    """Review / Resolve Structural Review Concerns' success response."""
    id: UUID
    structural_proposal_id: UUID
    review_position: str
    concerns: str | None
    status: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
