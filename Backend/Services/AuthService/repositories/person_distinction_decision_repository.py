from sqlalchemy.ext.asyncio import AsyncSession

from models.person_distinction_decision import PersonDistinctionDecision
from repositories.base_repository import BaseRepository


class PersonDistinctionDecisionRepository(BaseRepository[PersonDistinctionDecision]):
    """Repository for Person Distinction Decision records (WP-07 BA-04)."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(PersonDistinctionDecision, session)
