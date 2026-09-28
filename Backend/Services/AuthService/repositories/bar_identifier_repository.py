from sqlalchemy import Integer, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.bar_identifier_ledger import BAR_IDENTIFIER_PREFIX, BarIdentifierLedger
from repositories.base_repository import BaseRepository

# 1-based character position at which the numeric suffix of `identifier`
# begins — the fixed prefix (`BAR_IDENTIFIER_PREFIX`) plus the literal `-`
# separator, e.g. "BA-000001" -> prefix occupies position 1-2, "-" is
# position 3, the suffix starts at position 4. Mirrors
# `C021OfferingDefinitionRepository._REFERENCE_SUFFIX_OFFSET`'s own
# fixed-offset approach, adopted deliberately after that table's own Gate 5
# finding that a runtime string-search function (`func.instr`) has no
# PostgreSQL equivalent — a fixed, compile-time-known offset needs no
# dialect-specific search function at all.
_IDENTIFIER_SUFFIX_OFFSET = len(BAR_IDENTIFIER_PREFIX) + 2


class BarIdentifierRepository(BaseRepository[BarIdentifierLedger]):
    """
    Repository for the `bar_identifier_ledger` table (WP-23 Workstream B).

    Read-side: `max_identifier_sequence` supports the service's
    application-level monotonic allocator (D5; `[IMPLEMENTATION DESIGN]` —
    no PostgreSQL SEQUENCE, mirroring `[RO DECISION]` O1's own precedent).
    Write-side: the inherited `create()` performs the actual issuance
    insert; the UNIQUE constraint on `identifier` is the concurrency
    backstop, with allocate-and-retry handled in
    `BarIdentifierService.issue_identifier`.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(BarIdentifierLedger, session)

    async def max_identifier_sequence(self) -> int:
        """
        The current highest numeric suffix across every issued
        `identifier`, or 0 if none has ever been issued.
        """
        suffix = func.substr(
            BarIdentifierLedger.identifier,
            _IDENTIFIER_SUFFIX_OFFSET,
        )
        query = select(func.coalesce(func.max(cast(suffix, Integer)), 0))
        result = await self.session.execute(query)
        return int(result.scalar_one() or 0)

    async def is_issued(self, identifier: str) -> bool:
        """
        Whether `identifier` already exists in the ledger. The services use
        it after a failed insert to tell a genuine identifier collision
        (retryable) from any other integrity failure (not retryable).
        """
        query = select(BarIdentifierLedger.id).where(BarIdentifierLedger.identifier == identifier)
        result = await self.session.execute(query)
        return result.first() is not None

    async def count_issued(self) -> int:
        """Total number of identifiers ever issued — test/verification convenience only."""
        query = select(func.count()).select_from(BarIdentifierLedger)
        result = await self.session.execute(query)
        return int(result.scalar_one() or 0)
