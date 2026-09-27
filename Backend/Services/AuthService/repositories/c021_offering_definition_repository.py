import uuid
from typing import Sequence

from sqlalchemy import Integer, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.c021_offering_definition import (
    OFFERING_REFERENCE_PREFIX,
    C021OfferingDefinition,
)
from repositories.base_repository import BaseRepository

# 1-based character position at which the numeric suffix of `offering_reference`
# begins — the fixed prefix (`OFFERING_REFERENCE_PREFIX`) plus the literal `-`
# separator, e.g. "OFFERING-000001" -> prefix occupies positions 1-8, "-" is
# position 9, the suffix starts at position 10.
_REFERENCE_SUFFIX_OFFSET = len(OFFERING_REFERENCE_PREFIX) + 2

# A defensive upper bound on the catalog list query. BA-01 charters no
# pagination contract (`TDS-C021 §13` names `GET /offerings` with no page
# parameters); this cap simply prevents an unbounded scan. Exposing real
# pagination is an implementation-time follow-up (`TDS-C021 §27`).
_LIST_HARD_CAP = 200


class C021OfferingDefinitionRepository(BaseRepository[C021OfferingDefinition]):
    """
    Repository for `c021_offering_definition` records (C-021, WP-20 BA-01).

    The write path (`establish`) uses the inherited `create()` directly,
    mirroring every prior WP establish repository. The catalog is
    platform-global (`ROD-C021` D8) — no tenant predicate anywhere; every
    `PLATFORM_ADMIN` caller sees the one enterprise-wide catalog, exactly as
    `/roles` exposes the one platform-global role catalog.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(C021OfferingDefinition, session)

    async def list_all(self) -> Sequence[C021OfferingDefinition]:
        """Every Offering Definition, newest first, hard-capped (`TDS-C021 §12`/`§13`)."""
        query = (
            select(C021OfferingDefinition)
            .order_by(C021OfferingDefinition.created_at.desc())
            .limit(_LIST_HARD_CAP)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_offering_reference(
        self, offering_reference: str
    ) -> C021OfferingDefinition | None:
        query = select(C021OfferingDefinition).where(
            C021OfferingDefinition.offering_reference == offering_reference
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def max_reference_sequence(self) -> int:
        """
        The current highest numeric suffix across all assigned
        `offering_reference` values, or 0 if the catalog is empty. Used by
        the service's application-level monotonic allocator (`TDS-C021 §9.3`,
        `[RO DECISION]` O1 — a PostgreSQL SEQUENCE is not mandated). The
        UNIQUE constraint on `offering_reference` is the concurrency backstop;
        a collision on insert triggers an allocate-and-retry in the service.

        Gate 5 remediation (2026-09-09): the prior implementation located the
        '-' at runtime via `func.instr(...)`, a SQLite/MySQL/Oracle function
        with no PostgreSQL equivalent (PostgreSQL has no built-in `instr`;
        the two dialects' own search-function names, `instr` vs.
        `strpos`/`position`, do not overlap at all) — every `establish()`
        call failed against the declared production database, a Critical
        Gate 5 finding undetected by Gates 1/2 because every prior gate ran
        exclusively against the SQLite test harness. No runtime search is
        actually needed:
        `offering_reference` is always system-assigned by this service in the
        fixed `OFFERING_REFERENCE_PREFIX + '-' + NNNNNN` shape, so the suffix
        always starts at the same, compile-time-known character offset
        (`_REFERENCE_SUFFIX_OFFSET`). A fixed-offset `substr(string, start)`
        is standard two-argument `SUBSTR`, supported identically by SQLite
        and PostgreSQL, with no dialect-specific function required.
        """
        suffix = func.substr(
            C021OfferingDefinition.offering_reference,
            _REFERENCE_SUFFIX_OFFSET,
        )
        query = select(func.coalesce(func.max(cast(suffix, Integer)), 0))
        result = await self.session.execute(query)
        return int(result.scalar_one() or 0)
