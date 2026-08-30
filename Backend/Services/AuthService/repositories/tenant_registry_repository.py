from sqlalchemy.ext.asyncio import AsyncSession

from models.tenant_registry import TenantRegistry
from repositories.base_repository import BaseRepository


class TenantRegistryRepository(BaseRepository[TenantRegistry]):
    """
    Repository for `tenant_registry` records (TDS-016 §5, C-040 Tenant
    Establishment). No lookup beyond BaseRepository.get_by_id is required
    by the chartered minimum-scope Establishment transaction (TDS-016 §8);
    later lifecycle Business Activities (migration/offboarding, out of
    scope here) would add their own query methods when chartered.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(TenantRegistry, session)
