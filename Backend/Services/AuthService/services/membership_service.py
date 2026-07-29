"""
WP-03 — Membership Management (C-007).

Business Activities implemented here:
- BA-01 Establish Membership Context, realizing PE-001-C007's
  ERB-C007-01 / EX-C007-01 (Recognize Existing Membership) +
  EX-C007-02 (Establish New Membership).
- BA-02 Understand Membership Context, realizing ERB-C007-02 /
  EX-C007-03 — a pure read, computing but never storing the
  Membership's current authority consequence (BR-C007-013).
- BA-03 Maintain Membership Terms, realizing ERB-C007-03 /
  EX-C007-04 (Resolve Conflicting Membership Terms) + EX-C007-05
  (Change Membership Terms). EX-C007-06 (Reconfirm Home-Node
  Structural Congruence) is explicitly out of BA-03's scope — its own
  Trigger requires a structural-change signal from C-005/ERG-001,
  and no such signal producer exists anywhere in this codebase
  (Enterprise Structure Management/C-005 has no IRA). See
  IMP-REPORT-WP-03's BA-03 gap analysis for the full disposition.
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
from typing import Any
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.membership import Membership
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from repositories.organization_repository import OrganizationRepository
from repositories.person_repository import PersonRepository
from repositories.role_repository import RoleRepository
from schemas.membership import (
    ChangeMembershipTermsRequest,
    EstablishMembershipRequest,
    HandOffMembershipContextRequest,
    HandoffOutcome,
    MembershipAuthorityConsequence,
    MembershipHandoffResponse,
    MembershipPortfolioResponse,
    MembershipResponse,
    MembershipUnderstandingResponse,
    MultiOrganizationAwarenessResponse,
    ReactivateMembershipRequest,
)
from observability import record_audit, publish_event, AuditStatus

CHANGEABLE_TERM_FIELDS = ("membership_type", "license_type", "home_node_id", "effective_from", "effective_to")


def _audit_value(value: Any) -> Any:
    """JSON-safe serialization for record_audit()'s metadata (UUID/datetime aren't natively json.dumps-able)."""
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


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

    async def change_terms(
        self, membership_id: UUID, request: ChangeMembershipTermsRequest, actor_id: str | None = None
    ) -> Membership:
        """
        Business Activity: Maintain Membership Terms (BA-03,
        ERB-C007-03 / EX-C007-04 Resolve Conflicting Membership Terms +
        EX-C007-05 Change Membership Terms).

        BR-C007-003 (classify before resolving): a supplied field equal
        to the Membership's current value is not a change for that
        field; if every supplied field is unchanged, the whole request
        is classified erroneous and rejected (409) — EX-C007-04's own
        "reject" outcome. At least one genuine difference classifies
        the request as a real change need and applies it — EX-C007-05.

        BR-C007-004 (preserve pre-change value): captured in
        record_audit()'s own previous_<field>/new_<field> metadata, the
        same traceability mechanism OrganizationService.activate()/
        suspend()/retire() already use for previous_status — no new
        versioning table, per IRA-003 §10's own Category B
        classification for this Business Activity.

        BR-C007-006 (terms independent of standing): satisfied by
        construction — membership_status is never read or written here.

        home_node_id, when supplied and changed, is validated exactly
        as BA-01's establish() validates it (404 unknown, 409 inactive)
        — BR-C007-002/007. EX-C007-06 (structural-signal-triggered
        reconfirmation) is out of scope; see this method's own module
        docstring / IMP-REPORT-WP-03's BA-03 gap analysis for why.

        effective_from/effective_to are normalized via _as_utc() before
        comparison — the same BA-02 fresh-session-round-trip fix reused
        here, since a Membership fetched via get_by_id() in a genuinely
        new request/session returns these fields offset-naive under
        SQLite's DateTime(timezone=True) dialect limitation; comparing
        a naive current_value against an offset-aware supplied value
        with `!=` never signals equality, which would misclassify a
        resupplied-identical value as a genuine change (BR-C007-003).
        """
        membership = await self.membership_repo.get_by_id(membership_id)
        if membership is None:
            record_audit(
                action="CHANGE_MEMBERSHIP_TERMS",
                resource=f"membership:{membership_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "membership not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Membership exists with id '{membership_id}'.",
            )

        supplied = request.model_dump(exclude_unset=True, exclude={"reason"})
        if not supplied:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="At least one term field (membership_type, license_type, home_node_id, effective_from, effective_to) must be supplied.",
            )

        changes: dict[str, tuple[Any, Any]] = {}
        for field, new_value in supplied.items():
            if field in ("membership_type", "license_type") and new_value is not None:
                new_value = new_value.value if hasattr(new_value, "value") else new_value
            current_value = getattr(membership, field)
            if field in ("effective_from", "effective_to"):
                current_value = _as_utc(current_value)
                new_value = _as_utc(new_value)
            if new_value != current_value:
                changes[field] = (current_value, new_value)

        if not changes:
            # BR-C007-003: every supplied term already matches the current value — classified erroneous (EX-C007-04's own "reject" outcome).
            record_audit(
                action="CHANGE_MEMBERSHIP_TERMS",
                resource=f"membership:{membership_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "requested terms match the membership's current terms; classified as an erroneous request, not a genuine change need"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Requested terms match the Membership's current terms; nothing to change.",
            )

        if "home_node_id" in changes:
            new_home_node_id = changes["home_node_id"][1]
            if new_home_node_id is not None:
                home_node = await self.organization_node_repo.get_by_id(new_home_node_id)
                if home_node is None:
                    record_audit(
                        action="CHANGE_MEMBERSHIP_TERMS",
                        resource=f"organization_node:{new_home_node_id}",
                        status=AuditStatus.DENIED,
                        actor_id=actor_id or "SYSTEM",
                        metadata={"reason": "candidate home node does not exist"},
                    )
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No organization node found with id '{new_home_node_id}'.",
                    )
                if not home_node.active_flag:
                    record_audit(
                        action="CHANGE_MEMBERSHIP_TERMS",
                        resource=f"organization_node:{new_home_node_id}",
                        status=AuditStatus.DENIED,
                        actor_id=actor_id or "SYSTEM",
                        metadata={"reason": "candidate home node is not active"},
                    )
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Organization node '{new_home_node_id}' is not active and cannot anchor this Membership.",
                    )

        update_kwargs = {field: new for field, (_old, new) in changes.items()}
        updated = await self.membership_repo.update(membership_id, update_kwargs)
        await self.membership_repo.session.flush()

        record_audit(
            action="CHANGE_MEMBERSHIP_TERMS",
            resource=f"membership:{membership_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "changed_fields": list(changes.keys()),
                **{f"previous_{field}": _audit_value(old) for field, (old, _new) in changes.items()},
                **{f"new_{field}": _audit_value(new) for field, (_old, new) in changes.items()},
                "reason": request.reason,
            },
        )
        publish_event(
            "MEMBERSHIP_TERMS_CHANGED",
            {
                "membership_id": str(membership_id),
                "changed_fields": list(changes.keys()),
            },
        )
        return updated

    async def reactivate(
        self, membership_id: UUID, request: ReactivateMembershipRequest, actor_id: str | None = None
    ) -> Membership:
        """
        Business Activity: Reactivate Membership (BA-06, ERB-C007-04 /
        EX-C007-08).

        Per PE-001-C007's own Exception & Recovery Semantics (6.3,
        "Reactivation not permitted by governing lifecycle authority")
        and Contract 5.3: URA-001-20 establishes the canonical standing
        states only, no canonical matrix of which source standing may
        transition to active. C-007 SHALL NOT invent such permission.
        No ADR or other canonical document anywhere in this repository
        establishes that SUSPENDED, DEACTIVATED, or ARCHIVED may
        transition to ACTIVE (same root cause as BA-05's own BLOCKED —
        Governance Decision Required disposition; see TD-037).

        BR-C007-014 requires that, absent established permission, "the
        outcome SHALL instead be explicit and unresolved or rejected"
        — this method implements exactly that: the existing Membership
        is never mutated, and every call is rejected with 409, citing
        Pending Canonical Binding. This is EX-C007-08's own explicitly
        named second completion path (the first — a permitted
        reactivation actually applied — is not reachable until a
        future governance decision establishes real permitted
        transitions).
        """
        membership = await self.membership_repo.get_by_id(membership_id)
        if membership is None:
            record_audit(
                action="REACTIVATE_MEMBERSHIP",
                resource=f"membership:{membership_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "membership not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Membership exists with id '{membership_id}'.",
            )

        if membership.membership_status == "ACTIVE":
            record_audit(
                action="REACTIVATE_MEMBERSHIP",
                resource=f"membership:{membership_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "membership is already ACTIVE; there is nothing to reactivate"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Membership is already ACTIVE; there is nothing to reactivate.",
            )

        # BR-C007-014 / Contract 5.3: no canonical authority anywhere establishes
        # that this (or any) non-active standing may transition to ACTIVE.
        # C-007 SHALL NOT invent that permission. TD-037.
        record_audit(
            action="REACTIVATE_MEMBERSHIP",
            resource=f"membership:{membership_id}",
            status=AuditStatus.DENIED,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "current_standing": membership.membership_status,
                "reason": request.reason,
                "rejection_basis": (
                    "no canonical authority establishes that this standing may "
                    "transition to ACTIVE (Pending Canonical Binding, TD-037)"
                ),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Reactivation from '{membership.membership_status}' to ACTIVE is not "
                "currently permitted: no canonical authority establishes this transition "
                "(Pending Canonical Binding, TD-037)."
            ),
        )

    async def surface_multi_organization_awareness(
        self, person_id: UUID, organization_id: UUID, actor_id: str | None = None
    ) -> MultiOrganizationAwarenessResponse:
        """
        Business Activity: Surface Multi-Organization Membership
        Awareness During Establishment (BA-07, ERB-C007-05 /
        EX-C007-09).

        BR-C007-008 / Contract 5.4: an establishing Organization SHALL
        receive, at most, an existence-only signal that a Person holds
        other Memberships — never which Organizations, on what terms,
        or under what standing (URA-001-17a's cross-tenant restriction).
        Reuses MembershipRepository.get_person_memberships() as-is (the
        same ACTIVE-only, cross-organization query WP-00's own login
        flow already relies on) — no new repository method required,
        confirming IRA-003 §10/§14's own Category B classification.

        Unlike BA-02's own pure-read precedent ("only a write path
        audits"), every call here is audited — success and denial
        alike — because this crosses a cross-tenant data-isolation
        boundary (BR-C007-008/URA-001-17a), a materially different
        sensitivity class than a same-organization single-Membership
        read. No explicit, named, audited cross-tenant sharing
        agreement mechanism exists anywhere in this codebase (see
        TD-040); the existence-only default below is therefore always
        what is returned.
        """
        person = await self.person_repo.get_by_id(person_id)
        if person is None:
            record_audit(
                action="SURFACE_MULTI_ORGANIZATION_AWARENESS",
                resource=f"person:{person_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target person does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No person found with id '{person_id}'.",
            )

        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            record_audit(
                action="SURFACE_MULTI_ORGANIZATION_AWARENESS",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "requesting organization does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization found with id '{organization_id}'.",
            )

        memberships = await self.membership_repo.get_person_memberships(person_id)
        has_other = any(m.organization_id != organization_id for m in memberships)

        record_audit(
            action="SURFACE_MULTI_ORGANIZATION_AWARENESS",
            resource=f"person:{person_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "requesting_organization_id": str(organization_id),
                "has_memberships_in_other_organizations": has_other,
            },
        )
        return MultiOrganizationAwarenessResponse(has_memberships_in_other_organizations=has_other)

    async def present_own_portfolio(self, person_id: UUID) -> MembershipPortfolioResponse:
        """
        Business Activity: Present Person's Own Cross-Organization
        Membership View (BA-08, ERB-C007-05 / EX-C007-10).

        BR-C007-009: a Membership Subject SHALL be able to see the
        complete detail of their own Membership portfolio — this is a
        materially different visibility posture from BA-07's own
        existence-only signal (BR-C007-008), because the caller is
        viewing their *own* data, which URA-001-17a's cross-tenant
        restriction never applied to in the first place (it governs an
        *establishing Organization's* visibility into a Person's
        Memberships elsewhere, not the Person's own).

        person_id is supplied by the router directly from the caller's
        own verified JWT claims, never from a query parameter — the
        entire safety property here rests on the caller only ever being
        able to name themselves. EX-C007-10's own second Participating
        Persona, "Platform Oversight Participant where an authorized
        aggregator is involved," is deliberately NOT implemented: no
        distinct aggregator claim exists anywhere in this codebase, and
        standing PLATFORM_ADMIN in for it — unlike every prior WP-03
        Business Activity's own interim-gate simplification — would let
        any platform admin read any Person's complete cross-tenant
        Membership detail, a materially larger exposure than anything
        BA-01 through BA-07 permit. Disclosed as TD-041, not silently
        implemented as an admin-accessible endpoint.

        Reuses MembershipRepository.get_person_memberships() as-is (the
        same query BA-07 already reuses) — no new repository method.
        No audit record: mirrors BA-02's own "only a write path audits"
        precedent, since a person reading their own data is not a
        cross-tenant-boundary event the way BA-07's cross-organization
        awareness check is.
        """
        memberships = await self.membership_repo.get_person_memberships(person_id)
        return MembershipPortfolioResponse(
            memberships=[MembershipResponse.model_validate(m) for m in memberships]
        )

    async def hand_off(
        self, membership_id: UUID, request: HandOffMembershipContextRequest, actor_id: str | None = None
    ) -> MembershipHandoffResponse:
        """
        Business Activity: Hand Off Membership Context to a Dependent
        Capability (BA-10, ERB-C007-06 / EX-C007-12).

        Per Contract 5.10, C-007 never calls into the named dependent
        capability's own API — no live integration exists anywhere in
        this codebase, and two of the three named capabilities (C-002,
        C-008) have no implementation at all (TD-042). The caller
        reports the already-resolved outcome, mirroring WP-02 BA-10's
        own `classify_handoff_rejection()` precedent exactly: compute
        fresh from existing state, audit, publish an event, return —
        never persist a new row.

        BR-C007-010 (bounded context + fresh authority consequence +
        explicit outcome): satisfied by reusing
        compute_membership_authority_consequence() (the same mechanism
        BA-02 and BA-09 already reuse) and composing
        MembershipUnderstandingResponse as the transferred context,
        never assembling a broader payload.

        BR-C007-011 (a downstream rejection SHALL NOT alter the
        underlying Authoritative Membership Context): satisfied by
        construction — this method never writes to `membership_status`
        or any other Membership field, for either outcome.

        "Context Superseded"/"Context Invalidated" (EX-C007-12's own
        traceability requirement for a superseded hand-off attempt) is
        satisfied by the audit trail itself: every call is independently
        recorded via record_audit(), so two hand-off reports for the
        same Membership remain separately traceable without a dedicated
        new table — the same audit-based traceability precedent BA-03/
        BA-06 already established for Membership Management itself.
        """
        membership = await self.membership_repo.get_by_id(membership_id)
        if membership is None:
            record_audit(
                action="HAND_OFF_MEMBERSHIP_CONTEXT",
                resource=f"membership:{membership_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "membership not found", "dependent_capability": request.dependent_capability.value},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Membership exists with id '{membership_id}'.",
            )

        if request.outcome == HandoffOutcome.RETURNED and not request.reason:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A reason is required when outcome is RETURNED (EX-C007-12's own 'insufficient Membership context' case).",
            )

        currently_effective, authority_consequence = compute_membership_authority_consequence(membership)
        understanding = MembershipUnderstandingResponse(
            **MembershipResponse.model_validate(membership).model_dump(),
            currently_effective=currently_effective,
            authority_consequence=authority_consequence,
        )
        handed_off_at = datetime.now(timezone.utc)

        record_audit(
            action="HAND_OFF_MEMBERSHIP_CONTEXT",
            resource=f"membership:{membership_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "dependent_capability": request.dependent_capability.value,
                "outcome": request.outcome.value,
                "reason": request.reason,
                "authority_consequence": authority_consequence.value,
                "currently_effective": currently_effective,
            },
        )
        publish_event(
            "MEMBERSHIP_CONTEXT_HANDED_OFF",
            {
                "membership_id": str(membership_id),
                "dependent_capability": request.dependent_capability.value,
                "outcome": request.outcome.value,
            },
        )

        return MembershipHandoffResponse(
            membership_context=understanding,
            dependent_capability=request.dependent_capability,
            outcome=request.outcome,
            reason=request.reason,
            handed_off_at=handed_off_at,
        )
