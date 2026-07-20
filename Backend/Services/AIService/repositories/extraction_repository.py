# repositories/extraction_repository import ESGExtractionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from models.extraction import ESGExtractionModel
from repositories.base_repository import BaseRepository

class ESGExtractionRepository(BaseRepository[ESGExtractionModel]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ESGExtractionModel, db_session)
