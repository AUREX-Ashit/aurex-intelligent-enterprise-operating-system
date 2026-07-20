from typing import Generic, TypeVar, Type, List, Optional, Any, Sequence
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from middleware.tenant import get_current_tenant
import structlog

logger = structlog.get_logger()

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.model = model
        self.db = db_session

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        """Fetches an entity by ID, strictly scoped to the current tenant"""
        tenant_id = get_current_tenant()
        
        # We assume RLS / Tenant filtering on all queries
        query = select(self.model).filter_by(id=id)
        if hasattr(self.model, "tenant_id"):
            query = query.filter_by(tenant_id=tenant_id)
            
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """Fetches all entities scoped to the current tenant"""
        tenant_id = get_current_tenant()
        
        query = select(self.model)
        if hasattr(self.model, "tenant_id"):
            query = query.filter_by(tenant_id=tenant_id)
            
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, obj_in: Dict[str, Any] if (Dict := globals().get("Dict")) else dict, created_by: Optional[str] = None) -> ModelType:
        """Instantiates an entity with active tenant bindings"""
        tenant_id = get_current_tenant()
        
        db_obj = self.model(**obj_in)
        if hasattr(db_obj, "tenant_id"):
            db_obj.tenant_id = tenant_id
        if hasattr(db_obj, "created_by") and created_by:
            db_obj.created_by = created_by
            db_obj.updated_by = created_by

        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: dict, updated_by: Optional[str] = None) -> ModelType:
        """Updates attributes bound to current tenant"""
        for field in obj_in:
            if hasattr(db_obj, field):
                setattr(db_obj, field, obj_in[field])
                
        if hasattr(db_obj, "updated_by") and updated_by:
            db_obj.updated_by = updated_by
            
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: Any) -> bool:
        """Deletes entity strictly scoped to current tenant"""
        tenant_id = get_current_tenant()
        obj = await self.get_by_id(id)
        if not obj:
            return False
            
        await self.db.delete(obj)
        await self.db.flush()
        return True
