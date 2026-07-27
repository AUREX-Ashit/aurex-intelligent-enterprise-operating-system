from sqlalchemy.ext.asyncio import AsyncSession

from models.delegation_policy import DelegationPolicy
from repositories.base_repository import BaseRepository


class DelegationPolicyRepository(BaseRepository[DelegationPolicy]):
    """
    Repository for Delegation Policy records (C-003, WP-02 BA-04).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DelegationPolicy, session)
