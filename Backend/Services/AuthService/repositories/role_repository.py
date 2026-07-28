import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.membership import Membership
from models.role import Role
from models.role_permission import RolePermission
from repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """
    Repository for Role records (C-003, WP-02).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Role, session)

    async def get_by_code(self, role_code: str) -> Role | None:
        """
        Looks up a Role by its unique role_code — the natural key used
        for Establish Role's pre-flight duplicate check, mirroring
        OrganizationRepository.get_by_code()'s exact pattern.
        """
        result = await self.session.execute(
            select(Role).where(Role.role_code == role_code)
        )
        return result.scalars().first()

    async def get_active_dependents(self, role_id: uuid.UUID) -> list[dict]:
        """
        WP-02 BA-09 (ERB-C003-03/EX-C003-09's enumeration requirement,
        Contract 5.6): Role has two real, AuthService-implemented
        dependent tables today, both WP-00-era — `memberships.role_id`
        and `role_permissions.role_id` (found during BA-09's own
        Independent Review; the original implementation enumerated only
        Membership, an incomplete enumeration EX-C003-09's Success
        Criteria forbids: "every currently-active dependent is
        enumerated before a breaking change is permitted"). Returns one
        dict per currently-ACTIVE Membership, plus one dict per
        `role_permissions` row — the latter has no lifecycle/status
        column of its own (a permanent Role-to-Permission mapping,
        BR-C003-02's own "Permission Assignment" concern), so its mere
        existence is treated as an active dependent, never expiring on
        its own.

        Unlike the other four WP-02 object types (see their own
        get_active_dependents() docstrings), this enumeration is real,
        not vacuous — both tables have existed in AuthService since
        WP-00.
        """
        membership_result = await self.session.execute(
            select(Membership.id, Membership.person_id, Membership.organization_id).where(
                Membership.role_id == role_id,
                Membership.membership_status == "ACTIVE",
            )
        )
        dependents = [
            {
                "dependent_type": "Membership",
                "dependent_id": str(row.id),
                "person_id": str(row.person_id),
                "organization_id": str(row.organization_id),
            }
            for row in membership_result.all()
        ]

        role_permission_result = await self.session.execute(
            select(RolePermission.id, RolePermission.permission_id).where(
                RolePermission.role_id == role_id,
            )
        )
        dependents.extend(
            {
                "dependent_type": "RolePermission",
                "dependent_id": str(row.id),
                "permission_id": str(row.permission_id),
            }
            for row in role_permission_result.all()
        )

        return dependents

    async def has_active_dependents(self, role_id: uuid.UUID) -> bool:
        """
        WP-02 BA-08 (BR-C003-04's dependency-check requirement). Reuses
        get_active_dependents() (WP-02 BA-09) as its own single source
        of truth, per the instruction not to duplicate dependency logic
        between the two Business Activities — this method is now a
        boolean projection of that same query, not a separate one.
        """
        return len(await self.get_active_dependents(role_id)) > 0
