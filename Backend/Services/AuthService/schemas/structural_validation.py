from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ValidateTransitionReadinessRequest(BaseModel):
    """
    Request body for Validate Transition Readiness (WP-04 BA-07, C-005,
    ERB-C005-07/EX-C005-10). structural_proposal_id references one
    specific proposal revision; structural_review_id references the
    review of that same revision, whose CONCERNS_RESOLVED status is
    hard-enforced (BR-C005-007) before a Validation Context row is
    created.
    """
    structural_proposal_id: UUID = Field(..., description="The specific proposal revision being validated")
    structural_review_id: UUID = Field(..., description="The review of that same proposal revision — must be CONCERNS_RESOLVED")
    readiness_notes: str | None = Field(None, description="Optional notes about the validation outcome")

    model_config = {
        "json_schema_extra": {
            "example": {
                "structural_proposal_id": "11111111-1111-1111-1111-111111111111",
                "structural_review_id": "22222222-2222-2222-2222-222222222222",
                "readiness_notes": "All review concerns resolved; ready to complete.",
            }
        }
    }


class StructuralValidationResponse(BaseModel):
    """Validate Transition Readiness' success response."""
    id: UUID
    structural_proposal_id: UUID
    structural_review_id: UUID
    readiness_notes: str | None
    status: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
