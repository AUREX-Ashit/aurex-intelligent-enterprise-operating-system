from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from models.domain_permission import DomainPermissionLevel


# ---------------------------------------------------------------------------
# BA-01 — Evaluate Access for a Governed Request (Unresolved/Deferred only,
# per IRA-005 S12's own authorized scope)
# ---------------------------------------------------------------------------

class EvaluateAccessRequest(BaseModel):
    """
    Request body for BA-01 (Evaluate Access for a Governed Request),
    realizing PE-001-C002's ERB-C002-01. Names the Membership whose
    access is being evaluated and the Domain/permission_level the
    governed request requires.
    """
    membership_id: UUID = Field(..., description="The Membership the access decision is evaluated for.")
    domain_id: UUID = Field(..., description="The Domain the requested permission_level applies to.")
    permission_level: DomainPermissionLevel = Field(..., description="One of URA-001-47's eight standing-authority levels.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "membership_id": "44444444-4444-4444-4444-444444444444",
                "domain_id": "55555555-5555-5555-5555-555555555555",
                "permission_level": "EDIT",
            }
        }
    }


class AccessEvaluationOutcomeResponse(BaseModel):
    """The Access Evaluation Outcome (AEO-000001) produced by BA-01."""
    id: UUID
    membership_id: UUID
    domain_id: UUID
    permission_level: str
    outcome_type: str
    validity_status: str
    reason: str
    approval_authority_id: UUID | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# BA-02 — Preserve and Bound Access Evaluation Outcome Validity
# ---------------------------------------------------------------------------

class PreserveAccessEvaluationOutcomeRequest(BaseModel):
    """Request body for BA-02's Preserve action (EX-C002-05) -- no fields beyond the path id; preservation is a pure state transition."""
    model_config = {"json_schema_extra": {"example": {}}}


class ExpireAccessEvaluationOutcomeRequest(BaseModel):
    """Request body for BA-02's Expire action (EX-C002-06) -- no fields beyond the path id; expiry is a pure state transition."""
    model_config = {"json_schema_extra": {"example": {}}}


# ---------------------------------------------------------------------------
# BA-03 — Detect and Resolve Access Context Change (classification/detection
# portion only, per IRA-005 S12 -- the "re-resolve to a fresh determination"
# path inherits BA-01's own excluded Permitted/Denied branches)
# ---------------------------------------------------------------------------

class DetectAccessContextChangeRequest(BaseModel):
    """
    Request body for BA-03 (Detect and Resolve Access Context Change,
    EX-C002-07). Records the governing fact that changed; this Business
    Activity classifies whether the existing outcome requires
    invalidation -- it does not itself re-evaluate to a fresh
    Permitted/Denied/Unresolved/Deferred determination (out of this
    Work Package's own authorized scope, IRA-005 S12).
    """
    changed_fact: str = Field(
        ..., min_length=1, max_length=500,
        description="The governing fact that changed, e.g. 'membership_status changed to SUSPENDED'.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {"changed_fact": "Membership standing changed from ACTIVE to SUSPENDED."}
        }
    }


class AccessContextChangeOutcome(BaseModel):
    """Result of BA-03's own classification (EX-C002-07's Context Produced)."""
    outcome_id: UUID
    invalidated: bool
    changed_fact: str
    checked_at: datetime
    re_evaluation_required: bool = Field(
        True, description="Always true when invalidated=True -- a fresh BA-01 call is the caller's own next step, never auto-triggered here."
    )

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# BA-04 — Resolve Dependent Capability Access Hand-off Rejection
# (mirrors WP-02 BA-10's own HandoffRejectionClassification pattern)
# ---------------------------------------------------------------------------

class AccessHandoffRejectionClassification(str, Enum):
    """
    Contract 5.6/BR-C002-05's own two-value classification for a
    dependent capability's rejection of a produced Access Evaluation
    Outcome hand-off -- mirrors WP-02 BA-10's own
    HandoffRejectionClassification exactly, applied here to C-002's own
    Access Evaluation Outcome instead of C-003's authorization policy
    objects.
    """
    CAPABILITY_SCOPED_INSUFFICIENCY = "CAPABILITY_SCOPED_INSUFFICIENCY"
    INTEGRITY_SIGNAL = "INTEGRITY_SIGNAL"


class ReportAccessHandoffRejectionRequest(BaseModel):
    """
    Request body for BA-04 (Resolve Dependent Capability Access
    Hand-off Rejection, EX-C002-08). The reporting capability's own
    stated reason is recorded for audit traceability but never used to
    decide the classification itself (mirrors WP-02 BA-10's own
    Contract 5.7 discipline, applied here to Contract 5.6).
    """
    reporting_capability: str = Field(
        ..., min_length=1, max_length=50,
        description="The capability reporting the rejection, e.g. 'C-007' (Membership Management).",
    )
    stated_reason: str = Field(
        ..., min_length=1, max_length=1000,
        description="The reporting capability's own explicit stated rejection reason -- recorded, never independently adjudicated as this Business Activity's own classification basis.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "reporting_capability": "C-007",
                "stated_reason": "Membership context no longer matches the outcome's own anchor.",
            }
        }
    }


class AccessHandoffRejectionOutcome(BaseModel):
    """Result of BA-04 (EX-C002-08's own Context Produced)."""
    outcome_id: UUID
    classification: AccessHandoffRejectionClassification
    object_preserved: bool = Field(..., description="True only for CAPABILITY_SCOPED_INSUFFICIENCY -- the object is preserved unchanged.")
    explanation: str = Field(..., description="The exact basis for the classification, computed from the outcome's own current validity_status -- never from the reporting capability's stated reason.")
    routed_to: str | None = Field(None, description="Populated only for INTEGRITY_SIGNAL -- names the governing Business Activity (BA-01) the correction is routed to.")
    checked_at: datetime

    model_config = {"from_attributes": True}
