from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.bar_registration import BarRegistration
from repositories.base_repository import BaseRepository


class BarRegistrationRepository(BaseRepository[BarRegistration]):
    """
    Repository for the `bar_registration` table (WP-23 Workstream C).

    `get_by_work_package_and_reference` supports the service's own
    friendlier-error pre-check for duplicate registration. It is
    deliberately NOT the sole duplicate-registration protection — the
    `uq_bar_registration_wp_reference` database constraint is the
    authoritative backstop against a race between two concurrent
    registration attempts for the same `(owning_work_package,
    business_activity_reference)` pair; this method exists only to let
    the service distinguish "already registered" from "identifier
    collision" after either kind of `IntegrityError`.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(BarRegistration, session)

    async def get_by_work_package_and_reference(
        self, owning_work_package: str, business_activity_reference: str
    ) -> BarRegistration | None:
        query = select(BarRegistration).where(
            BarRegistration.owning_work_package == owning_work_package,
            BarRegistration.business_activity_reference == business_activity_reference,
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_identifier(self, identifier: str) -> BarRegistration | None:
        query = select(BarRegistration).where(BarRegistration.identifier == identifier)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def count_registered(self) -> int:
        """Total number of registrations ever created — test/verification convenience only."""
        query = select(func.count()).select_from(BarRegistration)
        result = await self.session.execute(query)
        return int(result.scalar_one() or 0)
