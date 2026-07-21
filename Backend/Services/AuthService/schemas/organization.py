from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class EstablishOrganizationRequest(BaseModel):
    """
    Request body for Establish Organization (Business Activity 1 of
    WP-01 / C-004). Fields mirror the Organization model's current
    (ADR-004-scoped) columns exactly — no field is invented beyond what
    the model persists.
    """
    organization_code: str = Field(..., min_length=1, max_length=50, description="Unique organization code")
    organization_name: str = Field(..., min_length=1, max_length=255, description="Organization display name")
    organization_type: str = Field(..., min_length=1, max_length=50, description="Organization type (e.g. CORPORATE, SUPPLIER)")
    description: str | None = Field(None, max_length=1000, description="Optional profile description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "organization_code": "ACME-CORP-001",
                "organization_name": "Acme Corporation",
                "organization_type": "CORPORATE",
                "description": "Global manufacturing conglomerate.",
            }
        }
    }


class OrganizationResponse(BaseModel):
    """
    Establish Organization's success response, and the shape future
    Organization read endpoints (Phase 1 of IRA-001's implementation
    plan) will reuse.
    """
    id: UUID
    organization_code: str
    organization_name: str
    organization_type: str
    description: str | None
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class OrganizationSortField(str, Enum):
    """Whitelisted sortable fields for BA-03 Search & List — mirrors repositories/organization_repository.py's _SORTABLE_COLUMNS."""
    organization_name = "organization_name"
    organization_code = "organization_code"
    created_at = "created_at"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class OrganizationListResponse(BaseModel):
    """Response for BA-03 Search & List Organizations — a page of results plus enough metadata to render pagination."""
    items: list[OrganizationResponse]
    total: int = Field(..., description="Total organizations matching the query, independent of pagination")
    skip: int
    limit: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [],
                "total": 0,
                "skip": 0,
                "limit": 20,
            }
        }
    }
