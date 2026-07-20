from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from models.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Generic Abstract Repository implementing basic CRUD actions securely nested 
    under strict tenant-id partition checks.
    """
    def __init__(self, model_class: Type[ModelType], db_session: AsyncSession):
        self.model_class = model_class
        self.db = db_session

    async def get_by_id(self, item_id: Any, tenant_id: str) -> Optional[ModelType]:
        """
        Fetches an item by ID. Validates tenant ownership.
        """
        query = select(self.model_class).where(
            self.model_class.id == item_id,
            self.model_class.tenant_id == tenant_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_tenant(self, tenant_id: str, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        List all records belonging exclusively to this tenant.
        """
        query = select(self.model_class).where(
            self.model_class.tenant_id == tenant_id
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, item_data: Dict[str, Any], tenant_id: str) -> ModelType:
        """
        Creates an item, explicitly embedding the tenant context.
        """
        item_data["tenant_id"] = tenant_id
        instance = self.model_class(**item_data)
        self.db.add(instance)
        await self.db.flush()  # flushes to populate model ID without committing
        return instance

    async def update(self, item_id: Any, update_data: Dict[str, Any], tenant_id: str) -> Optional[ModelType]:
        """
        Updates an existing item matching tenant scope.
        """
        # Exclude immutable parameters
        update_data.pop("id", None)
        update_data.pop("tenant_id", None)
        
        query = update(self.model_class).where(
            self.model_class.id == item_id,
            self.model_class.tenant_id == tenant_id
        ).values(**update_data).execution_options(synchronize_session="fetch")
        
        await self.db.execute(query)
        await self.db.flush()
        
        return await self.get_by_id(item_id, tenant_id)

    async def delete(self, item_id: Any, tenant_id: str) -> bool:
        """
        Deletes a record matching tenant scope.
        """
        query = delete(self.model_class).where(
            self.model_class.id == item_id,
            self.model_class.tenant_id == tenant_id
        )
        result = await self.db.execute(query)
        await self.db.flush()
        return (result.rowcount or 0) > 0
