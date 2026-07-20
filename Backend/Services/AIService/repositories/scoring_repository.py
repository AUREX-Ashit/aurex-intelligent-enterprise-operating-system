# repositories/scoring_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from models.scoring import ESGScoringModel
from repositories.base_repository import BaseRepository

class ESGScoringRepository(BaseRepository[ESGScoringModel]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ESGScoringModel, db_session)
