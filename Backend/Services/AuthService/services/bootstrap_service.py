"""
WP-00 Platform Bootstrap — Business Activity implementation.

Realizes CAP-001 C-001/C-004/C-006 (Identity/Organization/Person
Management) via the seed execution path IMP-001 Section 12.3 mandates
("The Master Data Population Specification executes as an automated,
idempotent pipeline stage on environment provisioning — never as a
manually-run script an engineer executes once and forgets") — applied
here to AuthService's own R-001 bootstrap data specifically.

REUSE NOTE: the data values below are not new — they are
scripts/bootstrap_data.py's port of the already-approved
scripts/03_seed_r001_data.sql, 05_bootstrap_first_user.sql, and
07_bootstrap_platform_admin.sql. Those SQL files remain unchanged in the
repository as the original manual-execution reference. This service
reimplements their *execution mechanism* only — via the existing
SQLAlchemy ORM models and BaseRepository (repositories/base_repository.py)
already used everywhere else in AuthService — rather than shelling out to
psql, for two reasons neither script satisfies: (1) testability against
the same in-memory SQLite database every other AuthService test already
uses (tests/conftest.py), and (2) consistency with the ORM-first pattern
this codebase already established (no other Business Activity in this
service is implemented via raw SQL). Dedicated OrganizationRepository and
RoleRepository classes are deliberately NOT created here — the generic
BaseRepository already covers this Business Activity's narrow read/create
needs, and per the Aurex Platform Administrator Roadmap, building the full
Organization/Role business-activity surface (with UI and APIs) is WP-01's
and WP-06's scope, not WP-00's.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, replace
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.identity import Identity
from models.membership import Membership
from models.organization import Organization
from models.permission import Permission
from models.person import Person
from models.role import Role
from models.role_permission import RolePermission
from repositories.base_repository import BaseRepository
from observability import record_audit, publish_event, record_metric, AuditStatus, Timer
from scripts import bootstrap_data as seed

_PRODUCTION_ENVIRONMENTS = {"production", "prod"}


def _resolve_seed_identity(identity: seed.IdentitySeed, override_env_var: str) -> seed.IdentitySeed:
    """
    IC-001 M1 safeguard: scripts/bootstrap_data.py's bcrypt hashes are public
    (visible in source, documented in RUNBOOK_BOOTSTRAP.md). Seeding them
    as-is is acceptable for development/staging demonstration but must never
    happen unattended in production. If `override_env_var` is set, its value
    (a bcrypt hash of an operator-chosen password) replaces the built-in
    hash. Otherwise, in a production environment, bootstrap refuses to run
    rather than silently seeding a publicly-known credential.
    """
    override_hash = os.getenv(override_env_var)
    if override_hash:
        return replace(identity, password_hash=override_hash)
    if settings.environment in _PRODUCTION_ENVIRONMENTS:
        raise RuntimeError(
            f"Refusing to bootstrap '{identity.email}' using the built-in demo "
            f"password hash in a production environment (ENVIRONMENT="
            f"'{settings.environment}'). Set {override_env_var} to a bcrypt hash "
            f"of a real, rotated password before running bootstrap."
        )
    return identity


@dataclass
class BootstrapResult:
    """Outcome of one bootstrap run — every count reflects rows *created this run* (0 on a re-run)."""
    roles_created: int = 0
    permissions_created: int = 0
    role_permissions_created: int = 0
    organizations_created: int = 0
    persons_created: int = 0
    identities_created: int = 0
    memberships_created: int = 0

    @property
    def total_created(self) -> int:
        return (
            self.roles_created + self.permissions_created + self.role_permissions_created
            + self.organizations_created + self.persons_created + self.identities_created
            + self.memberships_created
        )

    @property
    def is_first_run(self) -> bool:
        return self.total_created > 0


class BootstrapService:
    """
    Idempotent orchestrator for the R-001 seed data. Safe to invoke on
    every deployment (IMP-CICD-002) — a second invocation always returns
    a BootstrapResult with every count at 0, never a duplicate row and
    never an error.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.roles = BaseRepository(Role, session)
        self.permissions = BaseRepository(Permission, session)
        self.role_permissions = BaseRepository(RolePermission, session)
        self.organizations = BaseRepository(Organization, session)
        self.persons = BaseRepository(Person, session)
        self.identities = BaseRepository(Identity, session)
        self.memberships = BaseRepository(Membership, session)

    async def run(self) -> BootstrapResult:
        with Timer() as timer:
            result = BootstrapResult()
            try:
                result.roles_created = await self._seed_roles()
                result.permissions_created = await self._seed_permissions()
                result.role_permissions_created = await self._seed_role_permissions()
                result.organizations_created = await self._seed_organization()
                result.persons_created += await self._seed_person(seed.DEMO_ADMIN_PERSON)
                result.persons_created += await self._seed_person(seed.PLATFORM_ADMIN_PERSON)
                demo_admin_identity = _resolve_seed_identity(seed.DEMO_ADMIN_IDENTITY, "BOOTSTRAP_ADMIN_PASSWORD_HASH")
                platform_admin_identity = _resolve_seed_identity(
                    seed.PLATFORM_ADMIN_IDENTITY, "BOOTSTRAP_PLATFORM_ADMIN_PASSWORD_HASH"
                )
                result.identities_created += await self._seed_identity(demo_admin_identity)
                result.identities_created += await self._seed_identity(platform_admin_identity)
                result.memberships_created += await self._seed_membership(seed.DEMO_ADMIN_MEMBERSHIP)
                result.memberships_created += await self._seed_membership(seed.PLATFORM_ADMIN_MEMBERSHIP)
                await self.session.commit()
            except Exception as exc:
                await self.session.rollback()
                record_audit(
                    action="PLATFORM_BOOTSTRAP",
                    resource="authservice.bootstrap",
                    status=AuditStatus.FAILED,
                    metadata={"error": str(exc)},
                )
                record_metric("bootstrap.run.failed", 1.0)
                raise

        record_audit(
            action="PLATFORM_BOOTSTRAP",
            resource="authservice.bootstrap",
            status=AuditStatus.SUCCESS,
            metadata={
                "total_created": result.total_created,
                "is_first_run": result.is_first_run,
                "duration_seconds": round(timer.elapsed_seconds, 4),
            },
        )
        publish_event(
            "PLATFORM_BOOTSTRAPPED",
            {
                "roles_created": result.roles_created,
                "permissions_created": result.permissions_created,
                "role_permissions_created": result.role_permissions_created,
                "organizations_created": result.organizations_created,
                "persons_created": result.persons_created,
                "identities_created": result.identities_created,
                "memberships_created": result.memberships_created,
                "is_first_run": result.is_first_run,
            },
        )
        record_metric("bootstrap.run.duration_seconds", timer.elapsed_seconds)
        record_metric("bootstrap.run.rows_created", float(result.total_created))
        return result

    # -- idempotent per-entity seeding -----------------------------------

    async def _existing_role_codes(self) -> set[str]:
        rows: Sequence[Role] = (await self.session.execute(select(Role.role_code))).scalars().all()  # type: ignore[assignment]
        return set(rows)

    async def _seed_roles(self) -> int:
        existing = await self._existing_role_codes()
        created = 0
        for role in seed.ROLES:
            if role.role_code in existing:
                continue
            await self.roles.create(
                {
                    "id": role.id,
                    "role_code": role.role_code,
                    "role_name": role.role_name,
                    "description": role.description,
                    "is_system_role": role.is_system_role,
                }
            )
            created += 1
        return created

    async def _seed_permissions(self) -> int:
        existing_codes = set(
            (await self.session.execute(select(Permission.permission_code))).scalars().all()
        )
        created = 0
        for permission in seed.PERMISSIONS:
            if permission.permission_code in existing_codes:
                continue
            await self.permissions.create(
                {
                    "id": permission.id,
                    "permission_code": permission.permission_code,
                    "permission_name": permission.permission_name,
                    "description": permission.description,
                }
            )
            created += 1
        return created

    async def _seed_role_permissions(self) -> int:
        existing_pairs = set(
            (await self.session.execute(select(RolePermission.role_id, RolePermission.permission_id))).all()
        )
        created = 0
        for role_id, permission_ids in seed.ROLE_PERMISSIONS.items():
            for permission_id in permission_ids:
                if (role_id, permission_id) in existing_pairs:
                    continue
                await self.role_permissions.create({"role_id": role_id, "permission_id": permission_id})
                created += 1
        return created

    async def _seed_organization(self) -> int:
        existing = await self.session.execute(
            select(Organization).where(Organization.organization_code == seed.DEMO_ORGANIZATION.organization_code)
        )
        if existing.scalar_one_or_none() is not None:
            return 0
        await self.organizations.create(
            {
                "id": seed.DEMO_ORGANIZATION.id,
                "organization_code": seed.DEMO_ORGANIZATION.organization_code,
                "organization_name": seed.DEMO_ORGANIZATION.organization_name,
                "organization_type": seed.DEMO_ORGANIZATION.organization_type,
                "is_active": True,
            }
        )
        return 1

    async def _seed_person(self, person: seed.PersonSeed) -> int:
        if await self.persons.get_by_id(person.id) is not None:
            return 0
        await self.persons.create(
            {
                "id": person.id,
                "first_name": person.first_name,
                "last_name": person.last_name,
                "display_name": person.display_name,
                "is_active": True,
            }
        )
        return 1

    async def _seed_identity(self, identity: seed.IdentitySeed) -> int:
        existing = await self.session.execute(select(Identity).where(Identity.email == identity.email))
        if existing.scalar_one_or_none() is not None:
            return 0
        await self.identities.create(
            {
                "id": identity.id,
                "person_id": identity.person_id,
                "email": identity.email,
                "password_hash": identity.password_hash,
                "identity_type": identity.identity_type,
                "is_primary": identity.is_primary,
                "is_verified": identity.is_verified,
            }
        )
        return 1

    async def _seed_membership(self, membership: seed.MembershipSeed) -> int:
        existing = await self.session.execute(
            select(Membership).where(
                Membership.person_id == membership.person_id,
                Membership.organization_id == membership.organization_id,
            )
        )
        if existing.scalar_one_or_none() is not None:
            return 0
        await self.memberships.create(
            {
                "id": membership.id,
                "person_id": membership.person_id,
                "organization_id": membership.organization_id,
                "role_id": membership.role_id,
                "membership_status": membership.membership_status,
                "is_primary": membership.is_primary,
            }
        )
        return 1

    # -- readiness support -------------------------------------------------

    async def is_bootstrapped(self) -> bool:
        """Used by the /ready endpoint: true once the Platform Administrator can log in."""
        result = await self.session.execute(
            select(Identity).where(Identity.email == seed.PLATFORM_ADMIN_IDENTITY.email)
        )
        return result.scalar_one_or_none() is not None
