from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from repositories.base_repository import BaseRepository

# Whitelisted sort columns (BA-03) — never resolve sort_by via getattr() on
# unchecked input; only these three columns are exposed for ordering.
_SORTABLE_COLUMNS = {
    "organization_name": Organization.organization_name,
    "organization_code": Organization.organization_code,
    "created_at": Organization.created_at,
}


class OrganizationRepository(BaseRepository[Organization]):
    """
    Repository for Organization records (C-004, WP-01).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Organization, session)

    async def get_by_code(self, organization_code: str) -> Organization | None:
        """
        Looks up an Organization by its unique organization_code — the
        natural key used for Establish Organization's pre-flight
        duplicate check (mirroring EstablishPersonContextService's
        recognize-before-create pattern, applied here against a real
        DB-enforced unique constraint rather than an unconstrained field).
        """
        result = await self.session.execute(
            select(Organization).where(Organization.organization_code == organization_code)
        )
        return result.scalars().first()

    async def search(
        self,
        query: str | None,
        status: str | None,
        skip: int,
        limit: int,
        sort_by: str,
        sort_order: str,
    ) -> tuple[Sequence[Organization], int]:
        """
        BA-03: Search & List Organizations. Returns (page of results, total
        matching count) so the caller can render pagination without a
        second round trip.

        `query` matches organization_name OR organization_code,
        case-insensitively, substring — .ilike() compiles to a
        case-insensitive LIKE on every backend this codebase runs against
        (Postgres in prod/CI, SQLite in tests), not just Postgres's native
        ILIKE.
        """
        stmt = select(Organization)
        count_stmt = select(func.count()).select_from(Organization)

        if query:
            pattern = f"%{query}%"
            condition = Organization.organization_name.ilike(pattern) | Organization.organization_code.ilike(pattern)
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        if status:
            stmt = stmt.where(Organization.status == status)
            count_stmt = count_stmt.where(Organization.status == status)

        sort_column = _SORTABLE_COLUMNS.get(sort_by, Organization.organization_name)
        stmt = stmt.order_by(sort_column.desc() if sort_order == "desc" else sort_column.asc())
        stmt = stmt.offset(skip).limit(limit)

        rows = await self.session.execute(stmt)
        total = await self.session.execute(count_stmt)
        return rows.scalars().all(), total.scalar_one()
