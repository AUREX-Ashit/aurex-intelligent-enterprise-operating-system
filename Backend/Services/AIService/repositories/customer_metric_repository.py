# repositories/customer_metric_repository.py
"""
WP-14 BA-03 — Resolve Enterprise Intelligence Candidate (Convergence
Decision). Writes are strictly tenant-scoped — `organization_id` is
always the caller's own JWT-derived claim, never a caller-supplied
identifier, per `CLAUDE.md §21.4`(c).
"""
from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.customer_metric import CustomerMetricRegistryModel


class CustomerMetricRegistryRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def find_same_org_by_exact_name(
        self, organization_id: uuid.UUID, metric_name: str
    ) -> CustomerMetricRegistryModel | None:
        """
        Semantic Matching placeholder (disclosed, not a real Reasoning
        Engine invocation — see `services/unclassified_intelligence_service.py`).
        Case-insensitive exact-name match against the caller's own
        existing, active Tenant CDEs only — the only real, populated data
        source available (`metric_registry`, the Global canonical library
        Binding 3 actually describes matching against, has zero physical
        rows anywhere in this repository).
        """
        query = select(CustomerMetricRegistryModel).where(
            CustomerMetricRegistryModel.organization_id == organization_id,
            CustomerMetricRegistryModel.active_flag.is_(True),
            func.lower(CustomerMetricRegistryModel.metric_name) == metric_name.lower(),
        )
        return (await self.db.execute(query)).scalars().first()

    async def create(
        self,
        *,
        organization_id: uuid.UUID,
        requested_by_user_id: uuid.UUID,
        metric_name: str,
        metric_code: str,
        metric_description: str | None,
        unit_of_measure: str | None,
        formula_logic: str | None,
        semantic_match_attempted_flag: bool,
        semantic_match_result_metric_id: uuid.UUID | None,
        semantic_match_score: Decimal | None,
        semantic_match_rejected_reason: str | None,
    ) -> CustomerMetricRegistryModel:
        instance = CustomerMetricRegistryModel(
            organization_id=organization_id,
            requested_by_user_id=requested_by_user_id,
            metric_name=metric_name,
            metric_code=metric_code,
            metric_description=metric_description,
            unit_of_measure=unit_of_measure,
            formula_logic=formula_logic,
            semantic_match_attempted_flag=semantic_match_attempted_flag,
            semantic_match_result_metric_id=semantic_match_result_metric_id,
            semantic_match_score=semantic_match_score,
            semantic_match_rejected_reason=semantic_match_rejected_reason,
        )
        self.db.add(instance)
        await self.db.flush()
        return instance
