"""
Enterprise BAR — WP-23 Workstream C, canonical Business Activity
registration mechanism.

Governance baseline (re-confirmed, not reopened):
  * D2 (`ROD-ENTERPRISE-BAR-Decision-Preparation.md §0b`) — cataloguing/
    registration and canonical identity are two of BAR's four LOCKED-
    minimum responsibilities; this service discharges both together, in
    one atomic act, per registration.
  * D5 (`§0d`) — BAR is the canonical Business Activity Identifier
    authority, identifier assigned at BAR registration. This service is
    where that assignment actually occurs.
  * D7 (`§0f`) — BAR keeps its own registration record, separate from
    `WPR-001` and `CBOR-INDEX.md`. Neither is modified here.
  * RD-23-03 (layered authority model,
    `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0`):
      - the registering act is the governance authority for a
        registration (authorized by whom, under which act, and why);
      - this service writes the execution-time runtime record
        (`bar_registration`) that BAR logic consults;
      - `BAR-INDEX.md` is the human governance catalogue;
      - a runtime row alone does not establish that the governance
        authorization exists. `registering_act` is a citation, not
        verified here, and reconciliation between the governance record
        and the runtime record is required but not implemented by this
        service.

Scope boundary (WP-23 Workstream C only — re-confirmed before writing this
module):
  * This service registers a Business Activity. It does NOT implement
    discovery (Workstream D), the execution-time gate (Workstream E), the
    D3 retroactive cutover of the 21 existing rows (Workstream F), or any
    C-024 integration (Workstream H). None of those is called from here.
  * No HTTP endpoint/router is created — nothing in this repository yet
    calls this service; it is exercised directly by this module's own
    tests, exactly mirroring how Workstream B's own service has no router
    either. A future Workstream (F, or a capability's own future BA
    implementation) will call `register()` directly.
  * This service does NOT populate `BAR-INDEX.md`. The index is the
    governance catalogue, maintained alongside each registering act, not
    a runtime output of this service. RD-23-03 requires the governance
    record and this runtime record to stay traceably related, but it
    does not decide the reconciliation mechanism, and none is
    implemented here.

Atomicity design, disclosed as `[IMPLEMENTATION DESIGN]`: this service
does NOT call `BarIdentifierService.issue_identifier()`, because issuance
and registration must succeed or fail as one unit. Instead it uses
`BarIdentifierRepository` directly (the same allocation algorithm, model
and `BAR_IDENTIFIER_PREFIX`) and inserts the ledger row and the
registration row together, in one savepoint per attempt, so that either
both succeed together or both roll back together.

Transaction ownership (Gate 3 remediation of VV-F-01 / VV-F-02, 2026-09-26):
  * The caller owns the transaction: this service never commits and never
    rolls back the caller's session. Commit or rollback is the caller's.
  * The caller's pending work is flushed once, before allocation, so a
    failure in it surfaces unchanged and is not classified as a collision.
  * Each allocation attempt runs in `session.begin_nested()` (a SAVEPOINT).
    An `IntegrityError` rolls back only that attempt's two inserts; the
    caller's other pending or flushed work, including earlier registrations
    in the same session, is preserved.
  * After a failed attempt, the failure is classified: a concurrent duplicate
    (same work package and reference) raises `BarRegistrationAlreadyExists`;
    a candidate identifier that is now issued is a genuine collision and is
    retried; any other integrity failure is re-raised unchanged, never
    retried and never reported as allocation exhaustion.
  * On success the savepoint is released into the caller's transaction.
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from models.bar_identifier_ledger import BAR_IDENTIFIER_PREFIX, BarIdentifierLedger
from models.bar_registration import BarRegistration
from observability import AuditStatus, publish_event, record_audit
from repositories.bar_identifier_repository import BarIdentifierRepository
from repositories.bar_registration_repository import BarRegistrationRepository

_REGISTER_ACTION = "BAR_REGISTER_BUSINESS_ACTIVITY"
_ALLOCATION_MAX_RETRIES = 5


class BarRegistrationAlreadyExists(RuntimeError):
    """
    Raised when a Business Activity matching the same
    `(owning_work_package, business_activity_reference)` pair is already
    registered. Not retried with a new identifier — a duplicate is not
    fixed by allocating a different `BA-NNNNNN` value.
    """


class BarRegistrationAllocationExhausted(RuntimeError):
    """Raised when `_ALLOCATION_MAX_RETRIES` consecutive identifier collisions occur."""


class BarRegistrationService:
    """Writes the enterprise BAR's runtime Business Activity registration record (D2, D5, D7; RD-23-03: the registering act, not this service, is the governance authority)."""

    def __init__(
        self,
        registration_repo: BarRegistrationRepository,
        identifier_repo: BarIdentifierRepository,
    ) -> None:
        self.registration_repo = registration_repo
        self.identifier_repo = identifier_repo
        # Both repositories must share one session/transaction — this is
        # what makes the identifier-issuance insert and the registration
        # insert atomic together. Enforced defensively, not merely assumed.
        if registration_repo.session is not identifier_repo.session:
            raise ValueError(
                "BarRegistrationService requires registration_repo and "
                "identifier_repo to share the same session, so both "
                "inserts commit or roll back together."
            )

    async def register(
        self,
        *,
        business_activity_reference: str,
        owning_capability: str,
        owning_work_package: str,
        registering_act: str,
        is_retroactive: bool,
        actor_id: str | None = None,
    ) -> BarRegistration:
        """
        Register one Business Activity: allocate its canonical
        `BA-NNNNNN` identifier and persist its registration record,
        atomically. Returns the persisted `BarRegistration` row.

        Mandatory fields, exactly the eight already approved
        (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md
        §4`): Identifier (assigned here), Reference, Owning Capability,
        Owning Work Package, Registration Status (always `REGISTERED` on
        success), Registering Act, Registration Date (assigned here),
        Retroactive flag.
        """
        self._validate_required_fields(
            business_activity_reference=business_activity_reference,
            owning_capability=owning_capability,
            owning_work_package=owning_work_package,
            registering_act=registering_act,
        )

        # Friendlier-error fast path — NOT the authoritative protection.
        # The `uq_bar_registration_wp_reference` database constraint,
        # checked again below after any collision, is the real backstop
        # against a race between two concurrent callers requesting the
        # same (work package, reference) pair.
        existing = await self.registration_repo.get_by_work_package_and_reference(
            owning_work_package, business_activity_reference
        )
        if existing is not None:
            self._audit_denied(
                reason="Business Activity already registered",
                owning_work_package=owning_work_package,
                business_activity_reference=business_activity_reference,
                actor_id=actor_id,
            )
            raise BarRegistrationAlreadyExists(
                f"A Business Activity is already registered for "
                f"work package '{owning_work_package}' with reference "
                f"'{business_activity_reference}' (identifier {existing.identifier})."
            )

        session = self.registration_repo.session
        # The caller owns the transaction. Flush the caller's own pending
        # work first, outside the collision handler, so that a failure in
        # it surfaces as itself and is never mistaken for a collision.
        await session.flush()

        last_error: IntegrityError | None = None
        for _ in range(_ALLOCATION_MAX_RETRIES):
            candidate = await self._next_identifier()
            try:
                # Each attempt (ledger insert + registration insert) runs in
                # a SAVEPOINT, so a failed attempt rolls back only its own two
                # inserts, never the caller's other work, including earlier
                # registrations in the same session (VV-F-01). On success the
                # savepoint is released into the caller's transaction, which
                # the caller still commits.
                async with session.begin_nested():
                    session.add(BarIdentifierLedger(identifier=candidate))
                    registration = await self.registration_repo.create(
                        {
                            "identifier": candidate,
                            "business_activity_reference": business_activity_reference,
                            "owning_capability": owning_capability,
                            "owning_work_package": owning_work_package,
                            "registering_act": registering_act,
                            "is_retroactive": is_retroactive,
                        }
                    )
                    await session.flush()
                break
            except IntegrityError as exc:
                last_error = exc
                # Classify the failure. Only the first two outcomes are
                # expected races; anything else is re-raised (VV-F-02):
                #   1. the (work package, reference) pair won a concurrent
                #      race — not retryable, a new identifier does not fix a
                #      duplicate;
                #   2. the identifier candidate is now issued by someone
                #      else — a genuine collision, retried with a fresh one;
                #   3. any other integrity failure — not a collision, never
                #      retried and never reported as exhaustion.
                raced = await self.registration_repo.get_by_work_package_and_reference(
                    owning_work_package, business_activity_reference
                )
                if raced is not None:
                    self._audit_denied(
                        reason="Business Activity already registered (concurrent)",
                        owning_work_package=owning_work_package,
                        business_activity_reference=business_activity_reference,
                        actor_id=actor_id,
                    )
                    raise BarRegistrationAlreadyExists(
                        f"A concurrent request already registered work package "
                        f"'{owning_work_package}' with reference "
                        f"'{business_activity_reference}' (identifier {raced.identifier})."
                    ) from exc
                if not await self.identifier_repo.is_issued(candidate):
                    record_audit(
                        action=_REGISTER_ACTION,
                        resource="bar_registration:allocation",
                        status=AuditStatus.FAILED,
                        actor_id=actor_id or "SYSTEM",
                        metadata={
                            "reason": "integrity failure that is not an identifier collision",
                            "owning_work_package": owning_work_package,
                            "business_activity_reference": business_activity_reference,
                        },
                    )
                    raise
                continue
        else:
            self._audit_denied(
                reason="BA-NNNNNN allocation exhausted retries during registration",
                owning_work_package=owning_work_package,
                business_activity_reference=business_activity_reference,
                actor_id=actor_id,
            )
            raise BarRegistrationAllocationExhausted(
                "Could not allocate a unique Business Activity Identifier for registration; retry."
            ) from last_error

        record_audit(
            action=_REGISTER_ACTION,
            resource=f"bar_registration:{registration.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "identifier": registration.identifier,
                "business_activity_reference": registration.business_activity_reference,
                "owning_capability": registration.owning_capability,
                "owning_work_package": registration.owning_work_package,
                "registering_act": registration.registering_act,
                "is_retroactive": registration.is_retroactive,
            },
        )
        publish_event(
            "BAR_BUSINESS_ACTIVITY_REGISTERED",
            {
                "identifier": registration.identifier,
                "owning_capability": registration.owning_capability,
                "owning_work_package": registration.owning_work_package,
            },
        )
        return registration

    async def _next_identifier(self) -> str:
        current_max = await self.identifier_repo.max_identifier_sequence()
        return f"{BAR_IDENTIFIER_PREFIX}-{current_max + 1:06d}"

    @staticmethod
    def _validate_required_fields(
        *,
        business_activity_reference: str,
        owning_capability: str,
        owning_work_package: str,
        registering_act: str,
    ) -> None:
        for name, value in (
            ("business_activity_reference", business_activity_reference),
            ("owning_capability", owning_capability),
            ("owning_work_package", owning_work_package),
            ("registering_act", registering_act),
        ):
            if not value or not value.strip():
                raise ValueError(f"'{name}' is required and must not be blank.")

    def _audit_denied(
        self,
        *,
        reason: str,
        owning_work_package: str,
        business_activity_reference: str,
        actor_id: str | None,
    ) -> None:
        record_audit(
            action=_REGISTER_ACTION,
            resource="bar_registration:allocation",
            status=AuditStatus.DENIED,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "reason": reason,
                "owning_work_package": owning_work_package,
                "business_activity_reference": business_activity_reference,
            },
        )
