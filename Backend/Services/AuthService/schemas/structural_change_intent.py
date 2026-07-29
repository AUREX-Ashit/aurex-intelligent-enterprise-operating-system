from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FrameStructuralChangeIntentRequest(BaseModel):
    """
    Request body for Frame Structural Change Intent (WP-04 BA-03, C-005,
    ERB-C005-03/EX-C005-04). Fields mirror StructuralChangeIntent's own
    persisted columns exactly — no field is invented beyond what the
    model persists, and no structural-target field is accepted (that
    binding is BA-04's own future scope, per the model's own docstring).
    """
    change_rationale: str = Field(..., min_length=1, description="The recognized change need / business rationale for the structural change")
    target_outcome: str = Field(..., min_length=1, description="The intended structural result (enterprise intent, not yet a Proposed Outcome Context)")
    decision_boundary: str | None = Field(None, description="Optional constraints or limits on the change")

    model_config = {
        "json_schema_extra": {
            "example": {
                "change_rationale": "APAC Holding's reporting structure no longer reflects the post-acquisition entity footprint.",
                "target_outcome": "Consolidate the three newly-acquired APAC entities under a single regional holding node.",
                "decision_boundary": "Must not alter any existing EU or Americas structural relationships.",
            }
        }
    }


class StructuralChangeIntentResponse(BaseModel):
    """Frame Structural Change Intent's success response."""
    id: UUID
    change_rationale: str
    target_outcome: str
    decision_boundary: str | None
    status: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
