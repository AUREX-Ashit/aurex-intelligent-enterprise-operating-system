from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import UserModel
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[UserModel]):
    """
    User DB repository scaffolding.
    Contains user-specific DB operations with multi-tenant scopes.
    """
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(UserModel, session)

    async def get_by_email(self, email: str, tenant_id: UUID | None = None) -> UserModel | None:
        """
        Query scoped by email and optional Tenant ID.
        Database queries are stubbed and ready to be implemented.
        """
        query = select(UserModel).where(UserModel.email == email)
        if tenant_id:
            query = query.where(UserModel.tenant_id == tenant_id)
            
        result = await self.session.execute(query)
        return result.scalars().first()

    async def verify_user_tenant_membership(self, user_id: UUID, tenant_id: UUID) -> bool:
        """
        Ensures users can only authenticate to authorized tenants.
        """
        query = select(UserModel).where(UserModel.id == user_id, UserModel.tenant_id == tenant_id)
        result = await self.session.execute(query)
        return result.scalars().first() is not None
