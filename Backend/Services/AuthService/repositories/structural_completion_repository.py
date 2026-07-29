from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.structural_completion import StructuralCompletion
from repositories.base_repository import BaseRepository


class StructuralCompletionRepository(BaseRepository[StructuralCompletion]):
    """
    Repository for Resulting Structural Context records (RSC-000001 —
    see models/structural_completion.py).

    WP-04 BA-08 needs BaseRepository's inherited create() plus one new
    method, get_by_structural_validation_id(), to enforce the guarded
    (non-idempotent) completion decision — the same purpose-built query
    pattern StructuralProposalRepository.get_current_revision() already
    established.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(StructuralCompletion, session)

    async def get_by_structural_validation_id(
        self, structural_validation_id: UUID
    ) -> StructuralCompletion | None:
        """Returns the existing completion for a given validation, if one already exists."""
        result = await self.session.execute(
            select(StructuralCompletion).where(
                StructuralCompletion.structural_validation_id == structural_validation_id
            )
        )
        return result.scalars().first()
