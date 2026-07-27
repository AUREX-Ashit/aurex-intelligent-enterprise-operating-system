from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DomainResponse(BaseModel):
    """Domain reference-catalog row (AMD-014). Read-only — no request schema exists; Domain rows are seeded, not created through this API."""
    id: UUID
    organization_id: UUID | None
    domain_name: str
    parent_domain_id: UUID | None
    active_flag: bool
    created_at: datetime

    model_config = {"from_attributes": True}
