from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from models.identity import Identity
from repositories.base_repository import BaseRepository


class IdentityRepository(BaseRepository[Identity]):
    """
    Repository for Identity records.
    Handles credential lookup for the R-001 login flow.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Identity, session)

    async def get_by_email(self, email: str) -> Identity | None:
        """
        Looks up an Identity by email address.
        First step of the login flow: resolve credentials before touching Person.
        Returns None when no matching Identity exists, which surfaces as 401.
        """
        query = select(Identity).where(Identity.email == email)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_email_with_person(self, email: str) -> Identity | None:
        """
        Looks up an Identity by email address with its Person eagerly loaded.

        Used by Person recognition (EX-C006-01, deterministic path): email is
        the only existing authoritative identifier that already carries a
        governed pointer to an Authoritative Person Context (every Identity
        traces to exactly one Person, per BR-C001-01). Eagerly loads Person
        so the recognition outcome is available without a second round-trip,
        following the same avoid-N+1 convention as MembershipRepository.

        Separate from get_by_email() (used by the login flow) so that login's
        existing query shape and behavior are left untouched.
        """
        query = (
            select(Identity)
            .options(joinedload(Identity.person))
            .where(Identity.email == email)
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_primary_identity(self, person_id: UUID) -> Identity | None:
        """
        Returns the primary Identity for a Person.
        Used when re-issuing tokens to confirm the Person still has an active
        primary credential (e.g., account not converted to SSO-only).
        """
        query = (
            select(Identity)
            .where(
                Identity.person_id == person_id,
                Identity.is_primary.is_(True)
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_person_identities(self, person_id: UUID) -> Sequence[Identity]:
        """
        Returns all Identities for a Person, primary first.
        Ordered by is_primary DESC so the primary credential is always at index 0.
        """
        query = (
            select(Identity)
            .where(Identity.person_id == person_id)
            .order_by(Identity.is_primary.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()
