from typing import Any, Generic, Sequence, TypeVar
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    SQLAlchemy 2.x generic Repository implementation.
    Decoupled interfaces for unit testing & code separation.
    """
    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, id: UUID) -> ModelType | None:
        """
        Retrieves a record by its database Primary Key.
        """
        return await self.session.get(self.model, id)

    async def get_multi(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """
        Retrieves multiple records with offset pagination.
        """
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, obj_in: dict[str, Any]) -> ModelType:
        """
        Inserts a new record into the database.
        """
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        # Session commit is deferred to Unit of Work or Dependency context
        return db_obj

    async def update(self, id: UUID, obj_in: dict[str, Any]) -> ModelType | None:
        """
        Updates an existing record's fields in place and returns it, or
        None if no record exists for the given id. Session commit is
        deferred to Unit of Work or Dependency context, same as create().
        """
        obj = await self.get_by_id(id)
        if obj is None:
            return None
        for field, value in obj_in.items():
            setattr(obj, field, value)
        return obj

    async def delete(self, id: UUID) -> ModelType | None:
        """
        Removes a record from the database.
        """
        obj = await self.get_by_id(id)
        if obj:
            await self.session.delete(obj)
        return obj
