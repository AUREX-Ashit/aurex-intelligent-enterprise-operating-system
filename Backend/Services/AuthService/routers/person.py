from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import db_manager
from repositories.identity_repository import IdentityRepository
from repositories.person_repository import PersonRepository
from schemas.person import (
    AuthoritativePersonContext,
    EstablishPersonRequest,
    PersonReferenceRequest,
    PersonRecognitionResponse,
)
from services.establish_person_context_service import EstablishPersonContextService
from services.person_recognition_service import PersonRecognitionService

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


async def get_person_recognition_service(
    identity_repo: Annotated[IdentityRepository, Depends(get_identity_repository)],
) -> PersonRecognitionService:
    return PersonRecognitionService(identity_repo)


async def get_establish_person_context_service(
    recognition_service: Annotated[PersonRecognitionService, Depends(get_person_recognition_service)],
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> EstablishPersonContextService:
    return EstablishPersonContextService(recognition_service, person_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/recognize",
    response_model=PersonRecognitionResponse,
    status_code=status.HTTP_200_OK,
    summary="Recognize an incoming person reference",
    description=(
        "Determines whether a person matching the supplied reference is already known "
        "to the platform. Only exact matching is supported — no fuzzy, probabilistic, "
        "or AI-assisted matching is performed. An unmatched reference returns "
        "NO_CANDIDATE without ranking or suggesting candidates. This endpoint does not "
        "require a tenant context."
    ),
    responses={
        200: {"description": "Recognition completed — outcome is MATCHED or NO_CANDIDATE either way."},
        422: {"description": "Invalid request (e.g., malformed email)."},
    },
)
async def recognize_person(
    reference: PersonReferenceRequest,
    recognition_service: Annotated[PersonRecognitionService, Depends(get_person_recognition_service)],
) -> PersonRecognitionResponse:
    """
    EX-C006-01 handler. No Authorization dependency: the canonical
    specification states no Access Evaluation Outcome requirement for this
    Experience (unlike EX-C001-01's BR-C001-03), consistent with Person
    Management's bootstrap-safe design (URA-001-15).
    """
    return await recognition_service.recognize(reference)


@router.post(
    "/establish",
    response_model=AuthoritativePersonContext,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new person",
    description=(
        "Creates a new person record, after confirming that no existing person matches "
        "the supplied reference. Does not create a login credential or any organization "
        "membership — those are established separately. This endpoint does not require "
        "a tenant context."
    ),
    responses={
        201: {"description": "Person established."},
        409: {"description": "An existing person already matches the supplied reference; nothing was created."},
        422: {"description": "Invalid request (e.g., malformed email, or a missing/empty required field)."},
    },
)
async def establish_person(
    request: EstablishPersonRequest,
    establish_service: Annotated[EstablishPersonContextService, Depends(get_establish_person_context_service)],
) -> AuthoritativePersonContext:
    """
    EX-C006-02 handler. No Authorization dependency, for the same reason as
    EX-C006-01 (URA-001-15). Internally re-runs EX-C006-01's recognition
    (PersonRecognitionService) against the supplied email as a runtime
    precondition check, per EX-C006-02's own Trigger — the caller's word
    that recognition already ran is not trusted.

    Tenant independence: establishing a person happens before any
    organization link exists for them — that link is created separately,
    later, once the person is already known. Since there is no organization
    to scope this request to yet, requiring one here would be asking for
    information that cannot exist at this point.
    """
    return await establish_service.establish(request)
