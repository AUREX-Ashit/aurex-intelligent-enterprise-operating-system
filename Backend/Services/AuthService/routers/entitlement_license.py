from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims, require_approval_authority
from middleware.tenant import get_current_tenant
from models.database import db_manager
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.c023_entitlement_context_repository import C023EntitlementContextRepository
from repositories.c023_license_context_repository import C023LicenseContextRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from repositories.organization_repository import OrganizationRepository
from schemas.entitlement_license import (
    ContextOutcomeResponse,
    EntitlementContextResponse,
    EstablishEntitlementLicenseRequest,
    EstablishEntitlementLicenseResponse,
    LicenseContextResponse,
)
from services.entitlement_license_establishment_service import (
    COMMIT_AUTHORITY_NAME,
    EntitlementLicenseEstablishmentService,
)

router = APIRouter()


async def get_entitlement_license_service(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> EntitlementLicenseEstablishmentService:
    return EntitlementLicenseEstablishmentService(
        license_repo=C023LicenseContextRepository(session),
        entitlement_repo=C023EntitlementContextRepository(session),
        membership_repo=MembershipRepository(session),
        organization_repo=OrganizationRepository(session),
        domain_repo=DomainRepository(session),
        approval_authority_repo=ApprovalAuthorityRepository(session),
    )


@router.post(
    "",
    response_model=EstablishEntitlementLicenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish an Authoritative Entitlement and/or License Context (C-023, WP-17 BA-01)",
    description=(
        "Administrative establish (continuing) outcome only — `(none) -> ACTIVE` "
        "(`WP-17 §9`; `TDS-C023 §4`). One call may establish a License "
        "(Membership-anchored) and/or an Entitlement (Organization-anchored, "
        "optionally Domain-scoped). Requires the caller to satisfy the "
        f"currently-ACTIVE '{COMMIT_AUTHORITY_NAME}' Approval Authority for the "
        "X-Tenant-ID Organization, resolved via the certified WP-18 mechanism "
        "(fail-closed, ANY_ONE strategy only, no PLATFORM_ADMIN / AUREX_ADMIN "
        "bypass). `membership.license_type` is never written or duplicated "
        "(Decision 6). Suspend / revoke / reactivate and Consumption / "
        "Allocation / Catalog / Billing / Subscription semantics are out of "
        "scope (`WP-17 §19`)."
    ),
    responses={
        201: {"description": "Context(s) established."},
        400: {"description": "Missing/malformed Authorization or X-Tenant-ID header."},
        401: {"description": "Access token invalid or expired."},
        403: {
            "description": (
                f"The '{COMMIT_AUTHORITY_NAME}' Approval Authority is not satisfied, "
                "or an anchor belongs to a different Organization than X-Tenant-ID."
            )
        },
        404: {"description": "Target Membership / Organization / Domain not found."},
        409: {"description": "A current Authoritative Context already exists for the anchor (INV-C023-09 / -10)."},
        422: {
            "description": (
                "Invalid request, or the Entitlement Type is not recognized (the Global "
                "Entitlement Type Catalog — Decision 3 — is deferred; the Entitlement half "
                "is vacuously blocked)."
            )
        },
    },
)
async def establish_entitlement_license_context(
    request: EstablishEntitlementLicenseRequest,
    service: Annotated[EntitlementLicenseEstablishmentService, Depends(get_entitlement_license_service)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant)],
    claims: Annotated[dict, Depends(require_approval_authority(COMMIT_AUTHORITY_NAME))],
) -> EstablishEntitlementLicenseResponse:
    license_row, entitlement_row = await service.establish(
        target_organization_id=tenant_id,
        actor_id=claims.get("person_id"),
        establish_license=request.membership_id is not None,
        establish_entitlement=request.organization_id is not None,
        membership_id=request.membership_id,
        organization_id=request.organization_id,
        domain_id=request.domain_id,
        entitlement_type_ref=request.entitlement_type_ref,
        c023_license_type=request.c023_license_type,
        entitlement_source_reference=request.entitlement_source_reference,
        effective_from=request.effective_from,
        effective_to=request.effective_to,
    )
    return EstablishEntitlementLicenseResponse(
        license=LicenseContextResponse.model_validate(license_row) if license_row is not None else None,
        entitlement=EntitlementContextResponse.model_validate(entitlement_row) if entitlement_row is not None else None,
    )


@router.get(
    "/{context_id}",
    response_model=ContextOutcomeResponse,
    summary="Display the resulting establishment/status outcome for one context (C-023, WP-17 BA-01)",
    description=(
        "Frontend item 2 (`TDS-C023 §17.2`) — the immediate resulting "
        "establishment/status outcome (type, anchor, effective period, current "
        "status) for a just-established Authoritative License or Entitlement "
        "Context. Tenant-isolated: a context id belonging to a different "
        "Organization than X-Tenant-ID returns 404, never a disclosure that it "
        "exists elsewhere. Not a standing/history dashboard."
    ),
    responses={
        200: {"description": "The context outcome."},
        400: {"description": "Missing/malformed Authorization or X-Tenant-ID header."},
        401: {"description": "Access token invalid or expired."},
        404: {"description": "No such context in this Organization."},
    },
)
async def get_entitlement_license_context_outcome(
    context_id: UUID,
    service: Annotated[EntitlementLicenseEstablishmentService, Depends(get_entitlement_license_service)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant)],
    claims: Annotated[dict, Depends(get_current_claims)],
) -> ContextOutcomeResponse:
    kind, row = await service.get_context_for_tenant(context_id, tenant_id)
    if kind == "LICENSE":
        return ContextOutcomeResponse(kind=kind, license=LicenseContextResponse.model_validate(row))
    return ContextOutcomeResponse(kind=kind, entitlement=EntitlementContextResponse.model_validate(row))
