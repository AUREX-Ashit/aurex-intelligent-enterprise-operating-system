from sqlalchemy.ext.asyncio import AsyncSession

from models.approval_authority import ApprovalAuthority
from repositories.base_repository import BaseRepository


class ApprovalAuthorityRepository(BaseRepository[ApprovalAuthority]):
    """
    Repository for Approval Authority records (C-003, WP-02 BA-03).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ApprovalAuthority, session)
