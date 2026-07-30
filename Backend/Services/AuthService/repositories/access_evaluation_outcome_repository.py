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
        self, domain_id: uuid.UUID
    ) -> ApprovalAuthority | None:
        """
        BA-01's own Deferred-branch lookup (EX-C002-04): the first
        currently-ACTIVE, DOMAIN-scoped Approval Authority governing the
        requested Domain, if any. Reuses ApprovalAuthority (WP-02) verbatim
        -- never reimplemented.
        """
        result = await self.session.execute(
            select(ApprovalAuthority).where(
                ApprovalAuthority.domain_id == domain_id,
                ApprovalAuthority.scope_type == "DOMAIN",
                ApprovalAuthority.status == "ACTIVE",
            )
        )
        return result.scalars().first()
