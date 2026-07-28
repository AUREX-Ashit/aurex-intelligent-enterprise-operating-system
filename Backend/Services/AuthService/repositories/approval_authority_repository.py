import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from models.approval_authority import ApprovalAuthority
from repositories.base_repository import BaseRepository


class ApprovalAuthorityRepository(BaseRepository[ApprovalAuthority]):
    """
    Repository for Approval Authority records (C-003, WP-02 BA-03).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ApprovalAuthority, session)

    async def get_active_dependents(self, approval_authority_id: uuid.UUID) -> list[dict]:
        """
        WP-02 BA-09 (ERB-C003-03/EX-C003-09's enumeration requirement):
        Master Technical Architecture's canonical
        `membership_approval_authority` join table is the real dependent
        of an Approval Authority (URA-001), but it is not yet
        implemented anywhere in AuthService (no model, no migration) —
        the same disclosed gap already governing this object type's
        TD-023/TD-028. Always returns an empty list today. Disclosed
        here, not silently omitted: this is a genuine architectural
        completeness gap, not a deliberate design choice, and should be
        revisited once `membership_approval_authority` is implemented.
        """
        return []

    async def has_active_dependents(self, approval_authority_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement). Reuses
        get_active_dependents() (WP-02 BA-09) as its own single source
        of truth, per the instruction not to duplicate dependency logic
        between the two Business Activities.
        """
        return len(await self.get_active_dependents(approval_authority_id)) > 0
