from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.role import Role
from repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """
    Repository for Role records (C-003, WP-02).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Role, session)

    async def get_by_code(self, role_code: str) -> Role | None:
        """
        Looks up a Role by its unique role_code — the natural key used
        for Establish Role's pre-flight duplicate check, mirroring
        OrganizationRepository.get_by_code()'s exact pattern.
        """
        result = await self.session.execute(
            select(Role).where(Role.role_code == role_code)
        )
        return result.scalars().first()
