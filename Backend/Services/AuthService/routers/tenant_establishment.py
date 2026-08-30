from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_ai002_holder
from models.database import db_manager
from repositories.authority_holder_repository import AuthorityHolderRepository
from repositories.organization_repository import OrganizationRepository
from repositories.tenant_registry_repository import TenantRegistryRepository
from schemas.tenant_establishment import EstablishTenantRequest, TenantResponse
from services.tenant_establishment_service import TenantEstablishmentService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_tenant_registry_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> TenantRegistryRepository:
    return TenantRegistryRepository(session)


async def get_authority_holder_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> AuthorityHolderRepository:
    return AuthorityHolderRepository(session)


async def get_tenant_establishment_service(
    organization_repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    tenant_registry_repo: Annotated[TenantRegistryRepository, Depends(get_tenant_registry_repository)],
    authority_holder_repo: Annotated[AuthorityHolderRepository, Depends(get_authority_holder_repository)],
) -> TenantEstablishmentService:
    return TenantEstablishmentService(organization_repo, tenant_registry_repo, authority_holder_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=TenantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a Tenant for an Organization (C-040, TDS-016 §8)",
    description=(
        "Chartered minimum C-040 Business Activity (Repository Owner "
        "Decision, 2026-08-26: 'Tenant Establishment only — Business "
        "Approval -> Infrastructure Allocation'). Atomically creates the "
        "tenant_registry row and populates organizations.tenant_id, "
        "exactly once, per TDS-016 §8. Requires the caller to be the "
        "currently-appointed AI-002 (Infrastructure Allocation Authority) "
        "accountability point — a live authority_holders lookup, never "
        "PLATFORM_ADMIN, never AUREX_ADMIN, never a role or claim "
        "substitute (TDS-017 §22). Also requires a currently-appointed "
        "AI-001 (Business Approval Authority) accountability point to "
        "exist, attributed as approver in the same atomic transaction. "
        "Migration, offboarding, cross-tenant sharing, and Technical "
        "Provisioning are explicitly out of scope (TDS-016 §1) — this "
        "endpoint only ever produces the initial PROVISIONED state."
    ),
    responses={
        201: {"description": "Tenant established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller is not the currently-appointed AI-002 accountability point."},
        404: {"description": "No Organization exists with the given organization_id."},
        409: {
            "description": (
                "This Organization already has an established Tenant; or no "
                "currently-appointed AI-001 accountability point exists to "
                "attribute Business Approval to."
            )
        },
        422: {"description": "Invalid request (e.g., organization_id is not a valid UUID)."},
    },
)
async def establish_tenant(
    request: EstablishTenantRequest,
    tenant_establishment_service: Annotated[TenantEstablishmentService, Depends(get_tenant_establishment_service)],
    claims: Annotated[dict, Depends(require_ai002_holder)],
) -> TenantResponse:
    """
    No X-Tenant-ID scoping: the caller is a platform-wide, pre-Organization
    accountability point (TDS-017), not acting within any Organization's
    own tenant boundary — see middleware/tenant.py's exemption list, which
    this path is added to, mirroring /auth/authority-login's own basis.
    """
    tenant, organization_id = await tenant_establishment_service.establish(
        request.organization_id, actor_id=claims.get("person_id")
    )
    return TenantResponse(
        id=tenant.id,
        organization_id=organization_id,
        tenant_code=tenant.tenant_code,
        lifecycle_state=tenant.lifecycle_state,
        version=tenant.version,
        approved_by_actor_id=tenant.approved_by_actor_id,
        approved_at=tenant.approved_at,
        allocated_by_actor_id=tenant.allocated_by_actor_id,
        allocated_at=tenant.allocated_at,
        created_at=tenant.created_at,
    )
