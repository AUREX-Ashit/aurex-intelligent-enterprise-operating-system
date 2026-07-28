import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from models.delegation_policy import DelegationPolicy
from repositories.base_repository import BaseRepository


class DelegationPolicyRepository(BaseRepository[DelegationPolicy]):
    """
    Repository for Delegation Policy records (C-003, WP-02 BA-04).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DelegationPolicy, session)

    async def get_active_dependents(self, delegation_policy_id: uuid.UUID) -> list[dict]:
        """
        WP-02 BA-09 (ERB-C003-03/EX-C003-09's enumeration requirement):
        Master Technical Architecture's canonical `delegation_registry`
        is the real dependent of a Delegation Policy (its own
        `delegation_policy_id` FK, added at BA-04), but
        `delegation_registry` itself is not yet implemented anywhere in
        AuthService (no model, no migration) — the same disclosed gap
        BA-04's own module docstring already names, and TD-028 already
        tracks. Always returns an empty list today. Disclosed here, not
        silently omitted.
        """
        return []

    async def has_active_dependents(self, delegation_policy_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement). Reuses
        get_active_dependents() (WP-02 BA-09) as its own single source
        of truth, per the instruction not to duplicate dependency logic
        between the two Business Activities.
        """
        return len(await self.get_active_dependents(delegation_policy_id)) > 0
