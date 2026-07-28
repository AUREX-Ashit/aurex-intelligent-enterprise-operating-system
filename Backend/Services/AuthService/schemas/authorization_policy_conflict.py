from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class DependencyViolation(BaseModel):
    """
    One explicit, named business-rule violation found during Dependency
    Conflict Detection (BA-09, WP-02 / C-003, realizing ERB-C003-03 /
    EX-C003-09). Returns the exact violated rule per Contract 5.6 and
    this Business Activity's own instruction — never a generic
    validation error.
    """
    rule: str = Field(..., description="The exact violated business rule, e.g. 'BR-C003-04', 'Contract-5.4', 'Contract-5.6'.")
    description: str = Field(..., description="Human-readable statement of what was found and why it violates the named rule.")
    detail: dict | None = Field(None, description="Structured detail supporting the violation (e.g. the specific dependent, the offending dates).")


class DependencyConflictReport(BaseModel):
    """
    Result of Detect Dependency Conflict (BA-09). Realizes EX-C003-09's
    own Context Produced: "Either a cleared path for ERB-C003-02
    [BA-08] to proceed, or a held change with a named, explained
    dependency list requiring the proposing authority's explicit
    resolution."
    """
    object_type: str
    object_id: UUID
    checked_at: datetime
    has_conflicts: bool
    violations: list[DependencyViolation]
    active_dependents: list[dict] = Field(
        default_factory=list,
        description="Every currently-active dependent found (EX-C003-09: 'enumerates every currently-active dependent'), named explicitly, never a bare count.",
    )

    model_config = {"from_attributes": True}


class ResolutionType(str, Enum):
    """
    Contract 5.6's own three explicit resolution modes: "reassignment,
    natural expiry, or an affirmative accepted break stated by the
    proposing authority — never a silent default."
    """
    REASSIGNMENT_CONFIRMED = "REASSIGNMENT_CONFIRMED"
    NATURAL_EXPIRY_CONFIRMED = "NATURAL_EXPIRY_CONFIRMED"
    ACCEPTED_BREAK = "ACCEPTED_BREAK"


class ResolveDependencyConflictRequest(BaseModel):
    """
    Request body for Resolve Dependency Conflict (BA-09). Records the
    proposing authority's explicit resolution statement (Contract 5.6);
    does not itself reassign a dependent's own reference — Membership
    (C-007) and every other dependent's own record remain outside C-003's
    boundary (Contract 5.1), consumed here strictly as an
    already-resolved input once the resolution is confirmed.
    """
    resolution_type: ResolutionType = Field(..., description="Exactly one of Contract 5.6's three resolution modes.")
    reason: str = Field(..., min_length=1, max_length=1000, description="The proposing authority's stated justification — never a silent default.")
    replacement_target_id: UUID | None = Field(
        None,
        description="Required only for REASSIGNMENT_CONFIRMED: the id of the same-type, ACTIVE object dependents are being reassigned to.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "resolution_type": "ACCEPTED_BREAK",
                "reason": "Membership migrated to a successor Role via Membership Management (C-007); dependency accepted as broken.",
            }
        }
    }
