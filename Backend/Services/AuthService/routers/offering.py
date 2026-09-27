from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.c021_offering_definition_repository import (
    C021OfferingDefinitionRepository,
)
from schemas.offering import (
    EstablishOfferingDefinitionRequest,
    OfferingDefinitionResponse,
)
from services.offering_definition_service import OfferingDefinitionService

router = APIRouter()


async def get_offering_service(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OfferingDefinitionService:
    return OfferingDefinitionService(C021OfferingDefinitionRepository(session))


@router.post(
    "",
    response_model=OfferingDefinitionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish an Offering Definition (C-021, WP-20 BA-01)",
    description=(
        "Establish one standalone Atomic Offering Definition in `state = "
        "'draft'` (`ROD-C021` D4/D7). Produces the first Authoritative "
        "Offering Definition Context and its stable, system-assigned Offering "
        "Reference (`COM-001-001` `PREFIX-NNNNNN`, `[RO DECISION]` O1). "
        "PLATFORM-GLOBAL — the C-021 catalog is one enterprise-wide catalog; "
        "there is no `organization_id` and no `X-Tenant-ID` header "
        "(`ROD-C021` D8; the `/offerings` prefix is tenant-middleware-exempt "
        "on the same basis as `/roles`). `category_ref` is OPTIONAL "
        "(`[RO DECISION]` O2) — omit it and it persists NULL; a supplied "
        "value must be non-empty. `list_price_reference` is an opaque "
        "reference string only, never a number (`ROD-C021` D6). No "
        "composition, relationships, publication, retirement, pricing "
        "computation, Subscription, Customer/Account, or Entitlement "
        "semantics are implemented (`ROD-C021` D3/D5/D6/D7; C-023 Decision 3 "
        "untouched)."
    ),
    responses={
        201: {"description": "Offering Definition established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        409: {"description": "A unique Offering Reference could not be allocated; retry."},
        422: {"description": "Invalid body (bad offering_kind, blank offering_name, blank category_ref)."},
    },
)
async def establish_offering_definition(
    request: EstablishOfferingDefinitionRequest,
    service: Annotated[OfferingDefinitionService, Depends(get_offering_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OfferingDefinitionResponse:
    row = await service.establish(request, actor_id=claims.get("person_id"))
    return OfferingDefinitionResponse.model_validate(row)


@router.get(
    "",
    response_model=list[OfferingDefinitionResponse],
    summary="List Offering Definitions (C-021, WP-20 BA-01)",
    description=(
        "Every Offering Definition in the one platform-global C-021 catalog, "
        "newest first (`ROD-C021` D4/D8). No tenant filter — the catalog is "
        "enterprise-wide, mirroring `/roles`. Hard-capped; pagination is a "
        "disclosed implementation-time follow-up (`TDS-C021 §27`)."
    ),
    responses={
        200: {"description": "The platform-global offering catalog (possibly empty)."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
    },
)
async def list_offering_definitions(
    service: Annotated[OfferingDefinitionService, Depends(get_offering_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> list[OfferingDefinitionResponse]:
    rows = await service.list_offerings()
    return [OfferingDefinitionResponse.model_validate(row) for row in rows]


@router.get(
    "/{offering_id}",
    response_model=OfferingDefinitionResponse,
    summary="Read one Offering Definition (C-021, WP-20 BA-01)",
    description=(
        "One Offering Definition by id. The catalog is platform-global, so "
        "every row is visible to any PLATFORM_ADMIN; an unknown id is a "
        "plain 404 (no anti-enumeration nuance is required, unlike the "
        "tenant-scoped C-023/C-132 read paths). `TDS-C021 §13`."
    ),
    responses={
        200: {"description": "The Offering Definition."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No Offering Definition with this id."},
    },
)
async def read_offering_definition(
    offering_id: UUID,
    service: Annotated[OfferingDefinitionService, Depends(get_offering_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OfferingDefinitionResponse:
    row = await service.get_offering(offering_id)
    return OfferingDefinitionResponse.model_validate(row)
