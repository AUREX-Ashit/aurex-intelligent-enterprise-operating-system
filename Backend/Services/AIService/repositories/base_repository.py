# repositories/base_repository.py
from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model_class: Type[ModelType], db_session: AsyncSession):
        self.model_class = model_class
        self.db = db_session

    async def get_by_id(self, tenant_id: str, record_id: Any) -> Optional[ModelType]:
        """Fetch matching model instance filtered strictly by both record ID and Tenant ID."""
        query = select(self.model_class).where(
            self.model_class.id == record_id,
            self.model_class.tenant_id == tenant_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_by_tenant(self, tenant_id: str, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Fetch all records matching specific Tenant ID only. Prevents leakages across silos."""
        query = select(self.model_class).where(
            self.model_class.tenant_id == tenant_id
        ).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, tenant_id: str, data: dict) -> ModelType:
        """Create new model instance tagged with matching Tenant ID."""
        instance = self.model_class(**data)
        instance.tenant_id = tenant_id
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update(self, tenant_id: str, record_id: Any, data: dict) -> Optional[ModelType]:
        """Update fields for selected entity under current tenancy block."""
        instance = await self.get_by_id(tenant_id, record_id)
        if not instance:
            return None
        
        for key, val in data.items():
            if hasattr(instance, key):
                setattr(instance, key, val)
                
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def delete_by_id(self, tenant_id: str, record_id: Any) -> bool:
        """Isolated deletion."""
        instance = await self.get_by_id(tenant_id, record_id)
        if not instance:
            return False
            
        await self.db.delete(instance)
        await self.db.commit()
        return True
