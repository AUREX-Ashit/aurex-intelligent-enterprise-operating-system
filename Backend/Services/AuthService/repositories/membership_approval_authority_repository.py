import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.membership_approval_authority import MembershipApprovalAuthority
from repositories.base_repository import BaseRepository


class MembershipApprovalAuthorityRepository(BaseRepository[MembershipApprovalAuthority]):
    """
    Repository for Membership <-> Approval Authority bindings (WP-18,
    C-003, TDS-018).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MembershipApprovalAuthority, session)

    async def get_open_binding(
        self, membership_id: uuid.UUID, approval_authority_id: uuid.UUID
    ) -> MembershipApprovalAuthority | None:
        """
        The currently-open (`effective_to IS NULL`) binding for this exact
        pair, if any — used by the bind-time uniqueness guard
        (`MembershipApprovalAuthorityService.bind()`, TDS-018 §19) and by
        `close()` to locate the row to deactivate.
        """
        query = select(MembershipApprovalAuthority).where(
            MembershipApprovalAuthority.membership_id == membership_id,
            MembershipApprovalAuthority.approval_authority_id == approval_authority_id,
            MembershipApprovalAuthority.effective_to.is_(None),
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_effective_binding(
        self,
        membership_id: uuid.UUID,
        approval_authority_id: uuid.UUID,
        as_of: datetime | None = None,
    ) -> MembershipApprovalAuthority | None:
        """
        TDS-018 §29.2 step 5 (Eligible actor / missing binding): a
        currently-effective row for this exact (membership, authority)
        pair — `effective_from <= as_of` and (`effective_to IS NULL` OR
        `effective_to > as_of`). Returns the most recently-started match
        if more than one somehow qualifies (defensive; the bind-time
        uniqueness guard, §19, is expected to prevent this in practice).
        """
        moment = as_of or datetime.now(timezone.utc)
        query = (
            select(MembershipApprovalAuthority)
            .where(
                MembershipApprovalAuthority.membership_id == membership_id,
                MembershipApprovalAuthority.approval_authority_id == approval_authority_id,
                MembershipApprovalAuthority.effective_from <= moment,
                (MembershipApprovalAuthority.effective_to.is_(None))
                | (MembershipApprovalAuthority.effective_to > moment),
            )
            .order_by(MembershipApprovalAuthority.effective_from.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().first()
