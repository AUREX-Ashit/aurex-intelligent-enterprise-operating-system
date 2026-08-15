# repositories/unclassified_intelligence_repository.py
"""
WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090). Writes
are strictly tenant-scoped — `organization_id` is always the caller's own
JWT-derived claim, never a caller-supplied identifier, per
`CLAUDE.md §21.4`(c).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.unclassified_intelligence import UnclassifiedIntelligenceRegistryModel


class UnclassifiedIntelligenceRegistryRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(
        self,
        *,
        organization_id: uuid.UUID,
        raw_extracted_value: str,
        source_document_reference: str,
        source_page_section: str | None,
        extraction_method: str,
    ) -> UnclassifiedIntelligenceRegistryModel:
        instance = UnclassifiedIntelligenceRegistryModel(
            organization_id=organization_id,
            raw_extracted_value=raw_extracted_value,
            source_document_reference=source_document_reference,
            source_page_section=source_page_section,
            extraction_method=extraction_method,
        )
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def get_by_id(
        self, organization_id: uuid.UUID, unclassified_id: uuid.UUID
    ) -> UnclassifiedIntelligenceRegistryModel | None:
        """
        WP-14 BA-03 — Resolve Enterprise Intelligence Candidate. Additive
        method (the `create()` above, BA-02's own, is untouched). Scoped
        strictly to the caller's own Organization — never an unscoped
        lookup by a caller-supplied identifier, per `CLAUDE.md §21.4`(c).
        """
        query = select(UnclassifiedIntelligenceRegistryModel).where(
            UnclassifiedIntelligenceRegistryModel.organization_id == organization_id,
            UnclassifiedIntelligenceRegistryModel.unclassified_id == unclassified_id,
        )
        return (await self.db.execute(query)).scalar_one_or_none()

    async def claim_for_resolution(
        self,
        organization_id: uuid.UUID,
        unclassified_id: uuid.UUID,
        *,
        resolution_status: str,
        resolved_by_user_id: uuid.UUID,
    ) -> bool:
        """
        WP-14 BA-03 — Gate 1 remediation, Finding 1 (concurrent
        double-resolution race). Atomically transitions a `PENDING`
        candidate to `resolution_status`, guarded by a `WHERE
        resolution_status = 'PENDING'` clause the database re-evaluates
        at the moment this `UPDATE` actually executes — not at the
        caller's own prior `get_by_id` read. An `UPDATE` statement
        inherently takes a write lock on the row(s) it matches, held for
        the remaining lifetime of the current transaction (i.e. until
        the caller's own final `commit()` — no explicit `SELECT ... FOR
        UPDATE` or dialect-specific locking syntax is required, and none
        is used, per the remediation's own "minimal, focused fix"
        constraint). A second, genuinely concurrent call against the
        same row therefore blocks on that same lock until the first
        transaction commits or rolls back, then re-evaluates its own
        `WHERE` clause against the now-current row and finds zero
        matches (since `resolution_status` is no longer `'PENDING'`) —
        `rowcount` is `0`, and this method returns `False`.

        Returns `True` only to the exactly-one caller that won the
        claim. **The caller MUST create no side-effecting rows
        (`customer_metric_registry`, `evidence_registry`) before this
        returns `True`** — this ordering is what prevents a losing
        concurrent request from ever creating an orphaned CDE/Evidence
        pair, the defect the Gate 1 independent certification's own
        from-scratch concurrency probe found.

        This fixes BA-03's own instance of a check-then-act race; the
        identical unguarded pattern exists in other, unrelated services
        across this repository (`TD-147`) — deliberately not touched
        here, per the remediation's own explicit "keep this remediation
        focused on BA-03" instruction.
        """
        result = await self.db.execute(
            update(UnclassifiedIntelligenceRegistryModel)
            .where(
                UnclassifiedIntelligenceRegistryModel.organization_id == organization_id,
                UnclassifiedIntelligenceRegistryModel.unclassified_id == unclassified_id,
                UnclassifiedIntelligenceRegistryModel.resolution_status == "PENDING",
            )
            .values(
                resolution_status=resolution_status,
                resolved_by_user_id=resolved_by_user_id,
                resolved_at=datetime.now(timezone.utc),
            )
        )
        await self.db.flush()
        return result.rowcount == 1

    async def attach_resolution_target(
        self,
        instance: UnclassifiedIntelligenceRegistryModel,
        *,
        resolved_metric_id: uuid.UUID | None,
        resolved_customer_metric_id: uuid.UUID | None,
    ) -> None:
        """
        WP-14 BA-03. Called only after `claim_for_resolution` has
        returned `True` for this exact candidate — no concurrent caller
        can still be racing for it at this point (the claim already
        transitioned it out of `PENDING`), so this plain attribute
        assignment is safe without its own additional guard. Flush-only
        (no commit) — mirrors `ContentRegistrationService`'s own
        established multi-step, single-transaction pattern (WP-11
        BA-03): the calling service owns the final `commit()`.
        """
        instance.resolved_metric_id = resolved_metric_id
        instance.resolved_customer_metric_id = resolved_customer_metric_id
        await self.db.flush()
