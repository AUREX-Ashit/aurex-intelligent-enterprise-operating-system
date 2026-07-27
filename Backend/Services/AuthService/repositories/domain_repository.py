from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.domain import Domain
from repositories.base_repository import BaseRepository


class DomainRepository(BaseRepository[Domain]):
    """
    Repository for Domain reference-data records (AMD-014). Read-only
    lookup support for WP-02 BA-02 — no create/update path is exposed
    here; Domain rows are platform-seeded (MDP-001 §B2a), and tenant-added
    domains (URA-001-43) are a future, separately-scoped configuration
    capability, not part of this lookup surface.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Domain, session)

    async def list_visible(self, organization_id: UUID | None) -> Sequence[Domain]:
        """
        Every platform-default domain (organization_id IS NULL), plus the
        given tenant's own added domains, if any — mirrors
        business_role_registry's NULL-is-global visibility rule
        (URA-001-43). With no organization_id supplied, only the
        platform-default catalog is returned.
        """
        stmt = select(Domain)
        if organization_id is not None:
            stmt = stmt.where(
                (Domain.organization_id.is_(None)) | (Domain.organization_id == organization_id)
            )
        else:
            stmt = stmt.where(Domain.organization_id.is_(None))
        stmt = stmt.order_by(Domain.domain_name.asc())

        result = await self.session.execute(stmt)
        return result.scalars().all()
