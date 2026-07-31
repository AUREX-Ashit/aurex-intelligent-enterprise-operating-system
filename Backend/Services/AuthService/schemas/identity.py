from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class IdentityContextStatus(str, Enum):
    """
    EX-C001-06's own two-outcome resolution result (Contract 5.6):
    CURRENT (the Identity's associated Person Context re-confirmed
    valid) or UNRESOLVED (it could not be). Never a third,
    candidate-selection outcome — PE-001-C001 Contract 5.4/BR-C001-04
    prohibit that.
    """
    CURRENT = "CURRENT"
    UNRESOLVED = "UNRESOLVED"


class IdentityStatusResponse(BaseModel):
    """
    Response for BA-01 — Detect and Resolve Disrupted Identity Context
    (EX-C001-06). Re-confirms currency against C-006 rather than
    trusting the last-known JWT claim state (Contract 5.6: "SHALL NOT
    infer that a disrupted or unresolved Identity Context remains valid
    absent a freshly re-resolved, affirmative confirmation").
    """
    identity_id: UUID
    person_id: UUID
    status: IdentityContextStatus
    checked_at: datetime

    model_config = {"from_attributes": True}


class RoutedPath(str, Enum):
    """
    EX-C001-07's own two named routing targets: NEW_IDENTITY
    (ERB-C001-01, excluded from WP-08's own scope, IRA-008 §4.1) or
    RE_RESOLUTION (ERB-C001-02, satisfied by construction via
    POST /auth/login, IRA-008 §4.2).
    """
    NEW_IDENTITY = "NEW_IDENTITY"
    RE_RESOLUTION = "RE_RESOLUTION"


class RecoverIdentityRequest(BaseModel):
    """
    Request body for BA-02 — Recover Inaccessible Identity Context
    (EX-C001-07), self-service scope only (IRA-008 §4.5): the caller
    requests recovery for their own person_id. Administrator-initiated
    recovery on another Person's behalf is excluded pending the Access
    Evaluation resolver IRA-008 §4.1 discloses as unavailable.
    """
    person_id: UUID = Field(..., description="The requesting Person's own id — validated against the caller's own JWT person_id claim.")
    reason: str = Field(..., min_length=1, max_length=1000, description="Why the established Identity has become unusable.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "person_id": "550e8400-e29b-41d4-a716-446655440000",
                "reason": "Lost access to the registered authentication device.",
            }
        }
    }


class IdentityRecoveryRequestResponse(BaseModel):
    """
    Result of BA-02. Realizes EX-C001-07's own Context Produced: "a
    governed recovery request record... never a completed technical
    credential reset performed by this EX itself."
    """
    id: UUID
    person_id: UUID
    routed_path: RoutedPath
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class IdentityHandoffClassification(str, Enum):
    """
    PE-001-C001 Contract 5.7's own two-value classification, mirroring
    BR-C003-06/Contract 5.7's C-003 analogue exactly (WP-02 BA-10,
    schemas/authorization_policy_handoff.py).
    """
    CAPABILITY_SCOPED_INSUFFICIENCY = "CAPABILITY_SCOPED_INSUFFICIENCY"
    INTEGRITY_SIGNAL = "INTEGRITY_SIGNAL"


class ClassifyHandoffRejectionRequest(BaseModel):
    """
    Request body for BA-03 — Resolve Dependent Capability Identity
    Hand-off Rejection (EX-C001-08). identity_id names the Identity
    Context that was handed off and rejected; stated_reason is recorded
    for audit traceability only — per Contract 5.7 ("a signal, not an
    authority") it never itself determines the classification (IRA-008
    §5, BA-03).
    """
    identity_id: UUID = Field(..., description="The Authoritative Identity Context that was handed off and rejected.")
    rejecting_capability: str = Field(..., min_length=1, max_length=50, description="The capability reporting the rejection, e.g. 'C-008'.")
    stated_reason: str = Field(..., min_length=1, max_length=1000, description="The reporting capability's own stated rejection reason — recorded, never independently adjudicated as this classification's own basis.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "identity_id": "550e8400-e29b-41d4-a716-446655440000",
                "rejecting_capability": "C-008",
                "stated_reason": "Workspace entry could not confirm the presented Identity Context.",
            }
        }
    }


class HandoffRejectionOutcome(BaseModel):
    """
    Result of BA-03. Realizes EX-C001-08's own Context Produced: "Either
    a named, capability-scoped rejection outcome with the Identity
    Context preserved, or a routed disruption signal handed to
    EX-C001-06."
    """
    identity_id: UUID
    classification: IdentityHandoffClassification
    identity_context_preserved: bool = Field(..., description="True only for CAPABILITY_SCOPED_INSUFFICIENCY.")
    routed_to: str | None = Field(None, description="Populated only for INTEGRITY_SIGNAL — names BA-01's own endpoint as the governed next step (Contract 5.7: routed to EX-C001-06, never auto-corrected here).")
    explanation: str
    checked_at: datetime

    model_config = {"from_attributes": True}
