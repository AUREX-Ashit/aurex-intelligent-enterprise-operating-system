from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EstablishOrganizationAttemptRequest(BaseModel):
    """
    Request body for BA-01 (amended, IRA-001A) — Establish Organization
    Identity. Candidate identity fields mirror the original
    EstablishOrganizationRequest exactly (no field invented); adds the
    optional primary_domain claim ERB-C004-02 requires a place to land.
    """
    organization_code: str = Field(..., min_length=1, max_length=50, description="Unique organization code")
    organization_name: str = Field(..., min_length=1, max_length=255, description="Organization display name")
    organization_type: str = Field(..., min_length=1, max_length=50, description="Organization type (e.g. CORPORATE, SUPPLIER)")
    description: str | None = Field(None, max_length=1000, description="Optional profile description")
    primary_domain: str | None = Field(None, max_length=255, description="Optional claimed primary domain (ERB-C004-02)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "organization_code": "ACME-CORP-001",
                "organization_name": "Acme Corporation",
                "organization_type": "CORPORATE",
                "description": "Global manufacturing conglomerate.",
                "primary_domain": "acme.example",
            }
        }
    }


class VerifyDomainClaimRequest(BaseModel):
    """Request body for BA-01B — Verify Organization Domain Claim (ERB-C004-02)."""
    verified: bool = Field(..., description="Outcome of independent proof-of-control verification")


class ActivateEstablishmentRequest(BaseModel):
    """
    Request body for BA-01C — Activate Organization, first-time
    (ERB-C004-03). no_domain_activation_reason is required only when the
    attempt's domain_verification_status is not VERIFIED — it records the
    governed no-domain activation decision itself (BR-C004-09), never a
    silent default.
    """
    no_domain_activation_reason: str | None = Field(
        None, max_length=1000, description="Required if the attempt has no VERIFIED domain claim"
    )


class OrganizationEstablishmentAttemptResponse(BaseModel):
    """Response shape for BA-01 (establish) and BA-01B (verify) — the Anchor's own state, never an OrganizationResponse."""
    id: UUID
    organization_code: str
    organization_name: str
    organization_type: str
    description: str | None
    primary_domain: str | None
    domain_verification_status: str
    activated_organization_id: UUID | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
