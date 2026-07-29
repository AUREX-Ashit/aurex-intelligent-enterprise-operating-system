from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization_establishment_attempt import OrganizationEstablishmentAttempt
from repositories.base_repository import BaseRepository


class OrganizationEstablishmentAttemptRepository(BaseRepository[OrganizationEstablishmentAttempt]):
    """
    Repository for Organization Establishment Attempt records (Organization
    Anchor Context, IRA-001A / C-004). Mirrors OrganizationRepository's own
    get_by_code() shape exactly — same duplicate-check precedent, applied
    to this table's own uq_organization_establishment_attempts_organization_code
    constraint.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(OrganizationEstablishmentAttempt, session)

    async def get_by_code(self, organization_code: str) -> OrganizationEstablishmentAttempt | None:
        result = await self.session.execute(
            select(OrganizationEstablishmentAttempt).where(
                OrganizationEstablishmentAttempt.organization_code == organization_code
            )
        )
        return result.scalars().first()
