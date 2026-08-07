# schemas/conversation.py
"""WP-12 — AI Conversation Management (C-094). Request/response contracts for BA-01 (`TDS-012 §5`)."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ConversationResponse(BaseModel):
    """Result of BA-01's own establish and close paths."""
    conversation_id: UUID
    state: str
    state_transitioned_at: datetime
    state_transition_reason: str | None
    created_at: datetime
    closed_at: datetime | None

    model_config = {"from_attributes": True}


class CloseConversationRequest(BaseModel):
    """Request body for BA-01's own explicit close path. Reason is always EXPLICIT_ACTION for this endpoint — RUNTIME_POLICY-triggered closes (inactivity timeout) are a separate, future mechanism, not user-invoked."""
    model_config = {
        "json_schema_extra": {"example": {}}
    }


# ---------------------------------------------------------------------------
# BA-02 — Execute Interaction / BA-03 — Retrieve Conversation
# ---------------------------------------------------------------------------

class ExecuteInteractionRequest(BaseModel):
    """
    Request body for BA-02's own turn-submission path.

    `business_activity_id` is optional and generated server-side if omitted —
    no Business Activity Engine integration exists in AIService yet (a
    cross-cutting concern beyond this Work Package's own scope); accepting a
    caller-supplied value when present, generating one otherwise, is a
    disclosed placeholder for that future integration, not a real
    accountability resolution.
    """
    input_text: str = Field(..., min_length=1, max_length=4000)
    business_activity_id: UUID | None = Field(None)

    model_config = {
        "json_schema_extra": {"example": {"input_text": "What is our current enterprise structure?"}}
    }


class InteractionResponse(BaseModel):
    """Result of BA-02's own execute path, and each row in BA-03's own list path. Composes the (first real implementation of the) Evidence Panel/Confidence contract, per `IRA-012 §4.4` — fields present, honestly `None` where no real computation exists yet, never fabricated."""
    interaction_id: UUID
    conversation_id: UUID
    sequence_number: int
    status: str
    input_reference: str
    output_reference: str | None
    confidence_score: int | None
    evidence_reference: str | None
    created_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class InteractionListResponse(BaseModel):
    """BA-03's own response — ordered by sequence_number, no aggregation (`ADR-022` Decision 3)."""
    interactions: list[InteractionResponse]
