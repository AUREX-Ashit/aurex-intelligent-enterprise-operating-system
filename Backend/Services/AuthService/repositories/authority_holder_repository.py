import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.authority_holder import AuthorityHolder, AuthorityHolderStatus
from repositories.base_repository import BaseRepository


class AuthorityHolderRepository(BaseRepository[AuthorityHolder]):
    """
    Repository for C-040 Authority Holder records (TDS-017 §23).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(AuthorityHolder, session)

    async def get_active_by_authority(self, authority_identity: str) -> AuthorityHolder | None:
        """
        Live lookup of the currently active accountability point for a
        given authority (TDS-017 §22's own "live lookup, never a token
        claim" requirement). Returns None if unpopulated (e.g. AI-002,
        TD-157) — never inferred, never simulated.
        """
        result = await self.session.execute(
            select(AuthorityHolder).where(
                AuthorityHolder.authority_identity == authority_identity,
                AuthorityHolder.status == AuthorityHolderStatus.ACTIVE.value,
            )
        )
        return result.scalar_one_or_none()

    async def get_active_by_person(self, person_id: uuid.UUID) -> list[AuthorityHolder]:
        """Every currently-active authority a given Person holds (diagnostic/audit use)."""
        result = await self.session.execute(
            select(AuthorityHolder).where(
                AuthorityHolder.holder_person_id == person_id,
                AuthorityHolder.status == AuthorityHolderStatus.ACTIVE.value,
            )
        )
        return list(result.scalars().all())
