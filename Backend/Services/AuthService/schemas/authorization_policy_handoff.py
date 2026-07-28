from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.authorization_policy_conflict import DependencyConflictReport


class HandoffRejectionClassification(str, Enum):
    """
    BR-C003-06's own two-value classification (Contract 5.7). Every
    dependent-capability hand-off rejection is classified as exactly one
    of these — never left generic, never inferred from the reporting
    capability's own stated reason alone.
    """
    CAPABILITY_SCOPED_INSUFFICIENCY = "CAPABILITY_SCOPED_INSUFFICIENCY"
    INTEGRITY_SIGNAL = "INTEGRITY_SIGNAL"


class ReportHandoffRejectionRequest(BaseModel):
    """
    Request body for Resolve Dependent Capability Hand-off Rejection
    (BA-10, WP-02 / C-003, realizing ERB-C003-03 / EX-C003-10). The
    reporting capability's own stated reason is recorded for audit
    traceability (EX-C003-10's own Context Consumed) but never used to
    decide the classification itself — Contract 5.7: "The dependent
    capability's stated rejection reason is a signal, not an authority."
    """
    reporting_capability: str = Field(
        ..., min_length=1, max_length=50,
        description="The capability reporting the rejection, e.g. 'C-002' (Access Management) — open-ended, since Contract 5.7 names C-002 and 'any other dependent capability'.",
    )
    stated_reason: str = Field(
        ..., min_length=1, max_length=1000,
        description="The reporting capability's own explicit stated rejection reason (EX-C003-10's own Context Required) — recorded, never independently adjudicated as this Business Activity's own classification basis.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "reporting_capability": "C-002",
                "stated_reason": "Access evaluation could not resolve a currently-valid grant for this object.",
            }
        }
    }


class HandoffRejectionOutcome(BaseModel):
    """
    Result of Resolve Dependent Capability Hand-off Rejection (BA-10).
    Realizes EX-C003-10's own Context Produced: "Either a named,
    capability-scoped rejection outcome with the object preserved, or a
    routed correction handed to ERB-C003-01/02."
    """
    object_type: str
    object_id: UUID
    classification: HandoffRejectionClassification
    object_preserved: bool = Field(..., description="True only for CAPABILITY_SCOPED_INSUFFICIENCY (Contract 5.7: the object is preserved unchanged).")
    explanation: str = Field(..., description="The exact basis for the classification, computed from BA-08's status and BA-09's own conflict detection — never from the reporting capability's stated reason.")
    routed_to: str | None = Field(None, description="Populated only for INTEGRITY_SIGNAL — names the governing ERB the correction is routed to (never auto-corrected here, Contract 5.8).")
    conflict_report: DependencyConflictReport = Field(..., description="The underlying BA-09 report this classification was computed from — full traceability, never a bare verdict.")
    checked_at: datetime

    model_config = {"from_attributes": True}
