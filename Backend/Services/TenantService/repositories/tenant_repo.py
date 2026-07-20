from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from models.tenant import Tenant, TenantConfig, TenantUser
from repositories.base import BaseRepository


class TenantRepository(BaseRepository[Tenant]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Tenant, db_session)

    async def get_by_name(self, name: str) -> Optional[Tenant]:
        """
        Loads a single tenant by unique name.
        """
        # Scaffolding: SQL query stub
        return None

    async def get_by_domain(self, domain: str) -> Optional[Tenant]:
        """
        Loads a single tenant by unique domain.
        """
        # Scaffolding: SQL query stub
        return None


class TenantConfigRepository(BaseRepository[TenantConfig]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(TenantConfig, db_session)

    async def get_by_tenant_id(self, tenant_id: UUID) -> Optional[TenantConfig]:
        """
        Get config for a tenant.
        """
        # Scaffolding
        return None


class TenantUserRepository(BaseRepository[TenantUser]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(TenantUser, db_session)

    async def get_by_email(self, email: str) -> Optional[TenantUser]:
        """
        Retrieve a user across tenants by work email.
        """
        # Scaffolding
        return None

    async def get_users_by_tenant(self, tenant_id: UUID) -> List[TenantUser]:
        """
        List all users registered inside a single tenant partition.
        """
        # Scaffolding: Simulated response for dashboard matching
        return []
