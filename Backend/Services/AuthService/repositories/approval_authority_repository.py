import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.approval_authority import ApprovalAuthority, VersionStatus
from repositories.base_repository import BaseRepository


class ApprovalAuthorityRepository(BaseRepository[ApprovalAuthority]):
    """
    Repository for Approval Authority records (C-003, WP-02 BA-03).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ApprovalAuthority, session)

    async def get_active_by_organization_and_name(
        self, organization_id: uuid.UUID, authority_name: str
    ) -> ApprovalAuthority | None:
        """
        WP-18 (C-003, TDS-018 §29.2 step 1): the currently-`ACTIVE` row for
        this Organization/`authority_name`, if any. Additive — does not
        change any existing method's behavior.
        """
        query = select(ApprovalAuthority).where(
            ApprovalAuthority.organization_id == organization_id,
            ApprovalAuthority.authority_name == authority_name,
            ApprovalAuthority.status == VersionStatus.ACTIVE.value,
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_any_by_organization_and_name(
        self, organization_id: uuid.UUID, authority_name: str
    ) -> ApprovalAuthority | None:
        """
        WP-18 (C-003, TDS-018 §29.2 step 1): any row (any status) for this
        Organization/`authority_name` — used only to distinguish
        `NO_AUTHORITY_CONFIGURED` (no row at all) from `INACTIVE_AUTHORITY`
        (a row exists but is `SUPERSEDED`/`DEPRECATED`/`RETIRED`). Additive
        — does not change any existing method's behavior.
        """
        query = select(ApprovalAuthority).where(
            ApprovalAuthority.organization_id == organization_id,
            ApprovalAuthority.authority_name == authority_name,
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_active_dependents(self, approval_authority_id: uuid.UUID) -> list[dict]:
        """
        WP-02 BA-09 (ERB-C003-03/EX-C003-09's enumeration requirement):
        Master Technical Architecture's canonical
        `membership_approval_authority` join table is the real dependent
        of an Approval Authority (URA-001), but it is not yet
        implemented anywhere in AuthService (no model, no migration) —
        the same disclosed gap already governing this object type's
        TD-023/TD-028. Always returns an empty list today. Disclosed
        here, not silently omitted: this is a genuine architectural
        completeness gap, not a deliberate design choice, and should be
        revisited once `membership_approval_authority` is implemented.
        """
        return []

    async def has_active_dependents(self, approval_authority_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement). Reuses
        get_active_dependents() (WP-02 BA-09) as its own single source
        of truth, per the instruction not to duplicate dependency logic
        between the two Business Activities.
        """
        return len(await self.get_active_dependents(approval_authority_id)) > 0
