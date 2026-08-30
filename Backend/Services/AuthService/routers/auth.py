from typing import Annotated, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_ai001_holder, require_ai002_holder, get_current_claims
from models.database import db_manager
from repositories.identity_repository import IdentityRepository
from repositories.membership_repository import MembershipRepository
from repositories.refresh_token_repository import RefreshTokenRepository
from repositories.authority_holder_repository import AuthorityHolderRepository
from schemas.auth import (
    AuthorityCheckResponse,
    AuthorityLoginRequest,
    AuthorityTokenResponse,
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


async def get_authority_holder_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> AuthorityHolderRepository:
    return AuthorityHolderRepository(session)


async def get_auth_service(
    identity_repo: Annotated[IdentityRepository, Depends(get_identity_repository)],
    membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)],
    refresh_token_repo: Annotated[RefreshTokenRepository, Depends(get_refresh_token_repository)],
    authority_holder_repo: Annotated[AuthorityHolderRepository, Depends(get_authority_holder_repository)],
) -> AuthService:
    return AuthService(identity_repo, membership_repo, refresh_token_repo, authority_holder_repo)


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


# ---------------------------------------------------------------------------
# C-040 Authority Runtime Enforcement (TDS-017) — narrowly-scoped
# pre-Organization authentication and authorization endpoints. Not a
# C-040 business endpoint (Tenant Establishment itself remains
# unimplemented, out of scope per TDS-016/017) — these exist to make the
# Phase 3/4 authentication and runtime-authorization mechanisms usable
# and testable ahead of any future Tenant Establishment endpoint that
# would actually consume require_ai001_holder/require_ai002_holder.
# ---------------------------------------------------------------------------

@router.post(
    "/authority-login/{authority_identity}",
    response_model=AuthorityTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authority-holder login (AI-001/AI-002)",
    description=(
        "Narrowly-scoped, Organization-independent login for the "
        "currently appointed AI-001 or AI-002 accountability point "
        "(TDS-017 §22). Reuses ordinary credential verification. "
        "Issues a token ONLY if the authenticated person is the live, "
        "currently ACTIVE holder of the named authority — never a "
        "generic zero-Membership bypass."
    ),
    responses={
        400: {"description": "authority_identity must be 'AI-001' or 'AI-002'"},
        401: {"description": "Invalid credentials"},
        403: {"description": "Authenticated, but not the currently appointed accountability point"},
    },
)
async def authority_login(
    authority_identity: str,
    login_data: AuthorityLoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthorityTokenResponse:
    return await auth_service.authenticate_authority_holder(login_data, authority_identity)


@router.get(
    "/authority-check/ai-001",
    response_model=AuthorityCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Diagnostic: verify caller is the live AI-001 accountability point",
    description=(
        "Exercises the require_ai001_holder runtime-authorization "
        "dependency (TDS-017 §24) in isolation. Not a C-040 business "
        "endpoint."
    ),
    responses={403: {"description": "Not the currently appointed AI-001 accountability point"}},
)
async def authority_check_ai001(
    claims: Annotated[dict, Depends(require_ai001_holder)],
) -> AuthorityCheckResponse:
    return AuthorityCheckResponse(authority_identity="AI-001", person_id=UUID(claims["person_id"]))


@router.get(
    "/authority-check/ai-002",
    response_model=AuthorityCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Diagnostic: verify caller is the live AI-002 accountability point",
    description=(
        "Exercises the require_ai002_holder runtime-authorization "
        "dependency (TDS-017 §24) in isolation. Not a C-040 business "
        "endpoint. Always denies today — AI-002 remains unpopulated "
        "(TD-157, Open — BLOCKED); no AI-002 holder record exists."
    ),
    responses={403: {"description": "Not the currently appointed AI-002 accountability point"}},
)
async def authority_check_ai002(
    claims: Annotated[dict, Depends(require_ai002_holder)],
) -> AuthorityCheckResponse:
    return AuthorityCheckResponse(authority_identity="AI-002", person_id=UUID(claims["person_id"]))
