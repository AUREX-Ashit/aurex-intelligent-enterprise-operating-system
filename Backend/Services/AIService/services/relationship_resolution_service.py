# services/relationship_resolution_service.py
"""
WP-14 BA-05 — Synchronize Enterprise Knowledge Graph. `RelationshipResolutionService`
(`TDS-013 §7`, §10–§13, §16). Orchestrates Entity Resolution
(`EntityOwnershipResolver`) for both endpoints, derives/validates
`organization_id` per BR-1–BR-4 (`ADR-023 §5.3`), performs Ontology
Validation (`relationship_type` membership in `RTA-001 §12.9`'s own closed
12-value set), then persists via `EnterpriseKnowledgeGraphRepository` —
one relationship-resolution attempt = one transaction (`TDS-013 §15`).
Idempotent on the natural key (`TDS-013 §17`, check-before-insert — this
design's own explicitly recommended mechanism, not a database `UNIQUE`
constraint, per `TDS-013 §17`'s own stated preference for BA-05's minimum
scope).

Rejections (`TDS-013 §16`) are signaled by raising
`RelationshipRejectedError`, never by returning a silent failure value —
`EventSubscriber.handle_inbound_message`'s own existing dispatch loop
(`Backend/Shared/Events/event_subscriber.py`) already catches any handler
exception and routes it to the existing DLQ mechanism
(`route_to_dead_letter_queue`, phase `HANDLER_CRASH`) — reused verbatim,
no new DLQ mechanism invented (`TDS-013 §8` step 6). Each rejection is
also independently logged here with its own specific reason class
(`TDS-013 §23`), before the exception is raised, so a structured record
exists even though the framework's own generic `HANDLER_CRASH` log does
not itself distinguish rejection reasons.

Audit trail uses `Backend/Shared/Logging`'s real `AuditLogger` directly
(`aurex.backend.shared.logging.audit_logger`), per `TDS-013 §5`/`§23`/
`§24` item 1's own explicit instruction ("BA-05 is a new component with
nothing to migrate away from... should use the real framework from the
outset") — not AIService's local, explicitly-temporary `observability.py`
substitute (`TD-105` Closed; the real framework is importable and
available, independently confirmed, `Gate 1` Finding `N-1` remediation).
Diagnostic (non-audit) logging still uses plain stdlib `logging`, mirroring
the already-certified BA-04 Increment's own precedent
(`services/knowledge_asset_service.py`'s own `_event_logger`) — TDS-013's
own "SHALL use the real framework" instruction is about the audit
vocabulary specifically, not a blanket replacement of every diagnostic
logger in this repository.
"""
from __future__ import annotations

import logging
import sys
import uuid
from enum import Enum
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parents[3]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from aurex.backend.shared.logging.audit_logger import AuditLogger, AuditStatus
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.knowledge_graph_repository import EnterpriseKnowledgeGraphRepository
from services.entity_ownership_resolver import EntityOwnershipResolver

_logger = logging.getLogger("aiservice.knowledge_graph")

# RTA-001 §12.9 — closed 12-value relationship-kind vocabulary. Membership
# check only; no value is added, renamed, or reinterpreted here.
ONTOLOGY_RELATIONSHIP_TYPES = frozenset(
    {
        "Owns",
        "Reports To",
        "Depends On",
        "Supports",
        "References",
        "Controls",
        "Measures",
        "Influences",
        "Linked To",
        "Derived From",
        "Verified By",
        "Governed By",
    }
)


class RejectionReason(str, Enum):
    """`TDS-013 §16`'s own named rejection classes."""

    SOURCE_NOT_FOUND = "SOURCE_NOT_FOUND"
    TARGET_NOT_FOUND = "TARGET_NOT_FOUND"
    CROSS_ORGANIZATION = "CROSS_ORGANIZATION"
    INVALID_RELATIONSHIP_TYPE = "INVALID_RELATIONSHIP_TYPE"


class RelationshipRejectedError(Exception):
    """Raised for every `TDS-013 §16` rejection outcome. Carries the specific reason class."""

    def __init__(self, reason: RejectionReason, detail: str) -> None:
        self.reason = reason
        super().__init__(f"{reason.value}: {detail}")


def derive_organization_id(
    source_organization_id: uuid.UUID | None, target_organization_id: uuid.UUID | None
) -> tuple[bool, uuid.UUID | None]:
    """
    `ADR-023 §5.3` BR-1–BR-4, `TDS-013 §10`–§13. Pure function — no I/O —
    so BR-1–BR-4's own positive/negative cases are independently
    unit-testable without a database. Returns `(accepted, organization_id)`;
    `accepted=False` means BR-1/BR-4 cross-organization rejection.
    """
    if source_organization_id is not None and target_organization_id is not None:
        if source_organization_id != target_organization_id:
            return False, None  # BR-1 mismatch == BR-4 cross-organization reject (TDS-013 §4)
        return True, source_organization_id  # BR-1 match
    if source_organization_id is not None:
        return True, source_organization_id  # BR-2 — target confirmed-Global
    if target_organization_id is not None:
        return True, target_organization_id  # BR-2 — source confirmed-Global
    return True, None  # BR-3 — both confirmed-Global


class RelationshipResolutionService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session
        self.resolver = EntityOwnershipResolver(db_session)
        self.repo = EnterpriseKnowledgeGraphRepository(db_session)

    async def resolve_and_persist(
        self,
        *,
        source_entity_type: str,
        source_entity_id: uuid.UUID,
        relationship_type: str,
        target_entity_type: str,
        target_entity_id: uuid.UUID | None = None,
    ) -> None:
        """
        `target_entity_id=None` is valid ONLY for `target_entity_type ==
        "ORGANIZATION"` — `RO-DEC-WP14-BA05-02`'s own decided target
        derivation (the target IS the source's own resolved
        `organization_id`, never independently looked up, `TDS-013 §9`).
        Raises `RelationshipRejectedError` on any `TDS-013 §16` rejection.
        Returns normally (no write) on an idempotent no-op, or after a
        successful insert.
        """
        # Ontology Validation (TDS-013 §16) — cheapest check, a
        # design-shape rejection unrelated to entity state; checked first.
        if relationship_type not in ONTOLOGY_RELATIONSHIP_TYPES:
            self._reject(
                RejectionReason.INVALID_RELATIONSHIP_TYPE,
                f"relationship_type={relationship_type!r} is not in RTA-001 §12.9's closed vocabulary",
                source_entity_id,
                target_entity_id,
            )

        source = await self.resolver.resolve(source_entity_type, source_entity_id)
        if not source.found:
            self._reject(
                RejectionReason.SOURCE_NOT_FOUND,
                f"{source_entity_type}:{source_entity_id} not found",
                source_entity_id,
                target_entity_id,
            )

        if target_entity_id is None:
            if target_entity_type != "ORGANIZATION":
                # No caller-supplied target_entity_id and no authorized
                # derivation rule for this target_entity_type — an Entity
                # Resolution failure, not a silent default.
                self._reject(
                    RejectionReason.TARGET_NOT_FOUND,
                    f"no target_entity_id supplied and no derivation rule for target_entity_type={target_entity_type!r}",
                    source_entity_id,
                    None,
                )
            # RO-DEC-WP14-BA05-02: derived from the source's own resolved
            # organization_id — never independently looked up.
            target_entity_id = source.organization_id

        target = await self.resolver.resolve(target_entity_type, target_entity_id)
        if not target.found:
            self._reject(
                RejectionReason.TARGET_NOT_FOUND,
                f"{target_entity_type}:{target_entity_id} not found",
                source_entity_id,
                target_entity_id,
            )

        accepted, resolved_organization_id = derive_organization_id(source.organization_id, target.organization_id)
        if not accepted:
            self._reject(
                RejectionReason.CROSS_ORGANIZATION,
                f"source organization_id={source.organization_id} != target organization_id={target.organization_id}",
                source_entity_id,
                target_entity_id,
            )

        existing = await self.repo.find_by_natural_key(
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            relationship_type=relationship_type,
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
        )
        if existing is not None:
            # TDS-013 §16/§17 — idempotent no-op, not an error, not a
            # duplicate row, not re-audited as a fresh SUCCESS.
            _logger.info(
                "Relationship already present (idempotent no-op): %s:%s -[%s]-> %s:%s",
                source_entity_type,
                source_entity_id,
                relationship_type,
                target_entity_type,
                target_entity_id,
            )
            return

        await self.repo.insert(
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            relationship_type=relationship_type,
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
            organization_id=resolved_organization_id,
        )
        AuditLogger.log(
            action="SYNCHRONIZE_KNOWLEDGE_GRAPH_RELATIONSHIP",
            resource=f"enterprise_knowledge_graph:{source_entity_type}:{source_entity_id}-[{relationship_type}]->{target_entity_type}:{target_entity_id}",
            status=AuditStatus.SUCCESS,
            actor_id="SYSTEM",
            tenant_id=str(resolved_organization_id) if resolved_organization_id else None,
        )

    def _reject(
        self,
        reason: RejectionReason,
        detail: str,
        source_entity_id: uuid.UUID | None,
        target_entity_id: uuid.UUID | None,
    ) -> None:
        """Logs a structured rejection record (`TDS-013 §23`) then raises — never returns."""
        AuditLogger.log(
            action="SYNCHRONIZE_KNOWLEDGE_GRAPH_RELATIONSHIP",
            resource=f"enterprise_knowledge_graph:{source_entity_id}->{target_entity_id}",
            status=AuditStatus.DENIED,
            actor_id="SYSTEM",
            tenant_id=None,
            metadata={"reason": reason.value, "detail": detail},
        )
        _logger.warning("Knowledge Graph relationship rejected (%s): %s", reason.value, detail)
        raise RelationshipRejectedError(reason, detail)
