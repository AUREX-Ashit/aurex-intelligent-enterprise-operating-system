import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.c023_license_context import C023LicenseContext
from repositories.base_repository import BaseRepository


class C023LicenseContextRepository(BaseRepository[C023LicenseContext]):
    """
    Repository for `c023_license_context` records (C-023, WP-17 BA-01).

    The write path (`establish`) uses the inherited `create()` directly,
    mirroring every prior WP-0X establish repository. Only the
    pre-check lookup below is added — the same shape
    `MembershipRepository.get_by_person_and_organization()` (WP-03) and
    `MembershipApprovalAuthorityRepository.get_open_binding()` (WP-18)
    established for their own "does a current row already exist?" guards.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(C023LicenseContext, session)

    async def get_current_for_membership(
        self, membership_id: uuid.UUID
    ) -> C023LicenseContext | None:
        """
        The current (`effective_to IS NULL`) Authoritative License Context
        for this Membership Anchor, if any — the INV-C023-10 pre-check
        (`TDS-C023 §15`, `PE-001-C023 §1.16`). The partial unique index
        `ux_c023_license_context_current` is the race-safe backstop; this
        lookup is the pre-check half of the certified
        pre-check-then-create-then-catch-`IntegrityError` pattern.
        """
        query = select(C023LicenseContext).where(
            C023LicenseContext.membership_id == membership_id,
            C023LicenseContext.effective_to.is_(None),
        )
        result = await self.session.execute(query)
        return result.scalars().first()
