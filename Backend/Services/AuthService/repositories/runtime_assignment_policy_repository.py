import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from models.runtime_assignment_policy import RuntimeAssignmentPolicy
from repositories.base_repository import BaseRepository


class RuntimeAssignmentPolicyRepository(BaseRepository[RuntimeAssignmentPolicy]):
    """
    Repository for Runtime Assignment Policy records (C-003, WP-02 BA-05).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RuntimeAssignmentPolicy, session)

    async def get_active_dependents(self, runtime_assignment_policy_id: uuid.UUID) -> list[dict]:
        """
        WP-02 BA-09 (ERB-C003-03/EX-C003-09's enumeration requirement):
        Master Technical Architecture's canonical
        `runtime_assignment_registry` is the real dependent of a Runtime
        Assignment Policy (its own `runtime_assignment_policy_id` FK,
        added at BA-05), but `runtime_assignment_registry` itself is not
        yet implemented anywhere in AuthService (no model, no migration)
        — the same disclosed gap BA-05's own module docstring already
        names, and TD-028 already tracks. Always returns an empty list
        today. Disclosed here, not silently omitted.
        """
        return []

    async def has_active_dependents(self, runtime_assignment_policy_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement). Reuses
        get_active_dependents() (WP-02 BA-09) as its own single source
        of truth, per the instruction not to duplicate dependency logic
        between the two Business Activities.
        """
        return len(await self.get_active_dependents(runtime_assignment_policy_id)) > 0
