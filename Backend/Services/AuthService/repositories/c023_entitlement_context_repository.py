import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.c023_entitlement_context import C023EntitlementContext
from repositories.base_repository import BaseRepository


class C023EntitlementContextRepository(BaseRepository[C023EntitlementContext]):
    """
    Repository for `c023_entitlement_context` records (C-023, WP-17 BA-01).

    Write path uses the inherited `create()`. Only the INV-C023-09
    pre-check lookup is added.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(C023EntitlementContext, session)

    async def get_current_for_anchor(
        self,
        organization_id: uuid.UUID,
        domain_id: uuid.UUID | None,
        entitlement_type_ref: str,
    ) -> C023EntitlementContext | None:
        """
        The current (`effective_to IS NULL`) Authoritative Entitlement
        Context for this Entitlement Anchor (Organization + optional
        Domain) and entitlement type, if any — the INV-C023-09 pre-check
        (`TDS-C023 §15`). `domain_id IS NULL` (organization-wide) and a
        specific `domain_id` are matched exactly, consistent with the
        `COALESCE`-sentinel semantics of `ux_c023_entitlement_context_current`
        (Repository Owner D-4): a NULL and a set Domain are never treated
        as the same anchor.
        """
        conditions = [
            C023EntitlementContext.organization_id == organization_id,
            C023EntitlementContext.entitlement_type_ref == entitlement_type_ref,
            C023EntitlementContext.effective_to.is_(None),
        ]
        if domain_id is None:
            conditions.append(C023EntitlementContext.domain_id.is_(None))
        else:
            conditions.append(C023EntitlementContext.domain_id == domain_id)

        query = select(C023EntitlementContext).where(*conditions)
        result = await self.session.execute(query)
        return result.scalars().first()
