import logging

from schemas.person import (
    AuthoritativePersonContext,
    PersonRecognitionOutcome,
    PersonRecognitionResponse,
    PersonReferenceRequest,
)
from repositories.identity_repository import IdentityRepository

logger = logging.getLogger(__name__)


class PersonRecognitionService:
    """
    Business service layer for EX-C006-01 — Recognize Incoming Person
    Reference (PE-001-C006), deterministic path only.

    Determines, via deterministic recognition, whether an Authoritative
    Person Context already exists for an incoming Person reference.

    Scope boundary: this service implements only the deterministic tier of
    the Recognition Authority Rule (PE-001-C006 §1.7). It does not perform
    probabilistic matching, similarity scoring, AI-assisted matching, or
    candidate ranking — those realize EX-C006-04 (Distinguish Candidate
    Person Matches) and are out of scope for this implementation.
    """

    def __init__(self, identity_repo: IdentityRepository) -> None:
        self.identity_repo = identity_repo

    async def recognize(self, reference: PersonReferenceRequest) -> PersonRecognitionResponse:
        """
        Executes EX-C006-01's deterministic recognition path.

        Deterministic match: the supplied reference resolves to an existing
        Identity, which — per BR-C001-01 — traces to exactly one
        Authoritative Person Context. Confirming that Identity therefore
        confirms the Person; no new Person data is created or inferred.

        No deterministic match: routed, per EX-C006-01's own Context
        Produced field, as a no-candidate signal. This implementation does
        not attempt probabilistic matching before returning NO_CANDIDATE;
        EX-C006-04's candidate-matching tier is unimplemented, not silently
        folded into this outcome.

        Logging never includes the reference value, person name, or any
        other PII — only the outcome, which does not identify an individual.
        """
        logger.info("Person recognition started")

        try:
            # TODO(metrics): increment person_recognition_attempt_total once a
            # metrics abstraction exists on this platform. No framework is
            # introduced here per this correction's explicit constraint.
            identity = await self.identity_repo.get_by_email_with_person(str(reference.email))

            if identity is None:
                logger.info("Person recognition found no candidate")
                # TODO(metrics): increment person_recognition_no_candidate_total.
                response = PersonRecognitionResponse(outcome=PersonRecognitionOutcome.NO_CANDIDATE, person=None)
                logger.info("Person recognition completed (outcome=%s)", response.outcome.value)
                return response

            person = identity.person
            response = PersonRecognitionResponse(
                outcome=PersonRecognitionOutcome.MATCHED,
                person=AuthoritativePersonContext(
                    person_id=person.id,
                    first_name=person.first_name,
                    last_name=person.last_name,
                    display_name=person.display_name,
                ),
            )
            # TODO(metrics): increment person_recognition_match_total.
            logger.info("Person recognition completed (outcome=%s)", response.outcome.value)
            return response
        except Exception:
            logger.exception("Person recognition encountered an unexpected error")
            raise
