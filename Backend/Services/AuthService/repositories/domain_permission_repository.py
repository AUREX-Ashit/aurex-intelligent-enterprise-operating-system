import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.domain_permission import DomainPermission
from repositories.base_repository import BaseRepository


class DomainPermissionRepository(BaseRepository[DomainPermission]):
    """
    Repository for Domain Permission records (C-003, WP-02 BA-02).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DomainPermission, session)

    async def get_active_grant(
        self, membership_id, domain_id, permission_level: str
    ) -> DomainPermission | None:
        """
        Looks up a currently-active (effective_to IS NULL) grant of the
        exact same (membership, domain, permission_level) triple — the
        structural duplicate-prevention check for Establish Domain
        Permission's pre-flight validation, mirroring
        OrganizationRepository.get_by_code()'s and RoleRepository.get_by_code()'s
        pre-check pattern.
        """
        result = await self.session.execute(
            select(DomainPermission).where(
                DomainPermission.membership_id == membership_id,
                DomainPermission.domain_id == domain_id,
                DomainPermission.permission_level == permission_level,
                DomainPermission.effective_to.is_(None),
            )
        )
        return result.scalars().first()

    async def get_active_dependents(self, domain_permission_id: uuid.UUID) -> list[dict]:
        """
        WP-02 BA-09 (ERB-C003-03/EX-C003-09's enumeration requirement):
        unlike Role, no table anywhere in this schema references a
        Domain Permission row by id — a Domain Permission is itself the
        leaf grant (URA-001-47), not a policy other rows point back to.
        Always returns an empty list, disclosed here rather than
        silently omitted — this is an architectural fact about Domain
        Permission's own shape, not an unimplemented check.
        """
        return []

    async def has_active_dependents(self, domain_permission_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement). Reuses
        get_active_dependents() (WP-02 BA-09) as its own single source
        of truth, per the instruction not to duplicate dependency logic
        between the two Business Activities.
        """
        return len(await self.get_active_dependents(domain_permission_id)) > 0
