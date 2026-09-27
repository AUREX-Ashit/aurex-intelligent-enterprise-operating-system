from sqlalchemy import Integer, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.c022_commercial_account import (
    ACCOUNT_REFERENCE_PREFIX,
    C022CommercialAccount,
)
from repositories.base_repository import BaseRepository

# 1-based character position at which the numeric suffix of `account_reference`
# begins — the fixed prefix (`ACCOUNT_REFERENCE_PREFIX`) plus the literal `-`
# separator, e.g. "ACCOUNT-000001" -> prefix occupies positions 1-7, "-" is
# position 8, the suffix starts at position 9. Mirrors
# `c021_offering_definition_repository._REFERENCE_SUFFIX_OFFSET`'s own
# fixed-offset design (Gate 5 remediation, WP-20) — a fixed-offset `substr`
# is portable across SQLite and PostgreSQL, unlike a runtime `instr()` scan.
_REFERENCE_SUFFIX_OFFSET = len(ACCOUNT_REFERENCE_PREFIX) + 2


class C022CommercialAccountRepository(BaseRepository[C022CommercialAccount]):
    """
    Repository for `c022_commercial_account` records (C-022, WP-21 BA-01).

    The write path (`establish`) uses the inherited `create()` directly,
    mirroring `C021OfferingDefinitionRepository`. The catalog is
    platform-global (`ROD-C022` D2) — no tenant predicate anywhere.

    `get_by_account_reference` is provided per `TDS-C022 §14`'s own minimum
    repository method list, even though BA-01 exposes no read/list endpoint
    (`ROD-C022-A` D8) — it exists for internal use and future-increment
    readiness, not to imply a retrieval route exists.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(C022CommercialAccount, session)

    async def get_by_account_reference(
        self, account_reference: str
    ) -> C022CommercialAccount | None:
        query = select(C022CommercialAccount).where(
            C022CommercialAccount.account_reference == account_reference
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def max_reference_sequence(self) -> int:
        """
        The current highest numeric suffix across all assigned
        `account_reference` values, or 0 if the table is empty. Used by the
        service's application-level monotonic allocator
        (`CommercialAccountService._next_account_reference`) — mirrors
        `C021OfferingDefinitionRepository.max_reference_sequence` exactly,
        including its Gate 5 PostgreSQL-portability remediation (a
        fixed-offset `substr`, never a dialect-specific `instr()`/`strpos()`
        search). The UNIQUE constraint on `account_reference` is the
        concurrency backstop; a collision on insert triggers an
        allocate-and-retry in the service.
        """
        suffix = func.substr(
            C022CommercialAccount.account_reference,
            _REFERENCE_SUFFIX_OFFSET,
        )
        query = select(func.coalesce(func.max(cast(suffix, Integer)), 0))
        result = await self.session.execute(query)
        return int(result.scalar_one() or 0)
