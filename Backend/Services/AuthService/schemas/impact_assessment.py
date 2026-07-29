from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AssessStructuralConsequenceRequest(BaseModel):
    """
    Request body for Assess Structural Consequence (WP-04 BA-05, C-005,
    ERB-C005-05/EX-C005-07). structural_proposal_id references one
    specific proposal revision (structural_proposals.id), not a
    proposal_id lineage.
    """
    structural_proposal_id: UUID = Field(..., description="The specific proposal revision this assessment is computed against")
    impact_description: str = Field(..., min_length=1, description="Known consequence context — affected structural areas")
    uncertainty_notes: str | None = Field(None, description="Uncertain consequence context")
    downstream_implications: str | None = Field(None, description="Identified downstream capability implications (BR-C005-008: identified, not executed)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "structural_proposal_id": "11111111-1111-1111-1111-111111111111",
                "impact_description": "Consolidation affects three existing reporting relationships under this node.",
                "uncertainty_notes": "Downstream reporting currency mapping not yet confirmed.",
                "downstream_implications": "May require a Membership home-node review for affected personnel.",
            }
        }
    }


class ImpactAssessmentResponse(BaseModel):
    """Assess Structural Consequence's success response."""
    id: UUID
    structural_proposal_id: UUID
    impact_description: str
    uncertainty_notes: str | None
    downstream_implications: str | None
    status: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
