import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.domain_permission import DomainPermission, DomainPermissionLevel
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

    async def get_active_grant_at_or_above(
        self, membership_id, domain_id, minimum_level: str
    ) -> DomainPermission | None:
        """
        WP-13 (Authorization Runtime Integration) — the query the
        DomainPermission precedence tier (URA-001-76, least specific of
        five) actually needs: does this Membership hold a currently
        active grant, for this Domain, at or above the requested
        DomainPermissionLevel? Distinct from get_active_grant() (WP-02
        BA-02's own exact-triple duplicate check) — this method compares
        by rank, not exact match, and additionally respects `status`
        (ACTIVE only — SUPERSEDED/DEPRECATED/RETIRED never authorize)
        and the effective_from/effective_to time window, neither of
        which get_active_grant() checks (it predates BA-07/BA-08's own
        temporal/status model).

        Rank is DomainPermissionLevel's own declared enum order
        (VIEW < ENTER < EDIT < REVIEW < APPROVE < ASSIGN < DELEGATE <
        ADMIN, per URA-001-47) — no separate rank column exists in this
        schema; this is a disclosed interpretive choice, not an
        assumption silently made.
        """
        levels = list(DomainPermissionLevel)
        minimum_rank = levels.index(DomainPermissionLevel(minimum_level))
        qualifying_levels = [level.value for level in levels[minimum_rank:]]

        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(DomainPermission).where(
                DomainPermission.membership_id == membership_id,
                DomainPermission.domain_id == domain_id,
                DomainPermission.permission_level.in_(qualifying_levels),
                DomainPermission.status == "ACTIVE",
                DomainPermission.effective_from <= now,
                (DomainPermission.effective_to.is_(None)) | (DomainPermission.effective_to > now),
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

    async def search(
        self,
        domain_id: uuid.UUID | None = None,
        membership_id: uuid.UUID | None = None,
        status: str | None = None,
    ) -> list[DomainPermission]:
        """
        WP-06 BA-01 (EX-C003-11's list/query branch): returns every
        Domain Permission matching the given, independently optional
        Domain, Membership, and status criteria. No criterion supplied
        returns every Domain Permission. Read-only, per EX-C003-11's own
        Purpose statement.
        """
        query = select(DomainPermission)
        if domain_id is not None:
            query = query.where(DomainPermission.domain_id == domain_id)
        if membership_id is not None:
            query = query.where(DomainPermission.membership_id == membership_id)
        if status is not None:
            query = query.where(DomainPermission.status == status)
        result = await self.session.execute(query)
        return list(result.scalars().all())
