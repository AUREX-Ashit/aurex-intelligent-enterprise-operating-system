from typing import Annotated, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import db_manager
from repositories.identity_repository import IdentityRepository
from repositories.membership_repository import MembershipRepository
from repositories.refresh_token_repository import RefreshTokenRepository
from schemas.auth import (
    LoginRequest,
    OrganizationSelectionResponse,
    RefreshTokenResponse,
    TokenResponse,
)
from services.auth_service import AuthService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_identity_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> IdentityRepository:
    return IdentityRepository(session)


async def get_membership_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> MembershipRepository:
    return MembershipRepository(session)


async def get_refresh_token_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)


async def get_auth_service(
    identity_repo: Annotated[IdentityRepository, Depends(get_identity_repository)],
    membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)],
    refresh_token_repo: Annotated[RefreshTokenRepository, Depends(get_refresh_token_repository)],
) -> AuthService:
    return AuthService(identity_repo, membership_repo, refresh_token_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User login",
    description=(
        "Authenticates a user by email and password. "
        "Supply X-Tenant-ID to log in directly to a specific organization. "
        "Omit X-Tenant-ID to receive an OrganizationSelectionResponse when the "
        "person belongs to more than one organization, or to auto-select when only one exists."
    ),
    responses={
        200: {
            "description": "Authenticated (full JWT) or organization selection required",
            "content": {
                "application/json": {
                    "oneOf": [
                        {"$ref": "#/components/schemas/TokenResponse"},
                        {"$ref": "#/components/schemas/OrganizationSelectionResponse"},
                    ]
                }
            },
        },
        401: {"description": "Invalid credentials"},
        403: {"description": "No active membership"},
    },
)
async def login(
    login_data: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    x_tenant_id: Annotated[str | None, Header()] = None,
) -> Union[TokenResponse, OrganizationSelectionResponse]:
    """
    Login handler for R-001 authentication flow.

    X-Tenant-ID (optional):
      - Provided  → direct org-scoped authentication → TokenResponse
      - Omitted, single membership  → auto-select org → TokenResponse
      - Omitted, multiple memberships → OrganizationSelectionResponse
        (client must re-POST with X-Tenant-ID set to the chosen organization_id)
    """
    organization_id: UUID | None = None

    if x_tenant_id is not None:
        try:
            organization_id = UUID(x_tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Header 'X-Tenant-ID' must be a valid RFC 4122 UUID.",
            )

    return await auth_service.authenticate_user(login_data, organization_id)


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description=(
        "Issues a new access token by validating the supplied refresh token against "
        "the database. Checks signature, expiry, revocation status, and current "
        "membership before re-issuing. Role changes are reflected immediately."
    ),
)
async def refresh_tokens(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    authorization: Annotated[str | None, Header(description="Bearer <refresh_token>")] = None,
) -> RefreshTokenResponse:
    """
    Refresh token handler. Expects Authorization: Bearer <refresh_token>.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header 'Authorization' must be populated with a Bearer token.",
        )

    refresh_token = authorization.split(" ", 1)[1]
    return await auth_service.refresh_session_token(refresh_token)
