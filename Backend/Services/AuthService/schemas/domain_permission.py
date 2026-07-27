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


class DomainPermissionResponse(BaseModel):
    """Establish Domain Permission's success response."""
    id: UUID
    membership_id: UUID
    domain_id: UUID
    permission_level: str
    effective_from: datetime
    effective_to: datetime | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
