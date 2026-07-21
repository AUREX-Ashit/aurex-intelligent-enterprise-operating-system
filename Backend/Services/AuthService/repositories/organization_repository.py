from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from repositories.base_repository import BaseRepository


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
