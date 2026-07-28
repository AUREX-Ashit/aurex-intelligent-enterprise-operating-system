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

    async def has_active_dependents(self, delegation_policy_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement): Master
        Technical Architecture's canonical `delegation_registry` is the
        real dependent of a Delegation Policy (its own
        `delegation_policy_id` FK, added at BA-04), but `delegation_registry`
        itself is not yet implemented anywhere in AuthService (no model,
        no migration) — the same disclosed gap BA-04's own module
        docstring already names. Always returns False today. Disclosed
        here, not silently omitted: this is a genuine architectural
        completeness gap, not a deliberate design choice, and should be
        revisited once `delegation_registry` is implemented.
        """
        return False
