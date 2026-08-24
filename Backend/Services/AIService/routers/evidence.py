# routers/evidence.py
"""
WP-15 BA-01 — Understand Evidence Context (C-066 Evidence Management,
`TDS-015`). A dedicated router, deliberately not added to
`routers/search.py` (C-093's own capability router) — mixing the two
would blur capability ownership between C-093 and C-066 (`TDS-015 §9`).
"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims
from models.database import get_db
from repositories.search_repository import EvidenceRegistryRepository
from schemas.evidence import EvidenceListResponse, EvidenceResponse
from services.evidence_context_service import EvidenceContextService

router = APIRouter(prefix="/evidence", tags=["Evidence"])

_INVALID_TOKEN = "Credentials verification failed."


def _require_organization_id(claims: dict) -> UUID:
    """
    Gate 2 V&V remediation (Finding C-2): a validly-signed JWT missing the
    `organization_id` claim previously caused an unhandled `KeyError` (HTTP
    500) at `UUID(claims["organization_id"])`. `AuthService` always issues
    this claim (`dependencies.decode_access_token`'s own docstring) — this
    is a defensive guard against a malformed/incomplete token, not a change
    to normal authentication behavior. Raises the same 401 `dependencies.
    get_current_claims` already raises for an otherwise-invalid token,
    rather than inventing a new error shape — scoped to these two BA-01
    endpoints only, not a change to `dependencies.py` or any other router.
    """
    raw_organization_id = claims.get("organization_id")
    if raw_organization_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_INVALID_TOKEN)
    return UUID(raw_organization_id)


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_evidence_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> EvidenceRegistryRepository:
    return EvidenceRegistryRepository(session)


async def get_evidence_context_service(
    evidence_repo: Annotated[EvidenceRegistryRepository, Depends(get_evidence_repo)],
) -> EvidenceContextService:
    return EvidenceContextService(evidence_repo)


# ---------------------------------------------------------------------------
# BA-01 — Understand Evidence Context
# ---------------------------------------------------------------------------

@router.get(
    "/{evidence_id}",
    response_model=EvidenceResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Evidence by id (WP-15 BA-01)",
    description=(
        "Read-only, no write/mutate/delete path exists (`TDS-015 §1`/§7). Any "
        "authenticated caller may retrieve their own Organization's own Evidence "
        "(`RO-DEC-C066-BA01-03`, Option C — no `PLATFORM_ADMIN` requirement for "
        "ordinary same-Organization reads). `PLATFORM_ADMIN` may additionally "
        "retrieve any other Organization's row. A foreign Organization's "
        "`evidence_id`, for a non-`PLATFORM_ADMIN` caller, returns 404 — never a "
        "403 that would disclose the row's own existence (`TDS-015 §5`)."
    ),
)
async def get_evidence(
    evidence_id: UUID,
    claims: Annotated[dict, Depends(get_current_claims)],
    service: Annotated[EvidenceContextService, Depends(get_evidence_context_service)],
) -> EvidenceResponse:
    organization_id = _require_organization_id(claims)
    is_platform_admin = claims.get("role_code") == "PLATFORM_ADMIN"
    return await service.get_by_id(organization_id, evidence_id, is_platform_admin=is_platform_admin)


@router.get(
    "",
    response_model=EvidenceListResponse,
    status_code=status.HTTP_200_OK,
    summary="List visible Evidence (WP-15 BA-01)",
    description=(
        "Always scoped to the caller's own Organization, for every caller including "
        "`PLATFORM_ADMIN` — no cross-Organization listing capability exists "
        "(`RO-DEC-C066-BA01-05`); no target-Organization selector is accepted. "
        "Filters are independently optional, additive `AND` predicates. An empty "
        "result is a valid 200, not a 404."
    ),
)
async def list_evidence(
    claims: Annotated[dict, Depends(get_current_claims)],
    service: Annotated[EvidenceContextService, Depends(get_evidence_context_service)],
    linked_entity_type: str | None = None,
    linked_entity_id: UUID | None = None,
    evidence_source: str | None = None,
    evidence_type: str | None = None,
) -> EvidenceListResponse:
    organization_id = _require_organization_id(claims)
    return await service.list_visible(
        organization_id,
        linked_entity_type=linked_entity_type,
        linked_entity_id=linked_entity_id,
        evidence_source=evidence_source,
        evidence_type=evidence_type,
    )
