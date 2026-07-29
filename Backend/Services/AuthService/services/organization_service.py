"""
WP-01 — Organization Management (C-004).

Business Activities implemented here (renamed per the WP-01 Scope
Reconciliation, IRA-001 §15, to align with PE-001-C004's canonical
ERBs): BA-01 Establish Organization Identity (amended, IRA-001A —
see below), BA-01B Verify Organization Domain Claim (new, IRA-001A),
BA-01C Activate Organization first-time (new, IRA-001A), BA-02
Resolve Organization Details, BA-03 Search & List Organizations,
BA-04 Steward Organization Identity, BA-05 Reactivate Suspended
Organization, BA-06 Suspend Organization, BA-07 Retire Organization &
Preserve Continuity.

IRA-001A constitutional correction (BR-C004-01, BR-C004-08, Contract
5.4): BA-01's original behavior wrote a fully-Authoritative, ACTIVE
Organization row directly on establishment — CERT-WP-01's own Finding
A, and this repository's own independent behavioral-compliance and
historical-governance investigations, established that this violates
BR-C004-01 ("An Organization SHALL NOT be treated as valid before
governed activation") and Contract 5.4 ("Prior to activation, no
Organization exists in this sense") using code that existed at
certification time — not merely a documentation-accuracy gap.
establish() now writes only to `organization_establishment_attempts`
(the Organization Anchor Context, PE-001-C004 §1.16) — a genuinely
separate, non-authoritative construct BA-02/BA-03 never query, so
BR-C004-08 ("An Organization Anchor Context SHALL NOT be treated as...
an Authoritative Organization Context... under any circumstance") and
Contract 5.4's "resolve as NOT_FOUND" requirement are satisfied by
construction rather than by read-path filtering discipline. The first
`organizations` row for a given establishment attempt is now created
only by activate_establishment() (BA-01C), the first and only
distinct, named, audited, governed-activation act (ERB-C004-03).
BA-02 through BA-07 are unmodified by this correction — none of them
ever queries `organization_establishment_attempts`.

Realizes CAP-001 C-004 per the ADR-003/ADR-004/ADR-005-scoped
implementation approved in IRA-001, corrected per IRA-001A. Follows
IMP-001 §6.3's Business Activity Lifecycle (Request -> Validation ->
Business Rule Execution -> Business Object Update -> Domain Event
Publication -> Audit Recording -> Response) and reuses WP-00's
established patterns exactly:
  - duplicate-check-then-create, mirroring EstablishPersonContextService
    (services/establish_person_context_service.py), strengthened here by
    also catching the database's own unique-constraint (both
    `organizations.organization_code` and, since IRA-001A,
    `organization_establishment_attempts.organization_code`) as a
    second line of defense against a concurrent duplicate request.
  - observability.py's record_audit/publish_event/AuditStatus, exactly as
    bootstrap_service.py already uses them (SD-002-054's seven audit
    questions; RTA-001 §4.13 Domain Event Publication).
"""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.organization import Organization, OrganizationStatus
from models.organization_establishment_attempt import (
    DomainVerificationStatus,
    OrganizationEstablishmentAttempt,
)
from repositories.organization_repository import OrganizationRepository
from repositories.organization_establishment_attempt_repository import (
    OrganizationEstablishmentAttemptRepository,
)
from schemas.organization import UpdateOrganizationProfileRequest
from schemas.organization_establishment_attempt import (
    ActivateEstablishmentRequest,
    EstablishOrganizationAttemptRequest,
)
from observability import record_audit, publish_event, AuditStatus


class OrganizationService:
    """Business Activity orchestrator for Organization Management (WP-01)."""

    def __init__(
        self,
        organization_repo: OrganizationRepository,
        organization_establishment_attempt_repo: OrganizationEstablishmentAttemptRepository,
    ) -> None:
        self.organization_repo = organization_repo
        self.organization_establishment_attempt_repo = organization_establishment_attempt_repo

    async def establish(
        self, request: EstablishOrganizationAttemptRequest, actor_id: str | None = None
    ) -> OrganizationEstablishmentAttempt:
        """
        Business Activity: Establish Organization Identity (BA-01,
        amended per IRA-001A). Realizes ERB-C004-01's own Exit Context:
        produces an Organization Anchor Context holding a Candidate
        Organization Identity Context — explicitly NOT an Authoritative
        Organization Context (BR-C004-08). No `organizations` row is
        created here; see activate_establishment() (BA-01C) for the
        first, distinct, governed activation act that does.

        Business Rule: organization_code must be unique platform-wide —
        checked against BOTH `organizations` (already-activated
        identities) and `organization_establishment_attempts` (in-flight
        ones), since the two share one namespace (BR-C004-01's own
        "one Organization Anchor Context per establishment thread"
        implies no two threads, nor a thread and an activated identity,
        may claim the same code). Enforced both here, for a clean 409,
        and by the database's own uq_organization_establishment_
        attempts_organization_code constraint as a second line of
        defense against a concurrent duplicate request.
        """
        existing_organization = await self.organization_repo.get_by_code(request.organization_code)
        existing_attempt = await self.organization_establishment_attempt_repo.get_by_code(
            request.organization_code
        )
        if existing_organization is not None or existing_attempt is not None:
            record_audit(
                action="ESTABLISH_ORGANIZATION_ANCHOR",
                resource=f"organization:{request.organization_code}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization_code already exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An organization with code '{request.organization_code}' already exists.",
            )

        try:
            attempt = await self.organization_establishment_attempt_repo.create(
                {
                    "organization_code": request.organization_code,
                    "organization_name": request.organization_name,
                    "organization_type": request.organization_type,
                    "description": request.description,
                    "primary_domain": request.primary_domain,
                    "domain_verification_status": (
                        DomainVerificationStatus.NOT_CLAIMED.value
                        if request.primary_domain is None
                        else DomainVerificationStatus.UNVERIFIED.value
                    ),
                }
            )
            await self.organization_establishment_attempt_repo.session.flush()
        except IntegrityError:
            # Closes the race window between the pre-check above and this
            # insert: two concurrent requests for the same organization_code
            # can both pass the pre-check before either commits. The
            # database's unique constraint catches the second one here.
            await self.organization_establishment_attempt_repo.session.rollback()
            record_audit(
                action="ESTABLISH_ORGANIZATION_ANCHOR",
                resource=f"organization:{request.organization_code}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization_code already exists (concurrent creation)"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An organization with code '{request.organization_code}' already exists.",
            )

        record_audit(
            action="ESTABLISH_ORGANIZATION_ANCHOR",
            resource=f"organization_establishment_attempt:{attempt.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"organization_code": attempt.organization_code},
        )
        publish_event(
            "ORGANIZATION_ANCHOR_ESTABLISHED",
            {
                "organization_establishment_attempt_id": str(attempt.id),
                "organization_code": attempt.organization_code,
                "organization_name": attempt.organization_name,
                "organization_type": attempt.organization_type,
                "domain_verification_status": attempt.domain_verification_status,
            },
        )
        return attempt

    async def verify_domain_claim(
        self, attempt_id: UUID, verified: bool, actor_id: str | None = None
    ) -> OrganizationEstablishmentAttempt:
        """
        Business Activity: Verify Organization Domain Claim (BA-01B,
        new per IRA-001A). Realizes ERB-C004-02: records a domain-claim
        verification outcome as a distinct, traceable act (BR-C004-02) —
        never trusted downstream before this act occurs, never silently
        assumed. The actual proof-of-control mechanism (DNS/email token,
        etc.) is out of this Business Activity's scope, consistent with
        PE-001-C004's own licensing of the no-domain path as fully
        sufficient without one (TD, disclosed in IMP-REPORT-WP-01's
        IRA-001A section) — this Business Activity's job is only to make
        the verification decision distinct, authorized, audited, and
        traceable, which is what BR-C004-02/BR-C004-09 actually require.
        """
        attempt = await self.organization_establishment_attempt_repo.get_by_id(attempt_id)
        if attempt is None:
            record_audit(
                action="VERIFY_ORGANIZATION_DOMAIN_CLAIM",
                resource=f"organization_establishment_attempt:{attempt_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "establishment attempt not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization establishment attempt exists with id '{attempt_id}'.",
            )

        if attempt.activated_organization_id is not None:
            record_audit(
                action="VERIFY_ORGANIZATION_DOMAIN_CLAIM",
                resource=f"organization_establishment_attempt:{attempt.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "establishment attempt already activated"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization establishment attempt '{attempt_id}' is already activated.",
            )

        if attempt.primary_domain is None:
            record_audit(
                action="VERIFY_ORGANIZATION_DOMAIN_CLAIM",
                resource=f"organization_establishment_attempt:{attempt.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "no primary_domain was claimed at establishment"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Organization establishment attempt '{attempt_id}' claimed no primary_domain "
                    "— nothing to verify. Use the governed no-domain path at activation instead."
                ),
            )

        new_status = (
            DomainVerificationStatus.VERIFIED.value if verified else DomainVerificationStatus.UNVERIFIED.value
        )
        updated = await self.organization_establishment_attempt_repo.update(
            attempt_id, {"domain_verification_status": new_status}
        )
        await self.organization_establishment_attempt_repo.session.flush()

        record_audit(
            action="VERIFY_ORGANIZATION_DOMAIN_CLAIM",
            resource=f"organization_establishment_attempt:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"organization_code": updated.organization_code, "verified": verified},
        )
        publish_event(
            "ORGANIZATION_DOMAIN_CLAIM_VERIFICATION_RECORDED",
            {
                "organization_establishment_attempt_id": str(updated.id),
                "organization_code": updated.organization_code,
                "domain_verification_status": updated.domain_verification_status,
            },
        )
        return updated

    async def activate_establishment(
        self,
        attempt_id: UUID,
        request: ActivateEstablishmentRequest,
        actor_id: str | None = None,
    ) -> Organization:
        """
        Business Activity: Activate Organization, first-time (BA-01C,
        new per IRA-001A). Realizes ERB-C004-03: the first, distinct,
        governed act that produces the first Authoritative Organization
        Context for a given Organization Anchor Context (Contract 5.1,
        Contract 5.4) — the constitutional correction's own centerpiece.
        Lexically and semantically distinct from the pre-existing
        `POST /organizations/{id}/activate` (BA-05, ERB-C004-06), which
        continues to mean only reactivation of an already-Authoritative,
        SUSPENDED Organization and is untouched by this correction.

        Business Rule (BR-C004-01, Contract 5.4): may only proceed with
        either a VERIFIED domain claim, or an explicit
        no_domain_activation_reason supplied on this call — the governed
        no-domain activation decision itself, recorded as a fact
        (BR-C004-09), never silently assumed by the absence of a domain.

        On success: creates the first `organizations` row for this
        establishment attempt (status=ACTIVE, identical shape BA-01
        originally wrote), and links the attempt to it via
        activated_organization_id — the attempt is preserved in
        lineage (§1.17), never deleted.
        """
        attempt = await self.organization_establishment_attempt_repo.get_by_id(attempt_id)
        if attempt is None:
            record_audit(
                action="ACTIVATE_ORGANIZATION_ESTABLISHMENT",
                resource=f"organization_establishment_attempt:{attempt_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "establishment attempt not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization establishment attempt exists with id '{attempt_id}'.",
            )

        if attempt.activated_organization_id is not None:
            record_audit(
                action="ACTIVATE_ORGANIZATION_ESTABLISHMENT",
                resource=f"organization_establishment_attempt:{attempt.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "establishment attempt already activated"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization establishment attempt '{attempt_id}' is already activated.",
            )

        has_verified_domain = attempt.domain_verification_status == DomainVerificationStatus.VERIFIED.value
        no_domain_reason = (request.no_domain_activation_reason or "").strip() or None
        if not has_verified_domain and not no_domain_reason:
            record_audit(
                action="ACTIVATE_ORGANIZATION_ESTABLISHMENT",
                resource=f"organization_establishment_attempt:{attempt.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={
                    "reason": "activation preconditions not met",
                    "domain_verification_status": attempt.domain_verification_status,
                },
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Organization establishment attempt '{attempt_id}' has no VERIFIED domain claim "
                    "and no no_domain_activation_reason was supplied — cannot activate."
                ),
            )

        if no_domain_reason and not has_verified_domain:
            attempt = await self.organization_establishment_attempt_repo.update(
                attempt_id, {"no_domain_activation_reason": no_domain_reason}
            )

        try:
            organization = await self.organization_repo.create(
                {
                    "organization_code": attempt.organization_code,
                    "organization_name": attempt.organization_name,
                    "organization_type": attempt.organization_type,
                    "description": attempt.description,
                    "status": OrganizationStatus.ACTIVE.value,
                }
            )
            await self.organization_repo.session.flush()
        except IntegrityError:
            # Same defense-in-depth as BA-01's original establish() carried
            # — a concurrent activation racing against a code that has
            # since been taken directly in `organizations` (only possible
            # if two attempts' pre-checks both passed before either
            # committed, since organization_code is unique per attempt).
            await self.organization_repo.session.rollback()
            record_audit(
                action="ACTIVATE_ORGANIZATION_ESTABLISHMENT",
                resource=f"organization_establishment_attempt:{attempt.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization_code already exists (concurrent activation)"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An organization with code '{attempt.organization_code}' already exists.",
            )

        await self.organization_establishment_attempt_repo.update(
            attempt_id, {"activated_organization_id": organization.id}
        )
        await self.organization_establishment_attempt_repo.session.flush()

        record_audit(
            action="ACTIVATE_ORGANIZATION_ESTABLISHMENT",
            resource=f"organization:{organization.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_code": organization.organization_code,
                "organization_establishment_attempt_id": str(attempt.id),
                "no_domain_activation_reason": no_domain_reason,
            },
        )
        publish_event(
            "ORGANIZATION_ACTIVATED_FIRST_TIME",
            {
                "organization_id": str(organization.id),
                "organization_establishment_attempt_id": str(attempt.id),
                "organization_code": organization.organization_code,
                "status": organization.status,
            },
        )
        return organization

    async def get_details(self, organization_id: UUID) -> Organization:
        """
        Business Activity: View Organization Details.

        Read-only — no audit record or domain event, on the same basis
        already established for Person's read-side Business Activity
        (PersonRecognitionService.recognize does not audit either; only
        the write path, establish, does). Reuses BaseRepository.get_by_id
        via OrganizationRepository as-is — no new repository method
        required.
        """
        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization exists with id '{organization_id}'.",
            )
        return organization

    async def update_profile(
        self,
        organization_id: UUID,
        request: UpdateOrganizationProfileRequest,
        actor_id: str | None = None,
    ) -> Organization:
        """
        Business Activity: Update Organization Profile (BA-04).

        Preconditions: the organization must already exist (404 if not,
        same basis as get_details). Business Object Update touches only
        organization_name, organization_type, and description —
        organization_code and status (lifecycle) are out of this
        activity's scope (status belongs to the Activate/Suspend/Retire
        Business Activities, ADR-005). Note (TD-013, discovered during
        BA-07): this method does not itself check status — PE-001-C004's
        ERB-C004-05 restricts identity stewardship to ACTIVE organizations
        only, which this implementation does not yet enforce. Tracked as
        technical debt, not fixed here (would change this already-accepted
        Business Activity's behavior).
        """
        organization = await self.organization_repo.update(
            organization_id,
            {
                "organization_name": request.organization_name,
                "organization_type": request.organization_type,
                "description": request.description,
            },
        )
        if organization is None:
            record_audit(
                action="UPDATE_ORGANIZATION_PROFILE",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization exists with id '{organization_id}'.",
            )

        await self.organization_repo.session.flush()

        record_audit(
            action="UPDATE_ORGANIZATION_PROFILE",
            resource=f"organization:{organization.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"organization_code": organization.organization_code},
        )
        publish_event(
            "ORGANIZATION_PROFILE_UPDATED",
            {
                "organization_id": str(organization.id),
                "organization_code": organization.organization_code,
                "organization_name": organization.organization_name,
                "organization_type": organization.organization_type,
            },
        )
        return organization

    async def activate(self, organization_id: UUID, actor_id: str | None = None) -> Organization:
        """
        Business Activity: Activate Organization (BA-05).

        Interim lifecycle model (ADR-005): a plain `status` transition,
        not yet the metadata-driven state machine SD-002-051 ultimately
        requires. Business Rule: only a SUSPENDED organization may be
        activated. Activating an already-ACTIVE organization is rejected
        with 409 rather than silently succeeding as a no-op — this keeps
        the interim state machine's transitions explicit, mirroring
        establish()'s duplicate-rejection precedent rather than inventing
        a new idempotent-success convention with no canonical basis.

        Does not touch organization_name/organization_type/description
        (BA-04's scope) or organization_code (immutable natural key).

        TD-012 resolution (BA-06): also syncs the legacy `is_active`
        boolean to `True` so it no longer silently diverges from
        `status` — see suspend()'s matching sync in the opposite
        direction.

        BA-07 correctness fix: RETIRED (ERB-C004-07 per PE-001-C004) is a
        terminal state — "no ERB, EX, or tenant-configured policy in this
        specification permits reactivating a retired Organization." A
        RETIRED organization must be rejected here explicitly; without
        this check, introducing RETIRED as a new status value would
        silently make it reactivatable via this already-shipped endpoint,
        which is exactly the invariant PE-001-C004 forbids.
        """
        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            record_audit(
                action="ACTIVATE_ORGANIZATION",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization exists with id '{organization_id}'.",
            )

        if organization.status == OrganizationStatus.RETIRED.value:
            record_audit(
                action="ACTIVATE_ORGANIZATION",
                resource=f"organization:{organization.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization is RETIRED and cannot be reactivated", "organization_code": organization.organization_code},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization '{organization_id}' is RETIRED and cannot be reactivated.",
            )

        if organization.status == OrganizationStatus.ACTIVE.value:
            record_audit(
                action="ACTIVATE_ORGANIZATION",
                resource=f"organization:{organization.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization already ACTIVE", "organization_code": organization.organization_code},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization '{organization_id}' is already ACTIVE.",
            )

        previous_status = organization.status
        updated = await self.organization_repo.update(
            organization_id, {"status": OrganizationStatus.ACTIVE.value, "is_active": True}
        )
        await self.organization_repo.session.flush()

        record_audit(
            action="ACTIVATE_ORGANIZATION",
            resource=f"organization:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "new_status": updated.status,
            },
        )
        publish_event(
            "ORGANIZATION_ACTIVATED",
            {
                "organization_id": str(updated.id),
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "status": updated.status,
            },
        )
        return updated

    async def suspend(self, organization_id: UUID, actor_id: str | None = None) -> Organization:
        """
        Business Activity: Suspend Organization (BA-06).

        Interim lifecycle model (ADR-005): mirrors activate()'s pattern
        in the opposite direction. Business Rule: only an ACTIVE
        organization may be suspended. Suspending an already-SUSPENDED
        organization is rejected with 409, the same explicit-transition
        precedent activate() established for BA-06 to follow.

        Does not touch organization_name/organization_type/description
        (BA-04's scope) or organization_code (immutable natural key).

        TD-012 resolution: also syncs the legacy `is_active` boolean to
        `False`, closing the divergence risk BA-05 flagged — `is_active`
        and `status` now always move together for both transitions.

        BA-07 correctness fix: RETIRED (ERB-C004-07 per PE-001-C004) is
        terminal — a RETIRED organization must be rejected here explicitly
        for the same reason activate() rejects it (see that method's
        docstring); without this check, RETIRED would be silently
        reversible via this already-shipped endpoint.
        """
        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            record_audit(
                action="SUSPEND_ORGANIZATION",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization exists with id '{organization_id}'.",
            )

        if organization.status == OrganizationStatus.RETIRED.value:
            record_audit(
                action="SUSPEND_ORGANIZATION",
                resource=f"organization:{organization.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization is RETIRED and cannot be suspended", "organization_code": organization.organization_code},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization '{organization_id}' is RETIRED and cannot be suspended.",
            )

        if organization.status == OrganizationStatus.SUSPENDED.value:
            record_audit(
                action="SUSPEND_ORGANIZATION",
                resource=f"organization:{organization.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization already SUSPENDED", "organization_code": organization.organization_code},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization '{organization_id}' is already SUSPENDED.",
            )

        previous_status = organization.status
        updated = await self.organization_repo.update(
            organization_id, {"status": OrganizationStatus.SUSPENDED.value, "is_active": False}
        )
        await self.organization_repo.session.flush()

        record_audit(
            action="SUSPEND_ORGANIZATION",
            resource=f"organization:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "new_status": updated.status,
            },
        )
        publish_event(
            "ORGANIZATION_SUSPENDED",
            {
                "organization_id": str(updated.id),
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "status": updated.status,
            },
        )
        return updated

    async def retire(self, organization_id: UUID, actor_id: str | None = None) -> Organization:
        """
        Business Activity: Retire Organization & Preserve Continuity (BA-07).

        Realizes ERB-C004-07 (PE-001-C004): a terminal, irreversible
        lifecycle transition, the final Business Activity of WP-01 per
        the WP-01 Scope Reconciliation (IRA-001 §15 / this report's Scope
        Reconciliation section).

        Business Rule (Entry Context, PE-001-C004 §3.8): retirement may
        be entered from ACTIVE **or** SUSPENDED — both are canonically
        valid starting states, not only SUSPENDED. Only an already-RETIRED
        organization is rejected (409), the same explicit-transition
        precedent activate()/suspend() established.

        Preserves continuity: no row is deleted. organization_code,
        organization_name, organization_type, description, created_at,
        and the full audit trail all remain intact and queryable via
        get_details()/search() after retirement — only status (and the
        synced is_active) changes. This satisfies PE-001-C004's "SHALL
        NOT physically delete" requirement via the existing repository
        layer as-is; no new repository method or deletion path was
        introduced.

        Irreversibility is enforced at the *other* transition methods:
        activate() and suspend() both reject a RETIRED organization
        (see their docstrings) — this method does not need to guard
        against being reversed itself, since nothing transitions away
        from RETIRED.

        Known Limitation (documented, not implemented — deliberately out
        of this Business Activity's minimal scope, consistent with
        ADR-004's incremental-implementation philosophy; recorded as
        TD-014): PE-001-C004 also describes an optional Organization
        Continuity Context linking a retired Organization to a successor
        (EX-C004-13) and a persisted retirement reason/responsible-
        authority record. Neither is implemented here — no successor-
        organization relationship exists anywhere in the current schema,
        and no WP-01 consumer needs one yet. The reason/authority
        requirement is satisfied at the same level of rigor as every
        other lifecycle transition (BA-05/BA-06): captured in the audit
        record's actor_id/metadata via the existing observability
        mechanism, not a new persisted column.
        """
        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            record_audit(
                action="RETIRE_ORGANIZATION",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization exists with id '{organization_id}'.",
            )

        if organization.status == OrganizationStatus.RETIRED.value:
            record_audit(
                action="RETIRE_ORGANIZATION",
                resource=f"organization:{organization.id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization already RETIRED", "organization_code": organization.organization_code},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization '{organization_id}' is already RETIRED.",
            )

        previous_status = organization.status
        updated = await self.organization_repo.update(
            organization_id, {"status": OrganizationStatus.RETIRED.value, "is_active": False}
        )
        await self.organization_repo.session.flush()

        record_audit(
            action="RETIRE_ORGANIZATION",
            resource=f"organization:{updated.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "new_status": updated.status,
            },
        )
        publish_event(
            "ORGANIZATION_RETIRED",
            {
                "organization_id": str(updated.id),
                "organization_code": updated.organization_code,
                "previous_status": previous_status,
                "status": updated.status,
            },
        )
        return updated

    async def search(
        self,
        query: str | None,
        status_filter: str | None,
        skip: int,
        limit: int,
        sort_by: str,
        sort_order: str,
    ) -> tuple[Sequence[Organization], int]:
        """
        Business Activity: Search & List Organizations.

        Read-only, same basis as get_details — no audit record or domain
        event. Delegates filtering/sorting/counting entirely to
        OrganizationRepository.search(); this method's job is only to sit
        in the same Business Activity orchestration layer as establish()
        and get_details(), not to hold query logic itself (that stays in
        the repository, consistent with MembershipRepository's existing
        query methods).
        """
        return await self.organization_repo.search(
            query=query,
            status=status_filter,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
        )
