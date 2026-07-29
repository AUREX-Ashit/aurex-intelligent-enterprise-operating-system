from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EstablishOrganizationNodeRequest(BaseModel):
    """
    Request body for Establish Organization Node (WP-04 BA-01, C-005,
    ERB-C005-01/EX-C005-01/02). Fields mirror OrganizationNode's current
    (IRA-004 §9-scoped Structural Identity subset) columns exactly — no
    field is invented beyond what the model persists.
    """
    node_code: str = Field(..., min_length=1, max_length=100, description="Unique node code")
    node_name: str = Field(..., min_length=1, max_length=255, description="Node display name")
    node_type: str = Field(..., min_length=1, max_length=255, description="Node type (e.g. HOLDING, REGION, ENTITY, SITE, SUPPLIER, JV) — free text, not a closed enum")
    legal_entity_name: str | None = Field(None, max_length=255, description="Official legal entity name")
    business_unit: str | None = Field(None, max_length=255, description="Business unit mapping")
    sector: str | None = Field(None, max_length=255, description="Industry sector")
    operational_status: str | None = Field(None, max_length=50, description="Operational status (e.g. ACTIVE, INACTIVE, DIVESTED) — free text, not a closed enum")
    effective_from: datetime | None = Field(None, description="Structural validity start")
    effective_to: datetime | None = Field(None, description="Structural validity end")

    model_config = {
        "json_schema_extra": {
            "example": {
                "node_code": "APAC-HOLD-001",
                "node_name": "APAC Holding",
                "node_type": "HOLDING",
                "legal_entity_name": "Acme APAC Holdings Pte Ltd",
                "business_unit": "APAC Operations",
                "sector": "Manufacturing",
                "operational_status": "ACTIVE",
            }
        }
    }


class OrganizationNodeResponse(BaseModel):
    """
    Establish Organization Node's success response, and the shape
    future OrganizationNode read endpoints (WP-04 BA-02) will reuse.
    """
    id: UUID
    node_code: str
    node_name: str
    node_type: str
    legal_entity_name: str | None
    business_unit: str | None
    sector: str | None
    operational_status: str | None
    active_flag: bool
    effective_from: datetime | None
    effective_to: datetime | None

    model_config = {"from_attributes": True}
