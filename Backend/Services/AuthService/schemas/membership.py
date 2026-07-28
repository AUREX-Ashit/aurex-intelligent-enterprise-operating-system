from datetime import datetime
from enum import Enum
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


class MembershipAuthorityConsequence(str, Enum):
    """
    WP-03 BA-02 (Understand Membership Context, ERB-C007-02/EX-C007-03).

    PE-001-C007's own Contract 5.1/5.3 and §6.3 ("Active standing with
    lapsed effective validity") state this rule four separate times: a
    Membership's recorded standing being ACTIVE SHALL NOT be presented
    or consumed as implying current authority — authority SHALL always
    be derived from Standing Context and Effective Validity Context
    together (BR-C007-013), recomputed live, never stored or cached.
    This enum is that computed result's own value set; it has no
    corresponding database column.
    """
    ACTIVE_AND_EFFECTIVE = "ACTIVE_AND_EFFECTIVE"
    ACTIVE_NOT_YET_EFFECTIVE = "ACTIVE_NOT_YET_EFFECTIVE"
    ACTIVE_BUT_LAPSED = "ACTIVE_BUT_LAPSED"
    NOT_ACTIVE = "NOT_ACTIVE"


class MembershipUnderstandingResponse(MembershipResponse):
    """
    Understand Membership Context's response (WP-03 BA-02). Extends
    MembershipResponse with the Membership Understanding Context's own
    computed fields — the Membership's stored terms/standing/home-node
    fields are unchanged and presented as-is; only these two fields are
    freshly derived on every call, never persisted.
    """
    currently_effective: bool = Field(
        ...,
        description=(
            "True only when membership_status is ACTIVE and now falls within "
            "[effective_from, effective_to). BR-C007-013: an ACTIVE Membership "
            "past its effective_to is never presented as currently effective."
        ),
    )
    authority_consequence: MembershipAuthorityConsequence = Field(
        ..., description="The reasoned classification behind currently_effective."
    )
