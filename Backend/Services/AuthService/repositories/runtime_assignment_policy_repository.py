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

    async def has_active_dependents(self, runtime_assignment_policy_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement): Master
        Technical Architecture's canonical `runtime_assignment_registry`
        is the real dependent of a Runtime Assignment Policy (its own
        `runtime_assignment_policy_id` FK, added at BA-05), but
        `runtime_assignment_registry` itself is not yet implemented
        anywhere in AuthService (no model, no migration) — the same
        disclosed gap BA-05's own module docstring already names. Always
        returns False today. Disclosed here, not silently omitted: this
        is a genuine architectural completeness gap, not a deliberate
        design choice, and should be revisited once
        `runtime_assignment_registry` is implemented.
        """
        return False
