from typing import List, Optional
import uuid
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from models.document import Document

class DocumentRepository(BaseRepository[Document]):
    """
    Service specific repository executing Domain Query Operations over ESG Ingestion documents.
    """
    def __init__(self, db_session: AsyncSession):
        super().__init__(Document, db_session)

    async def get_by_status(self, tenant_id: str, status: str) -> List[Document]:
        """
        Retrieves list of documents for a specific tenant in a given state.
        """
        query = select(Document).where(
            Document.tenant_id == tenant_id,
            Document.status == status
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_ocr_task_id(self, ocr_task_id: str) -> Optional[Document]:
        """
        Retrieves document matching background task reference across tenants (internal system query).
        """
        query = select(Document).where(Document.ocr_task_id == ocr_task_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_ocr_status(self, doc_id: uuid.UUID, tenant_id: str, status: str, ocr_task_id: Optional[str] = None) -> Optional[Document]:
        """
        Standardizes transitions of OCR status tags securely.
        """
        updater = {"status": status}
        if ocr_task_id:
            updater["ocr_task_id"] = ocr_task_id
            
        return await self.update(doc_id, updater, tenant_id)
