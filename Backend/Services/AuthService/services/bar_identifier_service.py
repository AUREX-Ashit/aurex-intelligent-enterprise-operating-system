"""
Enterprise BAR — WP-23 Workstream B, Business Activity Identifier issuance
mechanism.

Governance baseline (re-confirmed, not reopened):
  * D2 (`ROD-ENTERPRISE-BAR-Decision-Preparation.md §0b`) — canonical
    Business Activity identity is one of BAR's four LOCKED-minimum
    responsibilities.
  * D5 (`§0d`) — BAR is the canonical Business Activity Identifier
    authority; the identifier is assigned at BAR registration, never
    earlier.
  * `[IMPLEMENTATION DESIGN — not constitutional text]` — the concrete
    `BA-NNNNNN` format (six-digit, zero-padded, sequential, starting at
    `BA-000001`) is an engineering choice
    (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md
    §5`), justified by the `BA-000089` illustrative example already used
    identically in `SD-002-004`/`CMD-001 §26.4a`/`IMP-001 §6.22.1b`, and
    by the six-digit sequential pattern every existing CBOR identifier in
    this repository already uses.

Scope boundary (WP-23 Workstream B only — re-confirmed before writing this
module, not assumed):
  * This service ONLY issues an identifier. It does NOT register a
    Business Activity, does NOT populate `BAR-INDEX.md`, does NOT perform
    discovery, does NOT implement the execution-time gate, and does NOT
    perform the D3 retroactive cutover of the 21 existing Business
    Activities. Those remain Workstreams C, D, E, and F respectively,
    none of which is implemented here.
  * No HTTP endpoint/router is created for this workstream — there is
    nothing meaningful to expose yet (registering nothing but an
    identifier, unattached to any Business Activity, is not itself a
    caller-facing operation). Workstream C will call
    `issue_identifier()` in-process, inside its own fuller registration
    transaction, once it exists.
  * No identifier is issued to any of the 21 existing Business Activities
    or to C-024 BA-01 by this module's own existence — issuance is a
    capability, not an act; nothing in this codebase currently invokes
    it outside this module's own tests.

Allocation mechanism, mirroring the already-certified
`OfferingDefinitionService._next_offering_reference`/`establish()` pattern
(`[RO DECISION]` O1) as the established repository convention:
`MAX(existing suffix) + 1`, formatted `BA-NNNNNN`, with the `identifier`
column's own UNIQUE constraint as the concurrency backstop and an
allocate-and-retry on collision. No PostgreSQL SEQUENCE.

Gap disclosure (per the governing instruction: gaps must not be silently
described as impossible unless the persistence mechanism actually
guarantees it): once an issuance INSERT commits, that identifier is
permanently issued and the sequence cannot skip a number out from under
it — the next `MAX+1` read will always see it. If an issuance's own
surrounding transaction is rolled back before commit (e.g. the caller
aborts, or a later step in a larger Workstream-C transaction fails), the
INSERT rolls back too and the number becomes available for reissue — this
produces no permanent gap. What this mechanism does NOT prevent, and does
not claim to prevent, is a committed identifier that is never
subsequently attached to any Business Activity (an "issued but orphaned"
identifier) — that is a possible, disclosed condition inherent in
decoupling issuance from registration (per the design's own §19a.6
separation), and its handling (if any) is left to Workstream C, not
resolved here.
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from models.bar_identifier_ledger import BAR_IDENTIFIER_PREFIX, BarIdentifierLedger
from observability import AuditStatus, publish_event, record_audit
from repositories.bar_identifier_repository import BarIdentifierRepository

_ISSUE_ACTION = "BAR_ISSUE_BUSINESS_ACTIVITY_IDENTIFIER"
_ALLOCATION_MAX_RETRIES = 5


class BarIdentifierAllocationExhausted(RuntimeError):
    """
    Raised when `_ALLOCATION_MAX_RETRIES` consecutive UNIQUE-constraint
    collisions occur. Mirrors `OfferingDefinitionService.establish`'s own
    HTTP 409 backstop in spirit; this service raises a plain exception
    rather than an HTTP response because it has no router of its own
    (Workstream C's future router, if any, decides how to translate this).
    """


class BarIdentifierService:
    """Business Activity Identifier issuance authority for the enterprise BAR (D5)."""

    def __init__(self, identifier_repo: BarIdentifierRepository) -> None:
        self.identifier_repo = identifier_repo

    async def issue_identifier(self, *, actor_id: str | None = None) -> str:
        """
        Issue and durably persist the next canonical `BA-NNNNNN`
        identifier. Returns the issued identifier as a string.

        This is issuance only — it does not create, reference, or imply
        the existence of any Business Activity. Callers (Workstream C, in
        the future) are responsible for attaching the returned identifier
        to an actual registration record in the same or a subsequent
        transaction.
        """
        session = self.identifier_repo.session
        # The caller owns the transaction. Flush the caller's own pending
        # work first, outside the collision handler, so that a failure in
        # it surfaces as itself and is never mistaken for a collision.
        await session.flush()

        last_error: IntegrityError | None = None
        for _ in range(_ALLOCATION_MAX_RETRIES):
            candidate = await self._next_identifier()
            try:
                # Each attempt runs in a SAVEPOINT, so a failed INSERT rolls
                # back only this attempt, never the caller's other work
                # (VV-F-01). On success the savepoint is released into the
                # caller's transaction, which the caller still commits.
                async with session.begin_nested():
                    row = await self.identifier_repo.create({"identifier": candidate})
                    await session.flush()
                break
            except IntegrityError as exc:
                # Only a genuine collision (the candidate is now issued by
                # someone else) is retried. Any other integrity failure is
                # re-raised unchanged, never reported as exhaustion (VV-F-02).
                if not await self.identifier_repo.is_issued(candidate):
                    record_audit(
                        action=_ISSUE_ACTION,
                        resource="bar_identifier_ledger:allocation",
                        status=AuditStatus.FAILED,
                        actor_id=actor_id or "SYSTEM",
                        metadata={"reason": "integrity failure that is not an identifier collision"},
                    )
                    raise
                last_error = exc
                continue
        else:
            record_audit(
                action=_ISSUE_ACTION,
                resource="bar_identifier_ledger:allocation",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "BA-NNNNNN allocation exhausted retries"},
            )
            raise BarIdentifierAllocationExhausted(
                "Could not allocate a unique Business Activity Identifier; retry."
            ) from last_error

        record_audit(
            action=_ISSUE_ACTION,
            resource=f"bar_identifier_ledger:{row.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"identifier": row.identifier},
        )
        publish_event(
            "BAR_BUSINESS_ACTIVITY_IDENTIFIER_ISSUED",
            {"identifier": row.identifier},
        )
        return row.identifier

    async def _next_identifier(self) -> str:
        current_max = await self.identifier_repo.max_identifier_sequence()
        return f"{BAR_IDENTIFIER_PREFIX}-{current_max + 1:06d}"
