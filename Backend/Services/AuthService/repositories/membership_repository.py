from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models.membership import Membership
from repositories.base_repository import BaseRepository


class MembershipRepository(BaseRepository[Membership]):
    """
    Repository for Membership records.
    Resolves Person-Organization-Role associations required for JWT claim building.
    All queries that feed the login flow eagerly load Role to avoid N+1 queries.

    WP-03 BA-01 (Establish Membership Context) adds get_by_person_and_
    organization() below for its own recognition lookup; the write path
    (establish) uses the inherited create() directly, mirroring every
    other WP-01/WP-02 repository's own establish pattern — no new write
    method is needed here.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Membership, session)

    async def get_active_membership(
        self,
        person_id: UUID,
        organization_id: UUID
    ) -> Membership | None:
        """
        Returns the single active Membership for a (person_id, organization_id) pair.

        Eagerly loads Role so that membership.role.role_code is immediately available
        for JWT payload construction without a second round-trip.

        Returns None when:
          - No membership row exists for this person/org combination
          - The membership exists but membership_status != 'ACTIVE'
        Both cases surface as 401 in authenticate_user().
        """
        query = (
            select(Membership)
            .options(joinedload(Membership.role))
            .where(
                Membership.person_id == person_id,
                Membership.organization_id == organization_id,
                Membership.membership_status == "ACTIVE"
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_person_memberships(self, person_id: UUID) -> Sequence[Membership]:
        """
        Returns all active Memberships for a Person across all Organizations.

        Uses selectinload rather than joinedload because this is a collection result.
        Primary membership is returned first via ORDER BY is_primary DESC.
        Inactive, suspended, and invited memberships are excluded.
        """
        query = (
            select(Membership)
            .options(
                selectinload(Membership.role),
                selectinload(Membership.organization),
            )
            .where(
                Membership.person_id == person_id,
                Membership.membership_status == "ACTIVE"
            )
            .order_by(Membership.is_primary.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_person_and_organization(
        self,
        person_id: UUID,
        organization_id: UUID
    ) -> Membership | None:
        """
        Returns any Membership (regardless of status) for a
        (person_id, organization_id) pair — WP-03 BA-01's own
        recognition lookup (BR-C007-001/EX-C007-01): a new Authoritative
        Membership Context SHALL NOT be established without first
        confirming, deterministically, that none already exists for
        this pair. Unlike get_active_membership(), this intentionally
        does not filter by membership_status, since BR-C007-001
        concerns whether a Membership exists at all, not only an active
        one — the same UniqueConstraint('person_id', 'organization_id')
        the model already declares.
        """
        query = select(Membership).where(
            Membership.person_id == person_id,
            Membership.organization_id == organization_id,
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_primary_membership(self, person_id: UUID) -> Membership | None:
        """
        Returns the primary active Membership for a Person.

        Used when no organization context is present and a default organization
        must be resolved (e.g., single-org persons or first-login redirect).
        Eagerly loads Role for immediate role_code access.
        Returns None when the Person has no primary active membership.
        """
        query = (
            select(Membership)
            .options(joinedload(Membership.role))
            .where(
                Membership.person_id == person_id,
                Membership.is_primary.is_(True),
                Membership.membership_status == "ACTIVE"
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()
