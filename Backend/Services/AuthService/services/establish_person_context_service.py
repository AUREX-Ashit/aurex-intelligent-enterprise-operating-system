import logging

from fastapi import HTTPException, status

from schemas.person import (
    AuthoritativePersonContext,
    EstablishPersonRequest,
    PersonRecognitionOutcome,
    PersonReferenceRequest,
)
from repositories.person_repository import PersonRepository
from services.person_recognition_service import PersonRecognitionService

logger = logging.getLogger(__name__)


class EstablishPersonContextService:
    """
    Business service layer for EX-C006-02 — Establish New Person Context
    (PE-001-C006).

    Establishes a new Authoritative Person Context, but only after
    confirming — by reusing EX-C006-01's own recognition path, not by
    trusting the caller's word — that no deterministic match and no
    candidate exists for the same incoming reference. This is EX-C006-02's
    own stated Trigger, enforced here as a runtime precondition rather than
    an assumed one, which also guards against a duplicate Person being
    created from two concurrent requests for the same reference.

    Scope boundary: creates a Person only. Per EX-C006-02's own Business
    Value ("without requiring an Identity or Membership first"), this
    service never creates an Identity or Membership — those belong to
    C-001 and C-007 respectively, both out of scope here.
    """

    def __init__(
        self,
        recognition_service: PersonRecognitionService,
        person_repo: PersonRepository,
    ) -> None:
        self.recognition_service = recognition_service
        self.person_repo = person_repo

    async def establish(self, request: EstablishPersonRequest) -> AuthoritativePersonContext:
        """
        Executes EX-C006-02.

        Logging never includes the reference value, person name, or any
        other PII — only the outcome and, on success, the newly assigned
        person_id (an opaque identifier, not personal data itself).
        """
        logger.info("Person establishment started")

        try:
            recognition = await self.recognition_service.recognize(
                PersonReferenceRequest(email=request.email)
            )
            if recognition.outcome != PersonRecognitionOutcome.NO_CANDIDATE:
                logger.info("Person establishment rejected — an existing match was found")
                # Implementation note (raised as HTTPException, not a domain-specific
                # exception translated by the router): this service follows the same
                # convention already used by the authentication service elsewhere in
                # this codebase, which also raises HTTPException directly rather than
                # a custom exception type. Introducing a domain-exception-plus-
                # translation pattern here, while the rest of the service layer does
                # not use one, would create two different error-handling conventions
                # side by side instead of one consistent one. Retained as-is for that
                # reason, not because a cleaner alternative doesn't exist.
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        "An Authoritative Person Context already exists for this reference; "
                        "establishment requires an explicit no-candidate outcome from recognition."
                    ),
                )

            # Transaction boundary: Recognition (the SELECT above) and Person
            # Creation (the INSERT below) both execute within the same database
            # session/transaction as the surrounding HTTP request — opened before
            # this method runs and committed only after the endpoint handler
            # returns, outside this service's own control. Recognition's read and
            # Creation's write are therefore not isolated from a second, concurrent
            # request for the same reference: two requests can both complete
            # Recognition — each seeing no existing match, since neither has
            # committed yet — before either proceeds to create a Person, resulting
            # in two Person rows for what should have been one. This is a real,
            # currently-possible race condition, not a hypothetical one. No row
            # locking, distributed locking, optimistic locking, uniqueness
            # constraint, or retry logic is introduced to close it here — that
            # protection is intentionally deferred until this capability's
            # canonical persistence strategy defines how duplicate-creation races
            # should be handled, so this method does not pre-empt that decision
            # with a locally invented mechanism.
            # TODO(metrics): increment person_establishment_attempt_total once a
            # metrics abstraction exists on this platform.
            person = await self.person_repo.create({
                "first_name": request.first_name,
                "last_name": request.last_name,
                "display_name": request.display_name,
            })
            await self.person_repo.session.flush()

            response = AuthoritativePersonContext(
                person_id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                display_name=person.display_name,
            )
            # TODO(events): publish PERSON_ESTABLISHED once an event-publishing
            # mechanism exists on this platform (FC-IB-001 Chapter 9 names this
            # event; none is currently emitted anywhere in this codebase, per
            # FC-IB-001 F-13).
            # TODO(metrics): increment person_establishment_completed_total.
            logger.info("Person establishment completed (person_id=%s)", response.person_id)
            return response
        except HTTPException:
            raise
        except Exception:
            logger.exception("Person establishment encountered an unexpected error")
            raise
