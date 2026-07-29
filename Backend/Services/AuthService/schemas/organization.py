from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class UpdateOrganizationProfileRequest(BaseModel):
    """
    Request body for Update Organization Profile (BA-04, WP-01 / C-004).
    Covers the same descriptive Profile fields as
    EstablishOrganizationAttemptRequest (schemas/organization_establishment_attempt.py,
    IRA-001A) except organization_code, which is
    intentionally excluded: it is the immutable natural key duplicate
    detection and search are built against (see
    OrganizationRepository.get_by_code()); renaming it is not part of
    this Business Activity's scope (IRA-001 §2.2's "Update Organization
    Profile" row) and would require its own uniqueness re-validation,
    which no canonical document currently asks WP-01 to build.
    """
    organization_name: str = Field(..., min_length=1, max_length=255, description="Organization display name")
    organization_type: str = Field(..., min_length=1, max_length=50, description="Organization type (e.g. CORPORATE, SUPPLIER)")
    description: str | None = Field(None, max_length=1000, description="Optional profile description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "organization_name": "Acme Corporation",
                "organization_type": "CORPORATE",
                "description": "Global manufacturing conglomerate.",
            }
        }
    }


class OrganizationResponse(BaseModel):
    """
    The Authoritative Organization response shape, reused by BA-01C
    (Activate Organization, first-time — IRA-001A) and every read/
    lifecycle endpoint (BA-02, BA-03, BA-04, BA-05, BA-06, BA-07).
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
