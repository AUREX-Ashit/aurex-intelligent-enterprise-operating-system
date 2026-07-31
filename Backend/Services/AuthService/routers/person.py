from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.identity_repository import IdentityRepository
from repositories.person_correction_repository import PersonCorrectionRepository
from repositories.person_distinction_decision_repository import PersonDistinctionDecisionRepository
from repositories.person_enrichment_repository import PersonEnrichmentRepository
from repositories.person_reconciliation_decision_repository import PersonReconciliationDecisionRepository
from repositories.person_repository import PersonRepository
from schemas.person import (
    AuthoritativePersonContext,
    CorrectPersonRequest,
    DistinguishPersonRequest,
    EnrichPersonRequest,
    EstablishPersonRequest,
    PersonConflictClassificationResponse,
    PersonCorrectionResponse,
    PersonDistinctionDecisionResponse,
    PersonEnrichmentResponse,
    PersonHandoffOutcome,
    PersonHandoffRequest,
    PersonReconciliationDecisionResponse,
    PersonReferenceRequest,
    PersonRecognitionResponse,
    PersonUnderstandingContext,
    ReconcilePersonRequest,
    ResolvePersonConflictRequest,
)
from services.establish_person_context_service import EstablishPersonContextService
from services.person_conflict_service import PersonConflictService
from services.person_correction_service import PersonCorrectionService
from services.person_distinction_service import PersonDistinctionService
from services.person_enrichment_service import PersonEnrichmentService
from services.person_handoff_service import PersonHandoffService
from services.person_reconciliation_service import PersonReconciliationService
from services.person_recognition_service import PersonRecognitionService
from services.person_understanding_service import PersonUnderstandingService

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


async def get_person_distinction_decision_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> PersonDistinctionDecisionRepository:
    return PersonDistinctionDecisionRepository(session)


async def get_person_reconciliation_decision_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> PersonReconciliationDecisionRepository:
    return PersonReconciliationDecisionRepository(session)


async def get_person_correction_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> PersonCorrectionRepository:
    return PersonCorrectionRepository(session)


async def get_person_enrichment_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> PersonEnrichmentRepository:
    return PersonEnrichmentRepository(session)


async def get_person_recognition_service(
    identity_repo: Annotated[IdentityRepository, Depends(get_identity_repository)],
) -> PersonRecognitionService:
    return PersonRecognitionService(identity_repo)


async def get_establish_person_context_service(
    recognition_service: Annotated[PersonRecognitionService, Depends(get_person_recognition_service)],
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> EstablishPersonContextService:
    return EstablishPersonContextService(recognition_service, person_repo)


async def get_person_understanding_service(
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> PersonUnderstandingService:
    return PersonUnderstandingService(person_repo)


async def get_person_distinction_service(
    distinction_repo: Annotated[PersonDistinctionDecisionRepository, Depends(get_person_distinction_decision_repository)],
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> PersonDistinctionService:
    return PersonDistinctionService(distinction_repo, person_repo)


async def get_person_conflict_service(
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> PersonConflictService:
    return PersonConflictService(person_repo)


async def get_person_reconciliation_service(
    reconciliation_repo: Annotated[PersonReconciliationDecisionRepository, Depends(get_person_reconciliation_decision_repository)],
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> PersonReconciliationService:
    return PersonReconciliationService(reconciliation_repo, person_repo)


async def get_person_correction_service(
    correction_repo: Annotated[PersonCorrectionRepository, Depends(get_person_correction_repository)],
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> PersonCorrectionService:
    return PersonCorrectionService(correction_repo, person_repo)


async def get_person_enrichment_service(
    enrichment_repo: Annotated[PersonEnrichmentRepository, Depends(get_person_enrichment_repository)],
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> PersonEnrichmentService:
    return PersonEnrichmentService(enrichment_repo, person_repo)


async def get_person_handoff_service(
    person_repo: Annotated[PersonRepository, Depends(get_person_repository)],
) -> PersonHandoffService:
    return PersonHandoffService(person_repo)


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


@router.get(
    "/{person_id}",
    response_model=PersonUnderstandingContext,
    status_code=status.HTTP_200_OK,
    summary="Understand a Person's authoritative context",
    description=(
        "WP-07 Business Activity: Understand Authoritative Person Context "
        "(C-006) — BA-03, realizing PE-001-C006's EX-C006-03. Read-only — "
        "establishes, corrects, enriches, distinguishes, or reconciles "
        "nothing. Also structurally satisfies EX-C006-09 (Preserve Context) "
        "and EX-C006-12 (Continue) — see IRA-007 §7.1/§7.2. Surfaces only "
        "boolean cross-capability existence signals, never Identity's or "
        "Membership's own data. Requires the PLATFORM_ADMIN role (interim "
        "gate — no Person Steward persona claim exists yet)."
    ),
    responses={
        200: {"description": "The Person's current authoritative context."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No Person exists with the given id."},
    },
)
async def understand_person(
    person_id: UUID,
    understanding_service: Annotated[PersonUnderstandingService, Depends(get_person_understanding_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> PersonUnderstandingContext:
    return await understanding_service.understand(person_id)


@router.post(
    "/distinguish",
    response_model=PersonDistinctionDecisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Distinguish candidate person matches",
    description=(
        "WP-07 Business Activity: Distinguish Candidate Person Matches "
        "(C-006) — BA-04, realizing PE-001-C006's EX-C006-04. Governs "
        "confirmation only — candidate-generation (probabilistic/fuzzy "
        "matching) is out of this Work Package's authorized scope "
        "(IRA-007 §7.3); operates on a caller-supplied candidate set. "
        "Applies identically whether one candidate or several, per the "
        "Recognition Authority Rule (§1.7) — never auto-selects. "
        "Requires the PLATFORM_ADMIN role."
    ),
    responses={
        201: {"description": "Distinction decision recorded."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "A candidate person id does not exist."},
        422: {"description": "selected_person_id inconsistent with decision_type/candidate_person_ids."},
    },
)
async def distinguish_person(
    request: DistinguishPersonRequest,
    distinction_service: Annotated[PersonDistinctionService, Depends(get_person_distinction_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> PersonDistinctionDecisionResponse:
    return await distinction_service.distinguish(request, actor_id=claims.get("person_id"))


@router.post(
    "/{person_id}/resolve-conflict",
    response_model=PersonConflictClassificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify a conflict against an already-identified Person",
    description=(
        "WP-07 Business Activity: Resolve Conflicting Person Context "
        "(C-006) — BA-05, realizing PE-001-C006's EX-C006-05. "
        "Classification only — routes to EX-C006-04 (ambiguity) or "
        "EX-C006-07 (correction need); never resolves the conflict "
        "itself. Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Conflict classified and routed."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Person does not exist."},
    },
)
async def resolve_person_conflict(
    person_id: UUID,
    request: ResolvePersonConflictRequest,
    conflict_service: Annotated[PersonConflictService, Depends(get_person_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> PersonConflictClassificationResponse:
    return await conflict_service.resolve_conflict(person_id, request, actor_id=claims.get("person_id"))


@router.post(
    "/reconcile",
    response_model=PersonReconciliationDecisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Review a potential duplicate Person indication",
    description=(
        "WP-07 Business Activity: Review Potential Duplicate Person "
        "Indication (C-006) — BA-06, realizing PE-001-C006's EX-C006-06. "
        "Records a governed Reconciliation Decision — never a silent "
        "merge. Technical consolidation following a confirmed duplicate "
        "is a downstream data-governance action outside this Enterprise "
        "Experience's own scope. Requires the PLATFORM_ADMIN role."
    ),
    responses={
        201: {"description": "Reconciliation decision recorded."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "One or both persons do not exist."},
        422: {"description": "person_id_a and person_id_b are the same person."},
    },
)
async def reconcile_person(
    request: ReconcilePersonRequest,
    reconciliation_service: Annotated[PersonReconciliationService, Depends(get_person_reconciliation_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> PersonReconciliationDecisionResponse:
    return await reconciliation_service.reconcile(request, actor_id=claims.get("person_id"))


@router.post(
    "/{person_id}/correct",
    response_model=PersonCorrectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Correct an inaccurate authoritative Person fact",
    description=(
        "WP-07 Business Activity: Correct Person Context (C-006) — "
        "BA-07, realizing PE-001-C006's EX-C006-07. Preserves the "
        "pre-correction value permanently in traceability — never a "
        "silent overwrite. Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Fact corrected; prior value preserved."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Person does not exist."},
        422: {"description": "Invalid request (e.g., empty corrected_value)."},
    },
)
async def correct_person(
    person_id: UUID,
    request: CorrectPersonRequest,
    correction_service: Annotated[PersonCorrectionService, Depends(get_person_correction_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> PersonCorrectionResponse:
    return await correction_service.correct(person_id, request, actor_id=claims.get("person_id"))


@router.post(
    "/{person_id}/enrich",
    response_model=PersonEnrichmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enrich a Person's authoritative context",
    description=(
        "WP-07 Business Activity: Enrich Person Context (C-006) — "
        "BA-08, realizing PE-001-C006's EX-C006-08. Additive only — "
        "never overwrites an existing fact; a contradicting candidate "
        "belongs to resolve-conflict, not enrichment. Requires the "
        "PLATFORM_ADMIN role."
    ),
    responses={
        201: {"description": "Enrichment recorded, sourced and sensitivity-classified."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Person does not exist."},
        422: {"description": "Invalid request."},
    },
)
async def enrich_person(
    person_id: UUID,
    request: EnrichPersonRequest,
    enrichment_service: Annotated[PersonEnrichmentService, Depends(get_person_enrichment_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> PersonEnrichmentResponse:
    return await enrichment_service.enrich(person_id, request, actor_id=claims.get("person_id"))


@router.post(
    "/{person_id}/handoff-to-identity",
    response_model=PersonHandoffOutcome,
    status_code=status.HTTP_200_OK,
    summary="Record the outcome of a Person-context hand-off to Identity Establishment",
    description=(
        "WP-07 Business Activity: Hand Off Person Context to Identity "
        "Establishment (C-006) — BA-09, realizing PE-001-C006's "
        "EX-C006-10. C-006 never calls Identity Management's own API "
        "(C-001 has no chartered Work Package) — the caller reports the "
        "outcome, mirroring WP-02 BA-10's own hand-off precedent. The "
        "underlying Person context is always preserved unchanged. "
        "Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Hand-off outcome recorded."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Person does not exist."},
        422: {"description": "outcome is RETURNED without a reason."},
    },
)
async def handoff_person_to_identity(
    person_id: UUID,
    request: PersonHandoffRequest,
    handoff_service: Annotated[PersonHandoffService, Depends(get_person_handoff_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> PersonHandoffOutcome:
    return await handoff_service.handoff(person_id, "C-001", request, actor_id=claims.get("person_id"))


@router.post(
    "/{person_id}/handoff-to-membership",
    response_model=PersonHandoffOutcome,
    status_code=status.HTTP_200_OK,
    summary="Record the outcome of a Person-context hand-off to Membership Establishment",
    description=(
        "WP-07 Business Activity: Hand Off Person Context to Membership "
        "Establishment (C-006) — BA-10, realizing PE-001-C006's "
        "EX-C006-11. C-006 never calls Membership Management's own API "
        "— the caller reports the outcome. The underlying Person "
        "context is always preserved unchanged, regardless of outcome. "
        "Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Hand-off outcome recorded."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Person does not exist."},
        422: {"description": "outcome is RETURNED without a reason."},
    },
)
async def handoff_person_to_membership(
    person_id: UUID,
    request: PersonHandoffRequest,
    handoff_service: Annotated[PersonHandoffService, Depends(get_person_handoff_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> PersonHandoffOutcome:
    return await handoff_service.handoff(person_id, "C-007", request, actor_id=claims.get("person_id"))
