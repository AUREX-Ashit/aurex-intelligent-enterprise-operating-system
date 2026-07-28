from sqlalchemy.ext.asyncio import AsyncSession

from models.runtime_assignment_policy import RuntimeAssignmentPolicy
from repositories.base_repository import BaseRepository


class RuntimeAssignmentPolicyRepository(BaseRepository[RuntimeAssignmentPolicy]):
    """
    Repository for Runtime Assignment Policy records (C-003, WP-02 BA-05).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RuntimeAssignmentPolicy, session)
