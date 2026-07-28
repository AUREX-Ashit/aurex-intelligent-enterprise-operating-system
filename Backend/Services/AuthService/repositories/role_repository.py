import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.membership import Membership
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

    async def has_active_dependents(self, role_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement): a Role
        is Role & Permission Management's only object type with a real,
        AuthService-implemented dependent table today —
        `memberships.role_id` (WP-00-era, real FK). Returns True if any
        Membership currently assigned this Role is itself ACTIVE.

        Unlike the other four WP-02 object types (see their own
        has_active_dependents() docstrings), this check is real, not
        vacuous — Membership has existed in AuthService since WP-00.
        """
        result = await self.session.execute(
            select(Membership.id).where(
                Membership.role_id == role_id,
                Membership.membership_status == "ACTIVE",
            ).limit(1)
        )
        return result.scalars().first() is not None
