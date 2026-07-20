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
    """
    person_id: UUID
    identity_id: UUID
    organization_id: UUID
    membership_id: UUID
    role_code: str


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
