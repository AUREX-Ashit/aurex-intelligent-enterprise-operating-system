from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.c022_commercial_account_repository import (
    C022CommercialAccountRepository,
)
from schemas.commercial_account import (
    CommercialAccountResponse,
    EstablishCommercialAccountRequest,
)
from services.commercial_account_service import CommercialAccountService

router = APIRouter()


async def get_commercial_account_service(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> CommercialAccountService:
    return CommercialAccountService(C022CommercialAccountRepository(session))


@router.post(
    "",
    response_model=CommercialAccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a Commercial Account (C-022, WP-21 BA-01)",
    description=(
        "Establish one standalone Authoritative Commercial Account in "
        "`status = 'active'` (`ROD-C022` §H/D1/D5). Produces the first "
        "Authoritative Commercial Account Context and its stable, "
        "system-assigned Account Reference (`COM-001-001` `PREFIX-NNNNNN`). "
        "PLATFORM-GLOBAL — no `organization_id` and no `X-Tenant-ID` header "
        "(`ROD-C022` D2; `/commercial-accounts` is tenant-middleware-exempt "
        "on the same basis as `/roles`/`/offerings`). No `classification` "
        "field exists (`ADR-038` Option A). No read/list endpoint exists "
        "(`ROD-C022-A` D8) — establish-only. No Customer, Customer–Account "
        "Relationship, reclassification, retirement/reactivation, merge/"
        "split/transfer, Subscription/Billing/Contract/Entitlement "
        "semantics are implemented."
    ),
    responses={
        201: {"description": "Commercial Account established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        409: {"description": "A unique Account Reference could not be allocated; retry."},
        422: {"description": "Invalid body (blank account_name)."},
    },
)
async def establish_commercial_account(
    request: EstablishCommercialAccountRequest,
    service: Annotated[CommercialAccountService, Depends(get_commercial_account_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> CommercialAccountResponse:
    row = await service.establish(request, actor_id=claims.get("person_id"))
    return CommercialAccountResponse.model_validate(row)
