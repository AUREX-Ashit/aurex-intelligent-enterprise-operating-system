from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EstablishRoleRequest(BaseModel):
    """
    Request body for Establish Business or System Role (BA-01, WP-02 /
    C-003, realizing ERB-C003-01 / EX-C003-01). Fields mirror the Role
    model's existing columns exactly — no field is invented beyond what
    the model persists. `is_system_role` is the schema's existing
    discriminator between a System Role and a Business Role (URA-001-03:
    "System Roles and Business Roles remain independent") — BA-01 does
    not introduce a new column for this.
    """
    role_code: str = Field(..., min_length=1, max_length=100, description="Unique role code")
    role_name: str = Field(..., min_length=1, max_length=255, description="Role display name")
    description: str | None = Field(None, max_length=1000, description="Optional role description")
    is_system_role: bool = Field(False, description="True for a System Role, False for a Business Role (URA-001 Section 3)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "role_code": "PLANT_HEAD",
                "role_name": "Plant Head",
                "description": "Business Role for plant-level operational accountability.",
                "is_system_role": False,
            }
        }
    }


class VersionRoleRequest(BaseModel):
    """
    Request body for Version and Re-effective-Date Authorization Policy
    Object (BA-07, WP-02 / C-003, realizing ERB-C003-02 / EX-C003-07),
    applied to Role. Amendable fields are metadata only (role_name,
    description) — role_code (identity) and is_system_role (fundamental
    type, BR-C003-01's structural rule) are not amendable here, per
    EX-C003-07's own Trigger scope: "does not change its fundamental
    type or structural rule conformance."
    """
    role_name: str | None = Field(None, min_length=1, max_length=255, description="Amended role display name. Omit to leave unchanged.")
    description: str | None = Field(None, max_length=1000, description="Amended description. Omit to leave unchanged.")
    effective_from: datetime | None = Field(None, description="Defaults to now if omitted.")
    effective_to: datetime | None = Field(None, description="NULL = open-ended.")
    approval_reference: str | None = Field(None, max_length=255, description="Optional free-text reference to the authority approving this version (SD-002-011).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "role_name": "Plant Head (Revised)",
            }
        }
    }


class RoleResponse(BaseModel):
    """Establish Role's success response."""
    id: UUID
    role_code: str
    role_name: str
    description: str | None
    is_system_role: bool
    version: int
    status: str
    effective_from: datetime
    effective_to: datetime | None
    approval_reference: str | None
    supersedes_id: UUID | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
