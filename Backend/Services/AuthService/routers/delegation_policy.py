from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.delegation_policy_repository import DelegationPolicyRepository
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from schemas.delegation_policy import EstablishDelegationPolicyRequest, DelegationPolicyResponse
from services.delegation_policy_service import DelegationPolicyService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_delegation_policy_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DelegationPolicyRepository:
    return DelegationPolicyRepository(session)


async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_domain_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DomainRepository:
    return DomainRepository(session)


async def get_delegation_policy_service(
    delegation_policy_repo: Annotated[DelegationPolicyRepository, Depends(get_delegation_policy_repository)],
    organization_repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    domain_repo: Annotated[DomainRepository, Depends(get_domain_repository)],
) -> DelegationPolicyService:
    return DelegationPolicyService(delegation_policy_repo, organization_repo, domain_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=DelegationPolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new Delegation Policy",
    description=(
        "WP-02 Business Activity: Establish Delegation Policy (C-003), "
        "realizing PE-001-C003's ERB-C003-01 / EX-C003-04. Requires the "
        "PLATFORM_ADMIN role (interim gate, mirroring BA-01/BA-02/BA-03 — "
        "confirmed Corporate Admin/Domain Owner authority is not yet "
        "implementable, tracked as technical debt). Declares exactly one "
        "delegation_type and exactly one scope_type (ORGANIZATION/DOMAIN/"
        "OBJECT/EVENT, URA-001-89); an ambiguous, dual-stated, or "
        "incomplete scope is rejected with 422. Governs future delegation "
        "instances (out of this capability's own scope) — never "
        "establishes a specific delegator/delegatee pairing itself. "
        "Rejects an unknown Organization or Domain with 404."
    ),
    responses={
        201: {"description": "Delegation Policy established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Organization or Domain does not exist."},
        422: {"description": "Invalid request (e.g., scope_type's required anchor missing, or an anchor supplied for the wrong scope_type)."},
    },
)
async def establish_delegation_policy(
    request: EstablishDelegationPolicyRequest,
    delegation_policy_service: Annotated[DelegationPolicyService, Depends(get_delegation_policy_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DelegationPolicyResponse:
    delegation_policy = await delegation_policy_service.establish(request, actor_id=claims.get("person_id"))
    return DelegationPolicyResponse.model_validate(delegation_policy)
