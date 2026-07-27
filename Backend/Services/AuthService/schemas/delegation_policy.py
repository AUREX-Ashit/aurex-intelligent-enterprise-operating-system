from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from models.delegation_policy import DelegationScopeType


class EstablishDelegationPolicyRequest(BaseModel):
    """
    Request body for Establish Delegation Policy (BA-04, WP-02 / C-003,
    realizing ERB-C003-01 / EX-C003-04). Fields mirror
    delegation_policy_registry's columns exactly (Master Technical
    Architecture, URA-001-88/89/90/92).

    scope_type is validated here, not merely inferred, for the same
    reason established at BA-03: EX-C003-04's own Success Criteria
    forbids establishing a Delegation Policy "without a stated type,
    scope, and sub-delegation rule" — this validator rejects any
    combination that would leave scope ambiguous, dual-stated, or
    missing its required anchor before the request ever reaches the
    service layer.
    """
    organization_id: UUID = Field(..., description="Required for every scope, including ORGANIZATION.")
    policy_name: str = Field(..., min_length=1, max_length=255, description="Descriptive label for the policy.")
    delegation_type: str = Field(
        ..., min_length=1, max_length=100,
        description="TEMPORARY/OUT_OF_OFFICE/EMERGENCY/ACTING_ROLE/PROJECT_BASED, or a tenant-defined custom type (URA-001-90).",
    )
    scope_type: DelegationScopeType = Field(..., description="Exactly one of URA-001-89's four scopes.")
    sub_delegation_allowed: bool = Field(False, description="URA-001-92: whether further delegation of an already-delegated authority is permitted.")
    domain_id: UUID | None = Field(None, description="Required if, and only if, scope_type is DOMAIN.")
    object_type: str | None = Field(None, max_length=100, description="Required if, and only if, scope_type is OBJECT.")
    object_id: UUID | None = Field(None, description="Required if, and only if, scope_type is OBJECT.")
    event_code: str | None = Field(None, max_length=100, description="Required if, and only if, scope_type is EVENT.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "organization_id": "33333333-3333-3333-3333-333333333333",
                "policy_name": "Emergency Financial Approval Delegation",
                "delegation_type": "EMERGENCY",
                "scope_type": "ORGANIZATION",
                "sub_delegation_allowed": False,
            }
        }
    }

    @model_validator(mode="after")
    def _validate_scope_consistency(self) -> "EstablishDelegationPolicyRequest":
        if self.scope_type == DelegationScopeType.ORGANIZATION:
            if self.domain_id is not None or self.object_type is not None or self.object_id is not None or self.event_code is not None:
                raise ValueError(
                    "scope_type 'ORGANIZATION' must not include domain_id, object_type, object_id, or event_code."
                )
        elif self.scope_type == DelegationScopeType.DOMAIN:
            if self.domain_id is None:
                raise ValueError("scope_type 'DOMAIN' requires domain_id.")
            if self.object_type is not None or self.object_id is not None or self.event_code is not None:
                raise ValueError("scope_type 'DOMAIN' must not include object_type, object_id, or event_code.")
        elif self.scope_type == DelegationScopeType.OBJECT:
            if self.object_type is None or self.object_id is None:
                raise ValueError("scope_type 'OBJECT' requires both object_type and object_id.")
            if self.domain_id is not None or self.event_code is not None:
                raise ValueError("scope_type 'OBJECT' must not include domain_id or event_code.")
        elif self.scope_type == DelegationScopeType.EVENT:
            if self.event_code is None:
                raise ValueError("scope_type 'EVENT' requires event_code.")
            if self.domain_id is not None or self.object_type is not None or self.object_id is not None:
                raise ValueError("scope_type 'EVENT' must not include domain_id, object_type, or object_id.")
        return self


class DelegationPolicyResponse(BaseModel):
    """Establish Delegation Policy's success response."""
    id: UUID
    organization_id: UUID
    policy_name: str
    delegation_type: str
    scope_type: str
    sub_delegation_allowed: bool
    domain_id: UUID | None
    object_type: str | None
    object_id: UUID | None
    event_code: str | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
