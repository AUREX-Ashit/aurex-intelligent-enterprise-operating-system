"""
C-040 Tenant Administration — Tenant Establishment (chartered minimum BA,
Repository Owner Decision 2026-08-26: "Tenant Establishment only —
Business Approval -> Infrastructure Allocation"). Realizes TDS-016 §8's
own atomic Establishment transaction exactly, using this repository's
own established Business Activity conventions (record_audit/publish_event,
duplicate-check-then-create, IntegrityError/rowcount-based race defense —
mirrored from services/organization_service.py's establish()/
activate_establishment()).

Explicitly out of scope, per TDS-016 §1 and the implementation
authorization's own boundaries: Technical Provisioning, migration,
offboarding, cross-tenant sharing — none of those lifecycle transitions
or their triggering authorities are implemented here.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status

from models.tenant_registry import TenantLifecycleState, TenantRegistry
from repositories.authority_holder_repository import AuthorityHolderRepository
from repositories.organization_repository import OrganizationRepository
from repositories.tenant_registry_repository import TenantRegistryRepository
from observability import record_audit, publish_event, AuditStatus

_AI001 = "AI-001"
_AI002 = "AI-002"


class TenantEstablishmentService:
    """Business Activity orchestrator for C-040 Tenant Establishment."""

    def __init__(
        self,
        organization_repo: OrganizationRepository,
        tenant_registry_repo: TenantRegistryRepository,
        authority_holder_repo: AuthorityHolderRepository,
    ) -> None:
        self.organization_repo = organization_repo
        self.tenant_registry_repo = tenant_registry_repo
        self.authority_holder_repo = authority_holder_repo

    async def establish(self, organization_id: UUID, actor_id: str | None = None) -> tuple[TenantRegistry, UUID]:
        """
        TDS-016 §8's own six-step atomic transaction:

          1. Verify caller is the currently-appointed AI-002 accountability
             point — enforced by the router's own require_ai002_holder
             dependency, before this method is ever called (TDS-016 §12,
             "the service itself enforces step 1 — it does not accept an
             unauthenticated or self-asserted claim").
          2. Verify a valid, referenced Business Approval decision exists
             for this Organization — realized here as a live lookup of
             AI-001's own currently-ACTIVE authority_holders row. No
             separate persisted "Business Approval decision" table is
             designed by TDS-016 §5; §11 confirms both actor attributions
             are written together, in this same atomic transaction, not
             read back from an earlier record. This is the implementation-
             level design choice TDS-016 §8's own preamble authorizes
             ("everything below is... not a constitutional requirement").
          3. Verify organization_master.tenant_id IS NULL for this
             Organization — the idempotency/duplicate-establishment guard.
          4. INSERT tenant_registry (PROVISIONED, version 1, both actor
             attributions).
          5/6. Conditional UPDATE organizations.tenant_id, guarded by
             tenant_id IS NULL; zero rows affected -> full rollback,
             including step 4's INSERT (a concurrent transaction won the
             race first).

        Returns (tenant_row, organization_id) — the router builds the
        response from both, since TenantRegistry deliberately carries no
        organization_id column (TDS-016 §5).
        """
        organization = await self.organization_repo.get_by_id(organization_id)
        if organization is None:
            record_audit(
                action="ESTABLISH_TENANT",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "organization not found"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Organization exists with id '{organization_id}'.",
            )

        if organization.tenant_id is not None:
            record_audit(
                action="ESTABLISH_TENANT",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "tenant already established", "tenant_id": str(organization.tenant_id)},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization '{organization_id}' already has an established Tenant.",
            )

        business_approval_holder = await self.authority_holder_repo.get_active_by_authority(_AI001)
        if business_approval_holder is None:
            record_audit(
                action="ESTABLISH_TENANT",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "no currently-appointed AI-001 accountability point exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "No currently-appointed AI-001 (Business Approval Authority) accountability "
                    "point exists — a Business Approval decision cannot be attributed."
                ),
            )

        if not actor_id:
            # Structurally unreachable via the router: require_ai002_holder
            # itself 403s before this method is ever called unless
            # claims["person_id"] is populated. Defensive only.
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This operation requires the currently appointed AI-002 accountability point.",
            )

        now = datetime.now(timezone.utc)
        tenant = await self.tenant_registry_repo.create(
            {
                "tenant_code": organization.organization_code,
                "lifecycle_state": TenantLifecycleState.PROVISIONED.value,
                "version": 1,
                "effective_from": now,
                "approved_by_actor_id": business_approval_holder.holder_person_id,
                "approved_at": now,
                "allocated_by_actor_id": UUID(actor_id),
                "allocated_at": now,
                "created_at": now,
            }
        )
        await self.tenant_registry_repo.session.flush()

        affected = await self.organization_repo.establish_tenant_if_unset(organization_id, tenant.id)
        if affected == 0:
            # Lost the race: another transaction established this
            # Organization's Tenant between our own pre-check above and
            # this UPDATE. Roll back the whole transaction, including the
            # tenant_registry INSERT just flushed (TDS-016 §8 step 6).
            await self.tenant_registry_repo.session.rollback()
            record_audit(
                action="ESTABLISH_TENANT",
                resource=f"organization:{organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "tenant already established (concurrent establishment)"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization '{organization_id}' already has an established Tenant.",
            )

        record_audit(
            action="ESTABLISH_TENANT",
            resource=f"tenant:{tenant.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_id": str(organization_id),
                "tenant_code": tenant.tenant_code,
                "approved_by_actor_id": str(business_approval_holder.holder_person_id),
            },
        )
        publish_event(
            "TENANT_ESTABLISHED",
            {
                "tenant_id": str(tenant.id),
                "organization_id": str(organization_id),
                "tenant_code": tenant.tenant_code,
                "lifecycle_state": tenant.lifecycle_state,
            },
        )
        return tenant, organization_id
