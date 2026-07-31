import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.access_evaluation_outcome import AccessEvaluationOutcome
from models.approval_authority import ApprovalAuthority
from repositories.base_repository import BaseRepository


class AccessEvaluationOutcomeRepository(BaseRepository[AccessEvaluationOutcome]):
    """Repository for Access Evaluation Outcome records (AEO-000001, WP-05 / C-002)."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(AccessEvaluationOutcome, session)

    async def get_active_domain_approval_authority(
        self, domain_id: uuid.UUID, organization_id: uuid.UUID
    ) -> ApprovalAuthority | None:
        """
        BA-01's own Deferred-branch lookup (EX-C002-04): the currently-ACTIVE,
        DOMAIN-scoped Approval Authority governing the requested Domain
        *within the requesting Membership's own Organization*, if any.
        Reuses ApprovalAuthority (WP-02) verbatim -- never reimplemented.

        `organization_id` is required, not optional: Domain is platform-
        shared reference data (`Domain.organization_id` is nullable), but
        ApprovalAuthority.organization_id is required for every scope
        (`models/approval_authority.py`) -- distinct organizations may each
        establish their own ACTIVE, DOMAIN-scoped Approval Authority
        against the same shared Domain. Without this filter, a Membership
        in one Organization could be deferred to another Organization's
        Approval Authority, disclosing that authority's name into a
        persisted, API-returned record (VV-AUDIT-WP-05 F-02). `order_by`
        makes selection deterministic where more than one ACTIVE authority
        exists within the same organization/domain (VV-AUDIT-WP-05 F-02
        item 3 -- `.first()` alone has no defined order).
        """
        result = await self.session.execute(
            select(ApprovalAuthority)
            .where(
                ApprovalAuthority.domain_id == domain_id,
                ApprovalAuthority.organization_id == organization_id,
                ApprovalAuthority.scope_type == "DOMAIN",
                ApprovalAuthority.status == "ACTIVE",
            )
            .order_by(ApprovalAuthority.created_at, ApprovalAuthority.id)
        )
        return result.scalars().first()
