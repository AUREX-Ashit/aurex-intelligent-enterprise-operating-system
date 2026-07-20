# repositories/validation_repository.py
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.validation import ESGValidationModel
from repositories.base_repository import BaseRepository

class ESGValidationRepository(BaseRepository[ESGValidationModel]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ESGValidationModel, db_session)

    async def get_by_extraction_id(self, tenant_id: str, extraction_id: int) -> Optional[ESGValidationModel]:
        """Fetch validation metrics matching specific extraction model."""
        query = select(self.model_class).where(
            self.model_class.extraction_id == extraction_id,
            self.model_class.tenant_id == tenant_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
