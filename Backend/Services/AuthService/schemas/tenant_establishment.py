from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EstablishTenantRequest(BaseModel):
    """
    Request body for the C-040 Tenant Establishment transaction (TDS-016
    §8). Names only the target Organization — the two authority
    attributions (approved_by_actor_id / allocated_by_actor_id) are never
    caller-supplied; both are derived server-side from live
    `authority_holders` lookups (TDS-017 §22's own "live lookup, never a
    self-asserted claim" requirement), never trusted from the request.
    """
    organization_id: UUID = Field(..., description="The Organization to establish a Tenant for")

    model_config = {
        "json_schema_extra": {
            "example": {"organization_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}
        }
    }


class TenantResponse(BaseModel):
    """Response shape for the established Tenant (tenant_registry row)."""
    id: UUID
    organization_id: UUID
    tenant_code: str
    lifecycle_state: str
    version: int
    approved_by_actor_id: UUID
    approved_at: datetime
    allocated_by_actor_id: UUID
    allocated_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
