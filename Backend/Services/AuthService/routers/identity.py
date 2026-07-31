from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims
from models.database import db_manager
from repositories.identity_recovery_request_repository import IdentityRecoveryRequestRepository
from repositories.identity_repository import IdentityRepository
from repositories.person_repository import PersonRepository
from schemas.identity import (
    ClassifyHandoffRejectionRequest,
    HandoffRejectionOutcome,
    IdentityRecoveryRequestResponse,
    IdentityStatusResponse,
    RecoverIdentityRequest,
)
from services.identity_handoff_classification_service import IdentityHandoffClassificationService
from services.identity_recovery_service import IdentityRecoveryService
from services.identity_status_service import IdentityStatusService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_identity_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> IdentityRepository:
    return IdentityRepository(session)


async def get_person_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> PersonRepository:
    return PersonRepository(session)


async def get_identity_recovery_request_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> IdentityRecoveryRequestRepository:
    return IdentityRecoveryRequestRepository(session)


async def get_identity_status_service(
    identity_repo: Annotated[IdentityRepository, Depends(get_identity_repository)],
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> IdentityStatusService:
    return IdentityStatusService(identity_repo, person_repo)


async def get_identity_recovery_service(
    recovery_repo: Annotated[IdentityRecoveryRequestRepository, Depends(get_identity_recovery_request_repository)],
    identity_repo: Annotated[IdentityRepository, Depends(get_identity_repository)],
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> IdentityRecoveryService:
    return IdentityRecoveryService(recovery_repo, identity_repo, person_repo)


async def get_identity_handoff_classification_service(
    status_service: Annotated[IdentityStatusService, Depends(get_identity_status_service)],
) -> IdentityHandoffClassificationService:
    return IdentityHandoffClassificationService(status_service)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/refresh-status",
    response_model=IdentityStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Detect and resolve disrupted Identity Context (WP-08 BA-01, EX-C001-06)",
    description=(
        "Re-confirms the caller's own current Identity Context against C-006's "
        "Authoritative Person Context rather than trusting the last-known JWT claim "
        "state. Read-only — no audit record or domain event."
    ),
)
async def refresh_identity_status(
    claims: Annotated[dict, Depends(get_current_claims)],
    status_service: Annotated[IdentityStatusService, Depends(get_identity_status_service)],
) -> IdentityStatusResponse:
    identity_id = UUID(claims["identity_id"])
    return await status_service.refresh(identity_id)


@router.post(
    "/recover",
    response_model=IdentityRecoveryRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Recover inaccessible Identity Context, self-service (WP-08 BA-02, EX-C001-07)",
    description=(
        "Records a governed recovery request and its routing determination "
        "(toward new Identity establishment or re-resolution of an existing "
        "Identity). Self-service only: the caller may request recovery for their "
        "own person_id only. Never performs the technical credential-recovery "
        "mechanism, and never executes the routed-to establishment/resolution itself."
    ),
)
async def recover_identity(
    request: RecoverIdentityRequest,
    claims: Annotated[dict, Depends(get_current_claims)],
    recovery_service: Annotated[IdentityRecoveryService, Depends(get_identity_recovery_service)],
) -> IdentityRecoveryRequestResponse:
    if str(request.person_id) != claims["person_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Self-service recovery requests may only be filed for the caller's own person_id.",
        )

    requested_by_identity_id = UUID(claims["identity_id"]) if claims.get("identity_id") else None
    return await recovery_service.request_recovery(
        request, requested_by_identity_id, actor_id=claims.get("person_id")
    )


@router.post(
    "/classify-handoff-rejection",
    response_model=HandoffRejectionOutcome,
    status_code=status.HTTP_200_OK,
    summary="Resolve dependent capability Identity hand-off rejection (WP-08 BA-03, EX-C001-08)",
    description=(
        "Classifies a dependent capability's Identity Context hand-off rejection as "
        "either capability-scoped insufficiency (Identity Context preserved) or an "
        "Identity Context integrity signal (routed to BA-01 for re-resolution). "
        "Computed entirely from the Identity Context's own independently-verifiable "
        "current state, never from the reporting capability's stated reason."
    ),
)
async def classify_handoff_rejection(
    request: ClassifyHandoffRejectionRequest,
    claims: Annotated[dict, Depends(get_current_claims)],
    classification_service: Annotated[
        IdentityHandoffClassificationService, Depends(get_identity_handoff_classification_service)
    ],
) -> HandoffRejectionOutcome:
    return await classification_service.classify(request, actor_id=claims.get("person_id"))
