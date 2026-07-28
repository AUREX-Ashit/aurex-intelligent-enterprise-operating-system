from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from models.runtime_assignment_policy import AssignmentTargetType

DEFAULT_LIFECYCLE_STATES: list[str] = [
    "CREATED",
    "ASSIGNED",
    "ACCEPTED",
    "IN_PROGRESS",
    "COMPLETED",
    "REJECTED",
    "ESCALATED",
    "EXPIRED",
    "ARCHIVED",
]
"""URA-001-78's nine default lifecycle states."""


class EstablishRuntimeAssignmentPolicyRequest(BaseModel):
    """
    Request body for Establish Runtime Assignment Policy (BA-05, WP-02 /
    C-003, realizing ERB-C003-01 / EX-C003-05). Fields mirror
    runtime_assignment_policy_registry's columns exactly (Master Technical
    Architecture, URA-001-75/77/78/80/94/94a).
    """
    organization_id: UUID = Field(..., description="The Organization this policy is established for.")
    policy_name: str = Field(..., min_length=1, max_length=255, description="Descriptive label for the policy.")
    assignment_target_type: AssignmentTargetType = Field(
        ..., description="Exactly one of URA-001-75's four assignment-target types."
    )
    configured_lifecycle_states: list[str] | None = Field(
        None,
        description=(
            "URA-001-78's configured lifecycle states. Defaults to the nine "
            "canonical states (CREATED/ASSIGNED/ACCEPTED/IN_PROGRESS/COMPLETED/"
            "REJECTED/ESCALATED/EXPIRED/ARCHIVED) when omitted; organizations "
            "may supply a superset to add tenant-defined states such as "
            "BOARD_APPROVED."
        ),
    )
    escalation_policy_id: UUID | None = Field(
        None,
        description="Reference to an existing Escalation Policy (URA-001-80/94/94a). Populated only where escalation is configured.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "organization_id": "33333333-3333-3333-3333-333333333333",
                "policy_name": "Revenue CDE Review Assignment Policy",
                "assignment_target_type": "BUSINESS_ROLE",
            }
        }
    }

    @field_validator("configured_lifecycle_states")
    @classmethod
    def _validate_states_non_empty(cls, value: list[str] | None) -> list[str] | None:
        if value is not None and len(value) == 0:
            raise ValueError("configured_lifecycle_states, if supplied, must not be empty.")
        return value


class VersionRuntimeAssignmentPolicyRequest(BaseModel):
    """
    Request body for Version and Re-effective-Date Authorization Policy
    Object (BA-07, WP-02 / C-003, realizing ERB-C003-02 / EX-C003-07),
    applied to Runtime Assignment Policy. Amendable fields are metadata
    only (policy_name, configured_lifecycle_states, escalation_policy_id)
    — assignment_target_type (BR-C003-01's structural rule) is not
    amendable here, per EX-C003-07's own Trigger scope: "does not change
    its fundamental type or structural rule conformance."
    """
    policy_name: str | None = Field(None, min_length=1, max_length=255, description="Amended policy name. Omit to leave unchanged.")
    configured_lifecycle_states: list[str] | None = Field(None, description="Amended lifecycle-states set (URA-001-78). Omit to leave unchanged.")
    escalation_policy_id: UUID | None = Field(None, description="Amended escalation reference. Omit to leave unchanged.")
    effective_from: datetime | None = Field(None, description="Defaults to now if omitted.")
    effective_to: datetime | None = Field(None, description="NULL = open-ended.")
    approval_reference: str | None = Field(None, max_length=255, description="Optional free-text reference to the authority approving this version (SD-002-011).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "policy_name": "Revenue CDE Review Assignment Policy (Revised)",
            }
        }
    }

    @field_validator("configured_lifecycle_states")
    @classmethod
    def _validate_states_non_empty(cls, value: list[str] | None) -> list[str] | None:
        if value is not None and len(value) == 0:
            raise ValueError("configured_lifecycle_states, if supplied, must not be empty.")
        return value


class RuntimeAssignmentPolicyResponse(BaseModel):
    """Establish Runtime Assignment Policy's success response."""
    id: UUID
    organization_id: UUID
    policy_name: str
    assignment_target_type: str
    configured_lifecycle_states: list[str]
    escalation_policy_id: UUID | None
    version: int
    status: str
    effective_from: datetime
    effective_to: datetime | None
    approval_reference: str | None
    supersedes_id: UUID | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
