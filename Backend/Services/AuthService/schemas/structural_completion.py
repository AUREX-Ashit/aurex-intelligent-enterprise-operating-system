from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CompleteStructuralTransitionRequest(BaseModel):
    """
    Request body for Complete Structural Transition (WP-04 BA-08, C-005,
    ERB-C005-08/EX-C005-11). structural_validation_id references the
    exact validated proposal revision being completed (GS-INV-012).
    """
    structural_validation_id: UUID = Field(..., description="The validation being completed — must exist and not already be completed")
    completion_notes: str | None = Field(None, description="Optional notes about the completion outcome")

    model_config = {
        "json_schema_extra": {
            "example": {
                "structural_validation_id": "11111111-1111-1111-1111-111111111111",
                "completion_notes": "Structural transition completed and communicated to affected stakeholders.",
            }
        }
    }


class StructuralCompletionResponse(BaseModel):
    """Complete Structural Transition's success response."""
    id: UUID
    structural_validation_id: UUID
    completion_notes: str | None
    status: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
