"""
WP-03 — Membership Management (C-007).

Business Activities implemented here:
- BA-01 Establish Membership Context, realizing PE-001-C007's
  ERB-C007-01 / EX-C007-01 (Recognize Existing Membership) +
  EX-C007-02 (Establish New Membership).
- BA-02 Understand Membership Context, realizing ERB-C007-02 /
  EX-C007-03 — a pure read, computing but never storing the
  Membership's current authority consequence (BR-C007-013).
See IRA-003 for the full ERB/EX -> Business Activity mapping and
BA-01's own Architecture Validation (§9).

Follows RoleService.establish()/DomainPermissionService.establish()'s
exact pattern (WP-01/WP-02): existence checks on every referenced
object, duplicate-check-then-create, record_audit / publish_event for
SD-002-054's seven audit questions and RTA-001 §4.13 Domain Event
Publication.

BR-C007-001 (no establishment without prior deterministic recognition
lookup, EX-C007-01) is satisfied by construction: establish() always
calls get_by_person_and_organization() before creating a row.
BR-C007-002/007 (a candidate home-node context is not authoritative
until confirmed, and must reference a node returned by C-005/ERG-001-
03's own lookup) are satisfied by construction: a supplied
home_node_id is validated for existence and active_flag before being
persisted; it is never invented or defaulted.

Authorization disposition (mirrors IRA-002 §2.7's BA-01 precedent
exactly): PE-001-C007's EX-C007-02 names "Membership Steward"/
"Membership Sponsor" as its Participating Personas. No such
relationship is modeled anywhere in this codebase. This method
therefore gates on the same interim PLATFORM_ADMIN dependency WP-01/
WP-02 already use, disclosed here as a stated simplification and
recorded as TD-031, pending a future, separately-scoped persona
authority model.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.membership import Membership
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from repositories.organization_repository import OrganizationRepository
from repositories.person_repository import PersonRepository
from repositories.role_repository import RoleRepository
from schemas.membership import EstablishMembershipRequest, MembershipAuthorityConsequence
from observability import record_audit, publish_event, AuditStatus


def compute_membership_authority_consequence(
    membership: Membership, now: datetime | None = None
) -> tuple[bool, MembershipAuthorityConsequence]:
    """
    WP-03 BA-02 (Understand Membership Context, ERB-C007-02/EX-C007-03).

    Pure function, no I/O: derives whether a Membership currently
    carries authority from Standing Context (membership_status) and
    Effective Validity Context (effective_from/effective_to) together,
    per BR-C007-013 and Contract 5.1/5.3 — never from standing alone.
    Mirrors the same ACTIVE-but-effective_to-passed comparison
    `authorization_policy_conflict_service.py`'s own dependency check
    already uses (WP-02 BA-09), extended with the symmetric
    not-yet-effective case URA-001-21's own example ("Board Member
    2027-2029") implies. Never called from a write path; this
    computation is deliberately not persisted anywhere (BR-C007-013:
    "SHALL produce only a recomputed... Context").
    """
    now = now or datetime.now(timezone.utc)
    effective_from = _as_utc(membership.effective_from)
    effective_to = _as_utc(membership.effective_to)
    if membership.membership_status != "ACTIVE":
        return False, MembershipAuthorityConsequence.NOT_ACTIVE
    if effective_from is not None and now < effective_from:
        return False, MembershipAuthorityConsequence.ACTIVE_NOT_YET_EFFECTIVE
    if effective_to is not None and now >= effective_to:
        return False, MembershipAuthorityConsequence.ACTIVE_BUT_LAPSED
    return True, MembershipAuthorityConsequence.ACTIVE_AND_EFFECTIVE


def _as_utc(value: datetime | None) -> datetime | None:
    """
    Every effective_from/effective_to is always written as UTC-aware
    (models/membership.py's own `datetime.now(timezone.utc)` default),
    but SQLite's DateTime(timezone=True) does not preserve tzinfo on a
    fresh-session round trip (a documented SQLAlchemy/SQLite dialect
    limitation, not a Postgres behavior) — a value read back naive is
    still UTC, just missing its tzinfo, so it is safe to attach.
    """
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


class MembershipService:
    """Business Activity orchestrator for Membership establishment (WP-03 BA-01)."""

    def __init__(
        self,
        membership_repo: MembershipRepository,
        person_repo: PersonRepository,
        organization_repo: OrganizationRepository,
        role_repo: RoleRepository,
        organization_node_repo: OrganizationNodeRepository,
    ) -> None:
        self.membership_repo = membership_repo
        self.person_repo = person_repo
        self.organization_repo = organization_repo
        self.role_repo = role_repo
        self.organization_node_repo = organization_node_repo

    async def establish(
        self, request: EstablishMembershipRequest, actor_id: str | None = None
    ) -> Membership:
        """
        Business Activity: Establish Membership Context (BA-01).

        Structural rules (BR-C007-001/002/007, EX-C007-01/02 Entry
        Context):
        - The target Person must already exist (404 if not — "an
          Authoritative Person Context," C-006).
        - The target Organization must already exist (404 if not —
          "a valid Organization Context," C-004).
        - The target Role must already exist (404 if not — TD-033's
          inherited requirement).
        - If home_node_id is supplied, it must reference a real, active
          OrganizationNode (404 if missing, 409 if inactive) — BR-C007-
          002/007. If omitted, the Membership is established without a
          home-node anchor (TD-032).
        - No existing Membership (any status) for this (person_id,
          organization_id) pair (409) — BR-C007-001's own recognition
          discipline (EX-C007-01), the same duplicate-prevention basis
          RoleService.establish()/OrganizationService.establish()
          already apply to their own natural keys.
        """
        person = await self.person_repo.get_by_id(request.person_id)
        if person is None:
            record_audit(
                action="ESTABLISH_MEMBERSHIP",
                resource=f"person:{request.person_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target person does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No person found with id '{request.person_id}'.",
            )

        organization = await self.organization_repo.get_by_id(request.organization_id)
        if organization is None:
            record_audit(
                action="ESTABLISH_MEMBERSHIP",
                resource=f"organization:{request.organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target organization does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization found with id '{request.organization_id}'.",
            )

        role = await self.role_repo.get_by_id(request.role_id)
        if role is None:
            record_audit(
                action="ESTABLISH_MEMBERSHIP",
                resource=f"role:{request.role_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target role does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No role found with id '{request.role_id}'.",
            )

        if request.home_node_id is not None:
            home_node = await self.organization_node_repo.get_by_id(request.home_node_id)
            if home_node is None:
                record_audit(
                    action="ESTABLISH_MEMBERSHIP",
                    resource=f"organization_node:{request.home_node_id}",
                    status=AuditStatus.DENIED,
                    actor_id=actor_id or "SYSTEM",
                    metadata={"reason": "candidate home node does not exist"},
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No organization node found with id '{request.home_node_id}'.",
                )
            if not home_node.active_flag:
                record_audit(
                    action="ESTABLISH_MEMBERSHIP",
                    resource=f"organization_node:{request.home_node_id}",
                    status=AuditStatus.DENIED,
                    actor_id=actor_id or "SYSTEM",
                    metadata={"reason": "candidate home node is not active"},
                )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Organization node '{request.home_node_id}' is not active and cannot anchor a new Membership.",
                )

        existing = await self.membership_repo.get_by_person_and_organization(
            request.person_id, request.organization_id
        )
        if existing is not None:
            record_audit(
                action="ESTABLISH_MEMBERSHIP",
                resource=f"membership:{request.person_id}:{request.organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "a membership already exists for this person and organization"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"A Membership already exists for person '{request.person_id}' "
                    f"in organization '{request.organization_id}'."
                ),
            )

        create_kwargs: dict = {
            "person_id": request.person_id,
            "organization_id": request.organization_id,
            "role_id": request.role_id,
            "home_node_id": request.home_node_id,
            "membership_type": request.membership_type.value,
            "license_type": request.license_type.value,
            "is_primary": request.is_primary,
        }
        if request.effective_from is not None:
            create_kwargs["effective_from"] = request.effective_from
        if request.effective_to is not None:
            create_kwargs["effective_to"] = request.effective_to

        try:
            membership = await self.membership_repo.create(create_kwargs)
            await self.membership_repo.session.flush()
        except IntegrityError:
            # Closes the race window between the pre-check above and this
            # insert, same basis as RoleService.establish()/OrganizationService.establish().
            await self.membership_repo.session.rollback()
            record_audit(
                action="ESTABLISH_MEMBERSHIP",
                resource=f"membership:{request.person_id}:{request.organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "a membership already exists for this person and organization (concurrent creation)"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"A Membership already exists for person '{request.person_id}' "
                    f"in organization '{request.organization_id}'."
                ),
            )

        record_audit(
            action="ESTABLISH_MEMBERSHIP",
            resource=f"membership:{membership.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "person_id": str(membership.person_id),
                "organization_id": str(membership.organization_id),
                "role_id": str(membership.role_id),
                "home_node_id": str(membership.home_node_id) if membership.home_node_id else None,
            },
        )
        publish_event(
            "MEMBERSHIP_ESTABLISHED",
            {
                "membership_id": str(membership.id),
                "person_id": str(membership.person_id),
                "organization_id": str(membership.organization_id),
            },
        )
        return membership

    async def understand(self, membership_id: UUID) -> Membership:
        """
        Business Activity: Understand Membership Context (BA-02,
        ERB-C007-02/EX-C007-03).

        Read-only — no audit record or domain event, the same basis
        already established for Organization's own read-side Business
        Activity (`OrganizationService.get_details()`: only a write
        path audits). Reuses `BaseRepository.get_by_id()` via
        `MembershipRepository` as-is — no new repository method
        required. The caller (router) is responsible for computing
        the Membership Authority Consequence via
        `compute_membership_authority_consequence()` above; this method
        never mutates the returned Membership and never computes or
        caches that consequence itself.
        """
        membership = await self.membership_repo.get_by_id(membership_id)
        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Membership exists with id '{membership_id}'.",
            )
        return membership
