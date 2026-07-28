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

    async def has_active_dependents(self, approval_authority_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement): Master
        Technical Architecture's canonical `membership_approval_authority`
        join table is the real dependent of an Approval Authority
        (URA-001), but it is not yet implemented anywhere in AuthService
        (no model, no migration) — the same disclosed gap already
        governing this object type's TD-023 authorization simplification.
        Always returns False today. Disclosed here, not silently omitted:
        this is a genuine architectural completeness gap, not a
        deliberate design choice, and should be revisited once
        `membership_approval_authority` is implemented.
        """
        return False
