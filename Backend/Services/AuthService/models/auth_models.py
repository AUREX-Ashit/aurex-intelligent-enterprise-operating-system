from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional, List

class LoginRequest(BaseModel):
    """
    Standard login request payload with email validation and constraints.
    """
    email: EmailStr = Field(..., description="The registered enterprise email address")
    password: str = Field(..., min_length=8, description="The user's secret password")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "ashit.aurex@gmail.com",
                "password": "Password123!"
            }
        }
    }


class TokenPayload(BaseModel):
    """
    Structured decrypted schema contained in JWT custom payloads.
    Tenant-isolation is verified by extracting the tenant_id on request boundaries.
    """
    sub: str = Field(..., description="Subject claim, typically the User UUID")
    email: EmailStr = Field(..., description="Authorized email address")
    tenant_id: UUID = Field(..., description="The unique enterprise tenant scope ID")
    role: str = Field(..., description="Corporate identity access role (e.g. admin, auditor, analyst)")
    exp: int = Field(..., description="Token expiration timestamp (UTC epoch)")
    jti: str = Field(..., description="Unique token identifier for revocation sweeps")


class LoginResponse(BaseModel):
    """
    Token issuing payload upon authenticated logins.
    """
    access_token: str = Field(..., description="Strict tenant-aware access JWT token")
    refresh_token: str = Field(..., description="Refresh JWT token to update active access sessions")
    token_type: str = Field(default="Bearer", description="Oauth2 compliant token scheme")
    tenant_id: UUID = Field(..., description="Authorized enterprise tenant domain index")
    role: str = Field(..., description="Granted access permission scope")
    expires_in: int = Field(default=900, description="Access token expiration validity period in seconds (default: 15 mins)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5ZDFi...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5ZDFi...",
                "token_type": "Bearer",
                "tenant_id": "3123da12-c214-4903-8ad1-6fcc7f80db18",
                "role": "auditor",
                "expires_in": 900
            }
        }
    }


class RefreshRequest(BaseModel):
    """
    JSON body container holding the refresh token.
    Can be used if cookie extraction or Bearer header are not preferred by clients.
    """
    refresh_token: str = Field(..., description="The persistent refresh token issued at login")


class RefreshResponse(BaseModel):
    """
    Returned response containing the refreshed access token.
    """
    access_token: str = Field(..., description="Newly issued tenant-aware access JWT token")
    token_type: str = Field(default="Bearer", description="Token scheme")
    expires_in: int = Field(default=900, description="New validity period in seconds")


class HealthCheckResponse(BaseModel):
    """
    Health check metadata telemetry.
    """
    status: str = Field(..., description="Overall health state (e.g. green, orange, red)")
    service: str = Field(dfault="aurex-auth-service", description="Service identity identifier")
    database_connected: bool = Field(..., description="Active connection check to PostgreSQL")
    uptime_seconds: float = Field(..., description="Seconds since server boots successfully")
