from sqlalchemy.ext.asyncio import AsyncSession

from models.person_correction import PersonCorrection
from repositories.base_repository import BaseRepository


class PersonCorrectionRepository(BaseRepository[PersonCorrection]):
    """Repository for Person Correction records (WP-07 BA-07)."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(PersonCorrection, session)
