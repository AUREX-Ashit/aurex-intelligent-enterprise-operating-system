from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.access_evaluation_outcome_repository import AccessEvaluationOutcomeRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from schemas.access_evaluation import (
    AccessContextChangeOutcome,
    AccessEvaluationOutcomeResponse,
    AccessHandoffRejectionOutcome,
    DetectAccessContextChangeRequest,
    EvaluateAccessRequest,
    ExpireAccessEvaluationOutcomeRequest,
    PreserveAccessEvaluationOutcomeRequest,
    ReportAccessHandoffRejectionRequest,
)
from services.access_evaluation_service import AccessEvaluationService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_access_evaluation_outcome_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> AccessEvaluationOutcomeRepository:
    return AccessEvaluationOutcomeRepository(session)


async def get_membership_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> MembershipRepository:
    return MembershipRepository(session)


async def get_domain_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DomainRepository:
    return DomainRepository(session)


async def get_access_evaluation_service(
    outcome_repo: Annotated[AccessEvaluationOutcomeRepository, Depends(get_access_evaluation_outcome_repository)],
    membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)],
    domain_repo: Annotated[DomainRepository, Depends(get_domain_repository)],
) -> AccessEvaluationService:
    return AccessEvaluationService(outcome_repo, membership_repo, domain_repo)


# ---------------------------------------------------------------------------
# BA-01 — Evaluate Access for a Governed Request
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=AccessEvaluationOutcomeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Evaluate Access for a Governed Request (BA-01)",
    description=(
        "WP-05 Business Activity BA-01, realizing PE-001-C002 ERB-C002-01. "
        "Produces an Unresolved or Deferred Access Evaluation Outcome only "
        "(IRA-005 S12) -- Permitted/Denied determination requires a "
        "URA-001-76 resolver not yet authorized for this Work Package and "
        "returns 501 rather than a fabricated decision."
    ),
    responses={
        201: {"description": "An Unresolved or Deferred Access Evaluation Outcome was created."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Domain does not exist."},
        422: {"description": "Invalid request (e.g., permission_level not one of URA-001-47's eight values)."},
        501: {"description": "Permitted/Denied determination is not implemented by this Work Package (IRA-005 S12)."},
    },
)
async def evaluate_access(
    request: EvaluateAccessRequest,
    service: Annotated[AccessEvaluationService, Depends(get_access_evaluation_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> AccessEvaluationOutcomeResponse:
    outcome = await service.evaluate(request)
    return AccessEvaluationOutcomeResponse.model_validate(outcome)


# ---------------------------------------------------------------------------
# BA-02 — Preserve and Bound Access Evaluation Outcome Validity
# ---------------------------------------------------------------------------

@router.post(
    "/{outcome_id}/preserve",
    response_model=AccessEvaluationOutcomeResponse,
    status_code=status.HTTP_200_OK,
    summary="Preserve Access Evaluation Outcome Within Governed Execution Scope (BA-02)",
    description="WP-05 Business Activity BA-02, realizing EX-C002-05. CREATED -> PRESERVED.",
    responses={
        200: {"description": "The outcome is now PRESERVED."},
        404: {"description": "No Access Evaluation Outcome found with this id."},
        409: {"description": "The outcome is not CREATED."},
    },
)
async def preserve_access_evaluation_outcome(
    outcome_id: UUID,
    request: PreserveAccessEvaluationOutcomeRequest,
    service: Annotated[AccessEvaluationService, Depends(get_access_evaluation_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> AccessEvaluationOutcomeResponse:
    outcome = await service.preserve(outcome_id)
    return AccessEvaluationOutcomeResponse.model_validate(outcome)


@router.post(
    "/{outcome_id}/expire",
    response_model=AccessEvaluationOutcomeResponse,
    status_code=status.HTTP_200_OK,
    summary="Expire Access Evaluation Outcome at Scope Boundary (BA-02)",
    description="WP-05 Business Activity BA-02, realizing EX-C002-06. PRESERVED -> EXPIRED. Explicit, caller-invoked -- no automatic time-based expiry.",
    responses={
        200: {"description": "The outcome is now EXPIRED."},
        404: {"description": "No Access Evaluation Outcome found with this id."},
        409: {"description": "The outcome is not PRESERVED."},
    },
)
async def expire_access_evaluation_outcome(
    outcome_id: UUID,
    request: ExpireAccessEvaluationOutcomeRequest,
    service: Annotated[AccessEvaluationService, Depends(get_access_evaluation_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> AccessEvaluationOutcomeResponse:
    outcome = await service.expire(outcome_id)
    return AccessEvaluationOutcomeResponse.model_validate(outcome)


# ---------------------------------------------------------------------------
# BA-03 — Detect and Resolve Access Context Change (classification only)
# ---------------------------------------------------------------------------

@router.post(
    "/{outcome_id}/context-change",
    response_model=AccessContextChangeOutcome,
    status_code=status.HTTP_200_OK,
    summary="Detect and Resolve Access Context Change (BA-03, classification only)",
    description=(
        "WP-05 Business Activity BA-03, realizing EX-C002-07's classification/detection "
        "portion only (IRA-005 S12). Invalidates a live outcome on a reported governing-fact "
        "change; does not itself re-evaluate to a fresh determination."
    ),
    responses={
        200: {"description": "The outcome was invalidated; a fresh BA-01 evaluation is the caller's own next step."},
        404: {"description": "No Access Evaluation Outcome found with this id."},
        409: {"description": "The outcome is not currently live (CREATED or PRESERVED)."},
    },
)
async def detect_access_context_change(
    outcome_id: UUID,
    request: DetectAccessContextChangeRequest,
    service: Annotated[AccessEvaluationService, Depends(get_access_evaluation_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> AccessContextChangeOutcome:
    return await service.detect_context_change(outcome_id, request)


# ---------------------------------------------------------------------------
# BA-04 — Resolve Dependent Capability Access Hand-off Rejection
# ---------------------------------------------------------------------------

@router.post(
    "/{outcome_id}/handoff-rejection",
    response_model=AccessHandoffRejectionOutcome,
    status_code=status.HTTP_200_OK,
    summary="Resolve Dependent Capability Access Hand-off Rejection (BA-04)",
    description="WP-05 Business Activity BA-04, realizing EX-C002-08. Mirrors WP-02 BA-10's own classification pattern.",
    responses={
        200: {"description": "The rejection was classified."},
        404: {"description": "No Access Evaluation Outcome found with this id."},
    },
)
async def resolve_access_handoff_rejection(
    outcome_id: UUID,
    request: ReportAccessHandoffRejectionRequest,
    service: Annotated[AccessEvaluationService, Depends(get_access_evaluation_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> AccessHandoffRejectionOutcome:
    return await service.resolve_handoff_rejection(outcome_id, request)
