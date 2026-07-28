from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from models.domain_permission import DomainPermissionLevel


class EstablishDomainPermissionRequest(BaseModel):
    """
    Request body for Establish Domain Permission (BA-02, WP-02 / C-003,
    realizing ERB-C003-01 / EX-C003-02). Fields mirror
    domain_permission_registry's columns exactly (Master Technical
    Architecture, URA-001-47).
    """
    membership_id: UUID = Field(..., description="The Membership this Domain Permission is granted to.")
    domain_id: UUID = Field(..., description="The target Domain, already established (C-004/URA-001 Section 4).")
    permission_level: DomainPermissionLevel = Field(..., description="One of URA-001-47's eight standing-authority levels.")
    effective_from: datetime | None = Field(None, description="Defaults to now if omitted (URA-001-53).")
    effective_to: datetime | None = Field(None, description="NULL = open-ended (URA-001-53: permissions may be time-bound, not always).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "membership_id": "44444444-4444-4444-4444-444444444444",
                "domain_id": "55555555-5555-5555-5555-555555555555",
                "permission_level": "APPROVE",
            }
        }
    }


class VersionDomainPermissionRequest(BaseModel):
    """
    Request body for Version and Re-effective-Date Authorization Policy
    Object (BA-07, WP-02 / C-003, realizing ERB-C003-02 / EX-C003-07),
    applied to Domain Permission. Domain Permission has no metadata field
    distinct from its structural grant itself (membership_id, domain_id,
    permission_level are each BR-C003-01's structural rule and are not
    amendable here) — this Business Activity is therefore pure
    re-effective-dating for this object type: only the effective-date
    window may be amended, per EX-C003-07's own Trigger scope ("an
    amended effective-date window... that does not change its
    fundamental type or structural rule conformance").
    """
    effective_from: datetime | None = Field(None, description="Defaults to now if omitted.")
    effective_to: datetime | None = Field(None, description="NULL = open-ended.")
    approval_reference: str | None = Field(None, max_length=255, description="Optional free-text reference to the authority approving this version (SD-002-011).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "effective_to": "2027-01-01T00:00:00Z",
            }
        }
    }


class DomainPermissionResponse(BaseModel):
    """Establish Domain Permission's success response."""
    id: UUID
    membership_id: UUID
    domain_id: UUID
    permission_level: str
    effective_from: datetime
    effective_to: datetime | None
    version: int
    status: str
    approval_reference: str | None
    supersedes_id: UUID | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
