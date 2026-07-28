from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from models.membership import MembershipType, LicenseType


class EstablishMembershipRequest(BaseModel):
    """
    Request body for Establish Membership Context (WP-03 BA-01, C-007,
    realizing ERB-C007-01 / EX-C007-01 / EX-C007-02).

    role_id is required despite PE-001-C007's own "C-007 does not
    assign or remove Roles or Permissions" boundary (§1.4/1.8/5.9/5.10)
    — this is an inherited WP-00 schema coupling (memberships.role_id
    is NOT NULL), disclosed as TD-033, not a canonical requirement of
    this Business Activity itself.

    home_node_id is optional despite the canonical model's NOT NULL
    home_node_id — disclosed as TD-032 (no Business Activity anywhere
    yet establishes an OrganizationNode row to reference). When
    supplied, it is validated as a real, active node (BR-C007-002/007);
    it is never invented or defaulted.
    """
    person_id: UUID = Field(..., description="The resolved Person this Membership is for (C-006, Legacy Baseline).")
    organization_id: UUID = Field(..., description="The valid Organization this Membership is within (C-004, WP-01).")
    role_id: UUID = Field(..., description="The Role held under this Membership. Inherited WP-00 requirement — see TD-033.")
    home_node_id: UUID | None = Field(None, description="Confirmed home-node anchor (URA-001-17b/ERG-001-03). Optional — see TD-032.")
    membership_type: MembershipType = Field(MembershipType.INTERNAL, description="URA-001-106.")
    license_type: LicenseType = Field(LicenseType.FULL, description="URA-001-111.")
    effective_from: datetime | None = Field(None, description="Defaults to now if omitted.")
    effective_to: datetime | None = Field(None, description="NULL = open-ended.")
    is_primary: bool = Field(False, description="Whether this is the Person's primary Membership.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "person_id": "11111111-1111-1111-1111-111111111111",
                "organization_id": "22222222-2222-2222-2222-222222222222",
                "role_id": "33333333-3333-3333-3333-333333333333",
                "membership_type": "INTERNAL",
                "license_type": "FULL",
            }
        }
    }


class MembershipResponse(BaseModel):
    """Establish Membership Context's success response."""
    id: UUID
    person_id: UUID
    organization_id: UUID
    role_id: UUID
    home_node_id: UUID | None
    membership_type: str
    license_type: str
    membership_status: str
    is_primary: bool
    effective_from: datetime
    effective_to: datetime | None
    joined_at: datetime
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
