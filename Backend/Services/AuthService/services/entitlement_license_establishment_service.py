"""
C-023 Licensing & Entitlement — WP-17 BA-01, "Establish Entitlement/License
Context (Administrative)". Realizes `TDS-C023 §14`'s own atomic
Establishment transaction, on the two-table schema approved by the
Repository Owner at `TDS-C023-A §19.1` (D-1 … D-6).

Modeled directly on `MembershipService.establish()` / `TenantEstablishment
Service.establish()` — the already-certified establish pattern
(validate anchors -> verify authority before any write -> establish inside
one DB transaction -> `record_audit` -> catch `IntegrityError` ->
`rollback` -> 409). Approval Authority is enforced by the certified WP-18
mechanism (`require_approval_authority()` on the route; this service
additionally re-reads the authorizing `approval_authorities` row only to
record its id, never to re-decide). Nothing in `TDS-018` / WP-18 is
modified.

Decision 6 (`IRA-C023 §18.13`): `memberships.license_type` is read by
value only where a validation needs it and is never written, duplicated,
or persisted here (`TDS-C023-A §4`). BA-01 writes only `status = 'ACTIVE'`
and never closes a context (`TDS-C023-A §9.1`; Repository Owner D-5).
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status

from models.c023_entitlement_context import C023EntitlementContext
from models.c023_license_context import C023LicenseContext
from observability import AuditStatus, publish_event, record_audit
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.c023_entitlement_context_repository import C023EntitlementContextRepository
from repositories.c023_license_context_repository import C023LicenseContextRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from repositories.organization_repository import OrganizationRepository

# The C-023 Commit Authority instance name (`TDS-C023 §7.2`) — free text in
# `approval_authorities.authority_name`, no schema change.
COMMIT_AUTHORITY_NAME = "Entitlement/License Commit Authority"

# Default Entitlement Source Reference for an administrative (no-Subscription)
# grant — `TDS-C023-A §3.1` names `"ADMINISTRATIVE"` for exactly this case;
# `BR-C023-02` keeps it non-authoritative regardless.
_ADMINISTRATIVE_SOURCE_REFERENCE = "ADMINISTRATIVE"

# The four `URA-001-115` specialized C-023 license types — Repository Owner
# D-3. Mirrors the `ck_c023_license_context_license_type` CHECK; validated
# here too so the caller gets a 422 rather than a raw IntegrityError.
_SPECIALIZED_LICENSE_TYPES = frozenset(
    {"SUPPLIER", "AUDITOR", "BOARD_MEMBER", "CONSULTANT"}
)

# ---------------------------------------------------------------------------
# Recognized-Entitlement-Type source — the Decision 3 seam.
# ---------------------------------------------------------------------------
# BA-01 references an ALREADY-RECOGNIZED Entitlement Type only; it never
# creates, modifies, or governs one (`WP-17 §7`; `TDS-C023 §5-A`/`§19`;
# `IRA-C023 §21.12` Decision 3 — DEFERRED, not reopened, not implemented).
# The Global Entitlement Type / Feature Catalog (`URA-001-113` — "metadata
# driven … Aurex Admins create global entitlements") is that recognized-type
# source. It does not exist yet, and building it is explicitly EXCLUDED by
# the WP-17 Implementation Authorization (`IMP-REPORT-WP-17 §3`).
#
# This set is therefore deliberately EMPTY. Consequently the Entitlement
# half of BA-01 is *vacuously blocked* end-to-end — a disclosed practical
# consequence, not a defect (`IRA-C023 §21.6`; `TDS-C023 §9.3`/`§19`;
# `IMP-REPORT-WP-17 §5`). The License half is fully exercisable. Which
# identifiers (and in which form) constitute the interim recognized set for
# BA-01 — if any, before Decision 3 — is a scope question NOT resolved by
# `TDS-C023-A §19.1` D-1…D-7; it is raised to the Repository Owner as an
# implementation-time STOP-and-report rather than decided here
# (`CLAUDE.md §18`/`§19.4`; Authorization item 9).
_RECOGNIZED_ENTITLEMENT_TYPE_REFS: frozenset[str] = frozenset()


class EntitlementLicenseEstablishmentService:
    """Business Activity orchestrator for C-023 WP-17 BA-01."""

    def __init__(
        self,
        license_repo: C023LicenseContextRepository,
        entitlement_repo: C023EntitlementContextRepository,
        membership_repo: MembershipRepository,
        organization_repo: OrganizationRepository,
        domain_repo: DomainRepository,
        approval_authority_repo: ApprovalAuthorityRepository,
    ) -> None:
        self.license_repo = license_repo
        self.entitlement_repo = entitlement_repo
        self.membership_repo = membership_repo
        self.organization_repo = organization_repo
        self.domain_repo = domain_repo
        self.approval_authority_repo = approval_authority_repo

    async def establish(
        self,
        *,
        target_organization_id: UUID,
        actor_id: str | None,
        establish_license: bool,
        establish_entitlement: bool,
        membership_id: UUID | None = None,
        organization_id: UUID | None = None,
        domain_id: UUID | None = None,
        entitlement_type_ref: str | None = None,
        c023_license_type: str | None = None,
        entitlement_source_reference: str | None = None,
        effective_from: datetime | None = None,
        effective_to: datetime | None = None,
    ) -> tuple[C023LicenseContext | None, C023EntitlementContext | None]:
        """
        `TDS-C023 §14`'s six-step atomic transaction. `target_organization_id`
        is the `X-Tenant-ID`-derived Organization the route's
        `require_approval_authority(...)` dependency has already resolved
        Commit Authority against (`TDS-C023-A §6`) — a value independent of
        the caller's own claims. Returns `(license_row_or_None,
        entitlement_row_or_None)`.
        """
        if not establish_license and not establish_entitlement:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "Nothing to establish: supply a 'membership_id' (to establish a "
                    "License) and/or an 'organization_id' with 'entitlement_type_ref' "
                    "(to establish an Entitlement)."
                ),
            )

        now = datetime.now(timezone.utc)
        effective_from = effective_from or now
        if effective_to is not None and effective_to <= effective_from:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="'effective_to' must be after 'effective_from'.",
            )
        source_reference = entitlement_source_reference or _ADMINISTRATIVE_SOURCE_REFERENCE

        # ---- Step 2 (evaluated first, before any read of the anchors that
        # would let a caller probe existence): the authorizing
        # `approval_authorities` row. The route dependency already proved
        # the caller satisfies it; this re-read only obtains the row id to
        # record on each context (`TDS-C023 §5-A` "Authority reference").
        authority = await self.approval_authority_repo.get_active_by_organization_and_name(
            target_organization_id, COMMIT_AUTHORITY_NAME
        )
        if authority is None:
            # Only reachable on a race where the row was superseded between
            # the dependency's resolution and this read — fail closed.
            self._audit_denied(actor_id, target_organization_id, "commit authority no longer active")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"The '{COMMIT_AUTHORITY_NAME}' Approval Authority is no longer "
                    f"active for this Organization."
                ),
            )

        # ---- Step 1/3: validate anchors and tenant match (fail closed on a
        # cross-Organization anchor, mirroring
        # `MembershipApprovalAuthorityService.bind()`'s own rejection).
        proposed_license: dict | None = None
        proposed_entitlement: dict | None = None

        if establish_license:
            proposed_license = await self._validate_license_anchor(
                actor_id=actor_id,
                target_organization_id=target_organization_id,
                membership_id=membership_id,
                c023_license_type=c023_license_type,
            )

        if establish_entitlement:
            proposed_entitlement = await self._validate_entitlement_anchor(
                actor_id=actor_id,
                target_organization_id=target_organization_id,
                organization_id=organization_id,
                domain_id=domain_id,
                entitlement_type_ref=entitlement_type_ref,
            )

        # ---- Step 4: establish inside a single transaction.
        license_row: C023LicenseContext | None = None
        entitlement_row: C023EntitlementContext | None = None
        try:
            if proposed_license is not None:
                license_row = await self.license_repo.create(
                    {
                        "membership_id": proposed_license["membership_id"],
                        "status": "ACTIVE",
                        "effective_from": effective_from,
                        "effective_to": effective_to,
                        "entitlement_source_reference": source_reference,
                        "approval_authority_id": authority.id,
                        "committed_by_actor_id": UUID(actor_id),
                        "committed_at": now,
                        "c023_license_type": proposed_license["c023_license_type"],
                        "created_at": now,
                    }
                )
            if proposed_entitlement is not None:
                entitlement_row = await self.entitlement_repo.create(
                    {
                        "organization_id": proposed_entitlement["organization_id"],
                        "domain_id": proposed_entitlement["domain_id"],
                        "entitlement_type_ref": proposed_entitlement["entitlement_type_ref"],
                        "status": "ACTIVE",
                        "effective_from": effective_from,
                        "effective_to": effective_to,
                        "entitlement_source_reference": source_reference,
                        "approval_authority_id": authority.id,
                        "committed_by_actor_id": UUID(actor_id),
                        "committed_at": now,
                        "created_at": now,
                    }
                )
            await self.license_repo.session.flush()
        except _integrity_errors() as exc:
            # ---- Step 6: a concurrent establish won the race between our
            # pre-check and this flush; the partial unique index rejected
            # the duplicate current context. Roll back the whole
            # transaction, mirroring `MembershipService.establish()`.
            await self.license_repo.session.rollback()
            self._audit_denied(
                actor_id, target_organization_id,
                "duplicate current Authoritative context (concurrent establish)",
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "A current Authoritative Entitlement/License Context already exists "
                    "for this anchor (concurrent establishment)."
                ),
            ) from exc

        # ---- Step 5: audit every established context.
        if license_row is not None:
            self._audit_established(
                actor_id=actor_id,
                target_organization_id=target_organization_id,
                kind="LICENSE",
                context_id=license_row.id,
                authority_id=authority.id,
                anchor={"membership_id": str(license_row.membership_id)},
                detail={
                    "c023_license_type": license_row.c023_license_type,
                    "effective_from": license_row.effective_from.isoformat(),
                    "effective_to": license_row.effective_to.isoformat() if license_row.effective_to else None,
                    "status": license_row.status,
                    "entitlement_source_reference": license_row.entitlement_source_reference,
                },
            )
        if entitlement_row is not None:
            self._audit_established(
                actor_id=actor_id,
                target_organization_id=target_organization_id,
                kind="ENTITLEMENT",
                context_id=entitlement_row.id,
                authority_id=authority.id,
                anchor={
                    "organization_id": str(entitlement_row.organization_id),
                    "domain_id": str(entitlement_row.domain_id) if entitlement_row.domain_id else None,
                    "entitlement_type_ref": entitlement_row.entitlement_type_ref,
                },
                detail={
                    "effective_from": entitlement_row.effective_from.isoformat(),
                    "effective_to": entitlement_row.effective_to.isoformat() if entitlement_row.effective_to else None,
                    "status": entitlement_row.status,
                    "entitlement_source_reference": entitlement_row.entitlement_source_reference,
                },
            )

        return license_row, entitlement_row

    # ------------------------------------------------------------------
    # Read path — "display the resulting establishment/status outcome"
    # (authorized frontend item 2, `TDS-C023 §17.2`).
    # ------------------------------------------------------------------

    async def get_context_for_tenant(
        self, context_id: UUID, target_organization_id: UUID
    ) -> tuple[str, C023LicenseContext | C023EntitlementContext]:
        """
        Return `("LICENSE" | "ENTITLEMENT", row)` for `context_id`, but only
        if the row belongs to `target_organization_id` (the caller's
        `X-Tenant-ID` Organization). A cross-Organization id yields 404 —
        never a 403 that would confirm the row exists in another tenant
        (`TDS-C023-A §6`/`§15`). PK UUIDs are globally unique, so a given id
        is in at most one of the two tables.
        """
        license_row = await self.license_repo.get_by_id(context_id)
        if license_row is not None:
            membership = await self.membership_repo.get_by_id(license_row.membership_id)
            if membership is not None and membership.organization_id == target_organization_id:
                return "LICENSE", license_row
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such context.")

        entitlement_row = await self.entitlement_repo.get_by_id(context_id)
        if entitlement_row is not None:
            if entitlement_row.organization_id == target_organization_id:
                return "ENTITLEMENT", entitlement_row
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such context.")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such context.")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _validate_license_anchor(
        self,
        *,
        actor_id: str | None,
        target_organization_id: UUID,
        membership_id: UUID | None,
        c023_license_type: str | None,
    ) -> dict:
        if membership_id is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="'membership_id' is required to establish a License.",
            )
        if c023_license_type is not None and c023_license_type not in _SPECIALIZED_LICENSE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "'c023_license_type' must be one of "
                    f"{sorted(_SPECIALIZED_LICENSE_TYPES)} (the four URA-001-115 specialized "
                    "types) or omitted. It is NOT the FULL/LIGHT base classification "
                    "(that stays on the Membership, C-007-owned)."
                ),
            )

        membership = await self.membership_repo.get_by_id(membership_id)
        if membership is None:
            self._audit_denied(actor_id, target_organization_id, "membership not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Membership exists with id '{membership_id}'.",
            )
        if membership.organization_id != target_organization_id:
            # Cross-Organization anchor — fail closed (`TDS-C023-A §6` point 2).
            self._audit_denied(actor_id, target_organization_id, "membership belongs to a different Organization")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Membership '{membership_id}' belongs to a different Organization "
                    f"than the X-Tenant-ID this request is scoped to."
                ),
            )

        existing = await self.license_repo.get_current_for_membership(membership_id)
        if existing is not None:
            self._audit_denied(actor_id, target_organization_id, "duplicate current License Context")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"A current Authoritative License Context already exists for "
                    f"Membership '{membership_id}' (INV-C023-10)."
                ),
            )
        return {"membership_id": membership_id, "c023_license_type": c023_license_type}

    async def _validate_entitlement_anchor(
        self,
        *,
        actor_id: str | None,
        target_organization_id: UUID,
        organization_id: UUID | None,
        domain_id: UUID | None,
        entitlement_type_ref: str | None,
    ) -> dict:
        if organization_id is None or not entitlement_type_ref:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="'organization_id' and 'entitlement_type_ref' are both required to establish an Entitlement.",
            )
        if organization_id != target_organization_id:
            self._audit_denied(actor_id, target_organization_id, "entitlement organization_id != X-Tenant-ID")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="'organization_id' must equal the X-Tenant-ID this request is scoped to.",
            )

        # Decision 3 seam — see `_RECOGNIZED_ENTITLEMENT_TYPE_REFS`.
        if entitlement_type_ref not in _RECOGNIZED_ENTITLEMENT_TYPE_REFS:
            self._audit_denied(actor_id, target_organization_id, f"entitlement type not recognized: {entitlement_type_ref}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    f"Entitlement Type '{entitlement_type_ref}' is not a recognized "
                    "Entitlement Type. BA-01 references already-recognized Entitlement "
                    "Types only and never creates one. The Global Entitlement Type / "
                    "Feature Catalog (URA-001-113; IRA-C023 Decision 3) is deferred and "
                    "not implemented, so no Entitlement Type is recognized yet — the "
                    "Entitlement half of this Business Activity is vacuously blocked "
                    "(IRA-C023 §21.6; TDS-C023 §9.3). The License half is unaffected."
                ),
            )

        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            self._audit_denied(actor_id, target_organization_id, "organization not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Organization exists with id '{organization_id}'.",
            )
        if domain_id is not None:
            domain = await self.domain_repo.get_by_id(domain_id)
            if domain is None:
                self._audit_denied(actor_id, target_organization_id, "domain not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No Domain exists with id '{domain_id}'.",
                )

        existing = await self.entitlement_repo.get_current_for_anchor(
            organization_id, domain_id, entitlement_type_ref
        )
        if existing is not None:
            self._audit_denied(actor_id, target_organization_id, "duplicate current Entitlement Context")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "A current Authoritative Entitlement Context already exists for this "
                    "Entitlement Anchor and type (INV-C023-09)."
                ),
            )
        return {
            "organization_id": organization_id,
            "domain_id": domain_id,
            "entitlement_type_ref": entitlement_type_ref,
        }

    def _audit_denied(self, actor_id: str | None, organization_id: UUID, reason: str) -> None:
        record_audit(
            action="ESTABLISH_ENTITLEMENT_LICENSE_CONTEXT",
            resource=f"organization:{organization_id}",
            status=AuditStatus.DENIED,
            actor_id=actor_id or "SYSTEM",
            tenant_id=str(organization_id),
            metadata={"reason": reason},
        )

    def _audit_established(
        self,
        *,
        actor_id: str | None,
        target_organization_id: UUID,
        kind: str,
        context_id: UUID,
        authority_id: UUID,
        anchor: dict,
        detail: dict,
    ) -> None:
        record_audit(
            action="ESTABLISH_ENTITLEMENT_LICENSE_CONTEXT",
            resource=f"c023_{kind.lower()}_context:{context_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            tenant_id=str(target_organization_id),
            metadata={
                "kind": kind,
                "context_id": str(context_id),
                "approval_authority_id": str(authority_id),
                "organization_id": str(target_organization_id),
                "anchor": anchor,
                **detail,
            },
        )
        publish_event(
            "ENTITLEMENT_LICENSE_CONTEXT_ESTABLISHED",
            {
                "kind": kind,
                "context_id": str(context_id),
                "organization_id": str(target_organization_id),
                "anchor": anchor,
                "status": detail.get("status"),
            },
        )


def _integrity_errors() -> tuple[type[BaseException], ...]:
    """
    The exception set a partial-unique-index violation surfaces as —
    `sqlalchemy.exc.IntegrityError` on both PostgreSQL (asyncpg) and the
    SQLite test harness. Isolated for readability, mirroring
    `MembershipService.establish()`'s own `except IntegrityError`.
    """
    from sqlalchemy.exc import IntegrityError

    return (IntegrityError,)
