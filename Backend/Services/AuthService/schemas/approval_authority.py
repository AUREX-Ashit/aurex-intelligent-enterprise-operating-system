from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from models.approval_authority import ApprovalScopeType, ApprovalStrategy


class EstablishApprovalAuthorityRequest(BaseModel):
    """
    Request body for Establish Approval Authority (BA-03, WP-02 / C-003,
    realizing ERB-C003-01 / EX-C003-03). Fields mirror
    approval_authority_registry's columns exactly (Master Technical
    Architecture, URA-001-04/41/42/61/82).

    scope_type is validated here, not merely inferred: EX-C003-03's own
    Success Criteria forbids establishing an Approval Authority "without
    exactly one declared strategy and exactly one declared scope" — this
    validator rejects any combination that would leave scope ambiguous,
    dual-stated, or missing its required anchor before the request ever
    reaches the service layer.
    """
    organization_id: UUID = Field(..., description="Required for every scope, including GLOBAL/COMPANY.")
    authority_name: str = Field(..., min_length=1, max_length=255, description="Annual Report Approver, Financial Statement Approver, etc.")
    approval_strategy: ApprovalStrategy = Field(..., description="One of URA-001-42/62's four strategies.")
    majority_threshold_pct: int | None = Field(None, ge=0, le=100, description="Configurable threshold (URA-001-82).")
    scope_type: ApprovalScopeType = Field(..., description="Exactly one of URA-001-61's four scopes.")
    domain_id: UUID | None = Field(None, description="Required if, and only if, scope_type is DOMAIN.")
    object_type: str | None = Field(None, max_length=100, description="Required if, and only if, scope_type is OBJECT.")
    object_id: UUID | None = Field(None, description="Required if, and only if, scope_type is OBJECT.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "organization_id": "33333333-3333-3333-3333-333333333333",
                "authority_name": "Annual Report Approver",
                "approval_strategy": "SEQUENTIAL",
                "scope_type": "COMPANY",
            }
        }
    }

    @model_validator(mode="after")
    def _validate_scope_consistency(self) -> "EstablishApprovalAuthorityRequest":
        if self.scope_type in (ApprovalScopeType.GLOBAL, ApprovalScopeType.COMPANY):
            if self.domain_id is not None or self.object_type is not None or self.object_id is not None:
                raise ValueError(
                    f"scope_type '{self.scope_type.value}' must not include domain_id, object_type, or object_id."
                )
        elif self.scope_type == ApprovalScopeType.DOMAIN:
            if self.domain_id is None:
                raise ValueError("scope_type 'DOMAIN' requires domain_id.")
            if self.object_type is not None or self.object_id is not None:
                raise ValueError("scope_type 'DOMAIN' must not include object_type or object_id.")
        elif self.scope_type == ApprovalScopeType.OBJECT:
            if self.object_type is None or self.object_id is None:
                raise ValueError("scope_type 'OBJECT' requires both object_type and object_id.")
            if self.domain_id is not None:
                raise ValueError("scope_type 'OBJECT' must not include domain_id.")
        return self


class VersionApprovalAuthorityRequest(BaseModel):
    """
    Request body for Version and Re-effective-Date Authorization Policy
    Object (BA-07, WP-02 / C-003, realizing ERB-C003-02 / EX-C003-07),
    applied to Approval Authority. Amendable fields are metadata only
    (authority_name, majority_threshold_pct) — approval_strategy and
    scope_type/domain_id/object_type/object_id (BR-C003-01's structural
    rule) are not amendable here, per EX-C003-07's own Trigger scope:
    "does not change its fundamental type or structural rule conformance."
    """
    authority_name: str | None = Field(None, min_length=1, max_length=255, description="Amended authority name. Omit to leave unchanged.")
    majority_threshold_pct: int | None = Field(None, ge=0, le=100, description="Amended threshold. Omit to leave unchanged.")
    effective_from: datetime | None = Field(None, description="Defaults to now if omitted.")
    effective_to: datetime | None = Field(None, description="NULL = open-ended.")
    approval_reference: str | None = Field(None, max_length=255, description="Optional free-text reference to the authority approving this version (SD-002-011).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "authority_name": "Annual Report Approver (Revised)",
            }
        }
    }


class ApprovalAuthorityResponse(BaseModel):
    """Establish Approval Authority's success response."""
    id: UUID
    organization_id: UUID
    authority_name: str
    approval_strategy: str
    majority_threshold_pct: int | None
    scope_type: str
    domain_id: UUID | None
    object_type: str | None
    object_id: UUID | None
    version: int
    status: str
    effective_from: datetime
    effective_to: datetime | None
    approval_reference: str | None
    supersedes_id: UUID | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
