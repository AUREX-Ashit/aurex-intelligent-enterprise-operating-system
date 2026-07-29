from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.organization_repository import OrganizationRepository
from repositories.organization_establishment_attempt_repository import (
    OrganizationEstablishmentAttemptRepository,
)
from schemas.organization import OrganizationResponse
from schemas.organization_establishment_attempt import (
    ActivateEstablishmentRequest,
    EstablishOrganizationAttemptRequest,
    OrganizationEstablishmentAttemptResponse,
    VerifyDomainClaimRequest,
)
from services.organization_service import OrganizationService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_organization_establishment_attempt_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationEstablishmentAttemptRepository:
    return OrganizationEstablishmentAttemptRepository(session)


async def get_organization_service(
    organization_repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    organization_establishment_attempt_repo: Annotated[
        OrganizationEstablishmentAttemptRepository,
        Depends(get_organization_establishment_attempt_repository),
    ],
) -> OrganizationService:
    return OrganizationService(organization_repo, organization_establishment_attempt_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=OrganizationEstablishmentAttemptResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new Organization Establishment Attempt (Organization Anchor Context)",
    description=(
        "IRA-001A / WP-01 Business Activity: Establish Organization Identity "
        "(BA-01, amended — C-004, ERB-C004-01). Requires the PLATFORM_ADMIN "
        "role, the same interim gate every WP-01 endpoint uses (IRA-001 "
        "§2.7). Produces a non-authoritative Organization Anchor Context, "
        "never an Organization — see POST /organization-establishment-"
        "attempts/{id}/activate for the distinct, governed activation act "
        "that produces the first real Organization. Rejects duplicate "
        "organization_code with 409, checked against both already-activated "
        "Organizations and other in-flight establishment attempts."
    ),
    responses={
        201: {"description": "Organization establishment attempt created."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        409: {"description": "An organization or establishment attempt with this organization_code already exists."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def establish_organization(
    request: EstablishOrganizationAttemptRequest,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OrganizationEstablishmentAttemptResponse:
    """
    No tenant-scoping: establishing a brand-new Organization Establishment
    Attempt has no existing tenant to scope to, the same basis the original
    (pre-IRA-001A) POST /organizations documented — see
    middleware/tenant.py's exemption list, which this path is added to.
    """
    attempt = await organization_service.establish(request, actor_id=claims.get("person_id"))
    return OrganizationEstablishmentAttemptResponse.model_validate(attempt)


@router.post(
    "/{attempt_id}/verify-domain",
    response_model=OrganizationEstablishmentAttemptResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify an Organization Establishment Attempt's domain claim",
    description=(
        "IRA-001A Business Activity: Verify Organization Domain Claim "
        "(BA-01B, new — C-004, ERB-C004-02). Requires the PLATFORM_ADMIN "
        "role. Only applicable to an attempt that claimed a primary_domain "
        "at establishment; records the verification outcome as a distinct, "
        "audited, traceable fact (BR-C004-02/BR-C004-09) — the actual "
        "proof-of-control mechanism is out of scope (disclosed as "
        "Technical Debt, IMP-REPORT-WP-01's IRA-001A section)."
    ),
    responses={
        200: {"description": "Domain claim verification outcome recorded."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No establishment attempt exists with this id."},
        409: {"description": "Attempt already activated, or claimed no primary_domain."},
        422: {"description": "attempt_id is not a valid UUID."},
    },
)
async def verify_organization_domain_claim(
    attempt_id: UUID,
    request: VerifyDomainClaimRequest,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OrganizationEstablishmentAttemptResponse:
    """No tenant-scoping, same basis as establish_organization above."""
    attempt = await organization_service.verify_domain_claim(
        attempt_id, request.verified, actor_id=claims.get("person_id")
    )
    return OrganizationEstablishmentAttemptResponse.model_validate(attempt)


@router.post(
    "/{attempt_id}/activate",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Activate an Organization Establishment Attempt (first-time activation)",
    description=(
        "IRA-001A Business Activity: Activate Organization, first-time "
        "(BA-01C, new — C-004, ERB-C004-03). Requires the PLATFORM_ADMIN "
        "role. Realizes BR-C004-01/Contract 5.4: the first, distinct, "
        "governed act producing the first Authoritative Organization "
        "Context for this establishment attempt. Requires either a "
        "VERIFIED domain claim or an explicit no_domain_activation_reason "
        "(the governed no-domain decision, BR-C004-09). Lexically and "
        "semantically distinct from POST /organizations/{organization_id}"
        "/activate (BA-05, reactivation of an already-Authoritative, "
        "SUSPENDED Organization) — that endpoint is unmodified and unaware "
        "of establishment attempts."
    ),
    responses={
        201: {"description": "Organization activated for the first time."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No establishment attempt exists with this id."},
        409: {
            "description": (
                "Attempt already activated; activation preconditions not met "
                "(no VERIFIED domain and no no_domain_activation_reason); or "
                "a concurrent activation already claimed this organization_code."
            )
        },
        422: {"description": "attempt_id is not a valid UUID."},
    },
)
async def activate_organization_establishment(
    attempt_id: UUID,
    request: ActivateEstablishmentRequest,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OrganizationResponse:
    """No tenant-scoping, same basis as establish_organization above."""
    organization = await organization_service.activate_establishment(
        attempt_id, request, actor_id=claims.get("person_id")
    )
    return OrganizationResponse.model_validate(organization)
