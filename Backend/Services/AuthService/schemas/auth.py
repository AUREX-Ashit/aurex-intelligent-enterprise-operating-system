from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """
    Validation schema for Auth Sign In endpoint.
    Strict validation of email format and password structure.
    """
    email: EmailStr = Field(..., description="User's unique registered corporate email address")
    password: str = Field(..., min_length=8, description="User's secure account password")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@corpstage.com",
                "password": "securePassWord123"
            }
        }
    }


class TokenPayload(BaseModel):
    """
    Internal R-001 JWT claims structure.
    Used by AuthService to build and decode token payloads.
    Never serialized directly in API responses.

    organization_id/membership_id/role_code are Optional (TDS-017 §22,
    C-040 Authority Runtime Enforcement): the ordinary Organization-scoped
    login path (authenticate_user) always populates all three, unchanged.
    The narrowly-scoped authority-holder login path
    (authenticate_authority_holder) leaves all three None — a platform-
    wide, pre-Organization accountability point (AI-001/AI-002) has no
    Membership and therefore no Organization or Role to carry. person_id
    and identity_id remain mandatory for both paths — Person/Identity are
    already Organization-independent (URA-001-15).
    """
    person_id: UUID
    identity_id: UUID
    organization_id: UUID | None = None
    membership_id: UUID | None = None
    role_code: str | None = None


class TokenResponse(BaseModel):
    """
    Standard response schema on successful authentication.
    """
    access_token: str = Field(..., description="Cryptographically signed JSON Web Token")
    token_type: str = Field("bearer", description="Token authentication scheme")
    expires_in: int = Field(3600, description="Remaining validity window in seconds")
    refresh_token: str = Field(..., description="Encrypted persistent token for access renewal")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_access",
                "token_type": "bearer",
                "expires_in": 3600,
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_refresh"
            }
        }
    }


class RefreshTokenResponse(BaseModel):
    """
    Token renewal response schema.
    """
    access_token: str = Field(..., description="New cryptographically signed JSON Web Token")
    token_type: str = Field("bearer", description="Token authentication scheme")
    expires_in: int = Field(3600, description="Validity window of the new token in seconds")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.new_dummy_access",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }
    }


class AuthorityLoginRequest(BaseModel):
    """
    Validation schema for the narrowly-scoped authority-holder login path
    (TDS-017 §22). Deliberately identical shape to LoginRequest — the
    credential-verification step is fully reused (Phase 3's own "reuse
    the existing credential/password verification mechanism"
    requirement) — kept as a distinct type so the two endpoints' own
    request contracts can evolve independently without coupling.
    """
    email: EmailStr = Field(..., description="User's unique registered corporate email address")
    password: str = Field(..., min_length=8, description="User's secure account password")


class AuthorityTokenResponse(BaseModel):
    """
    Response for a successful authority-holder login. Deliberately carries
    NO refresh_token — TDS-017 never specifies refresh/renewal semantics
    for this token class, and reusing the ordinary refresh_session_token()
    flow would silently require organization_id (it hard-requires and
    re-validates Membership), which this path's own token never carries.
    Not inventing that behavior here: an authority holder simply
    re-authenticates (password + live holder-check) once this short-lived
    access token expires.
    """
    access_token: str = Field(..., description="Cryptographically signed JSON Web Token")
    token_type: str = Field("bearer", description="Token authentication scheme")
    expires_in: int = Field(3600, description="Remaining validity window in seconds")


class AuthorityCheckResponse(BaseModel):
    """
    Diagnostic response confirming the caller's own live-verified
    authority-holder status (TDS-017 §22/§24 — a live lookup, never a
    token-embedded claim). Not a C-040 business endpoint response — this
    exists to exercise the Phase 4 runtime-authorization dependency in
    isolation, ahead of any future Tenant Establishment endpoint that
    would actually consume it.
    """
    authority_identity: str = Field(..., description="'AI-001' or 'AI-002'")
    person_id: UUID = Field(..., description="The authenticated caller's own person_id")
    authorized: bool = Field(True, description="Always True for a 200 response — a denial raises 403 instead")


class OrganizationOption(BaseModel):
    """
    A single organization available for selection during multi-org login.
    Returned as part of OrganizationSelectionResponse when a person
    belongs to more than one active organization.
    """
    organization_id: UUID = Field(..., description="Organization unique identifier")
    organization_name: str = Field(..., description="Display name of the organization")
    role_code: str = Field(..., description="Role the person holds in this organization")

    model_config = {
        "json_schema_extra": {
            "example": {
                "organization_id": "550e8400-e29b-41d4-a716-446655440000",
                "organization_name": "ABC Manufacturing",
                "role_code": "ESG_MANAGER"
            }
        }
    }


class OrganizationSelectionResponse(BaseModel):
    """
    Returned when a person belongs to multiple organizations and no
    X-Tenant-ID was supplied. The client must present this list to the user,
    then re-POST /auth/login with X-Tenant-ID set to the chosen organization_id.
    """
    requires_organization_selection: bool = Field(
        True,
        description="Always True for this response type — used by clients as a discriminator"
    )
    organizations: list[OrganizationOption] = Field(
        ...,
        description="Organizations available for selection"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "requires_organization_selection": True,
                "organizations": [
                    {
                        "organization_id": "550e8400-e29b-41d4-a716-446655440000",
                        "organization_name": "ABC Manufacturing",
                        "role_code": "ESG_MANAGER"
                    },
                    {
                        "organization_id": "660e8400-e29b-41d4-a716-446655440001",
                        "organization_name": "XYZ Chemicals",
                        "role_code": "AUDITOR"
                    }
                ]
            }
        }
    }
