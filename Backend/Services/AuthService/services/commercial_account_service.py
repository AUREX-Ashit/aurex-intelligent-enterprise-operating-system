"""
C-022 Customer & Account Management — WP-21 BA-01, "Establish Commercial
Account". Realizes `TDS-C022`'s independently-reviewed design on the
single-table schema recorded at `TDS-C022 §6` (schema-shape STOP-and-report),
hosted in `AuthService` per `ROD-C022` D3.

Modeled directly on `OfferingDefinitionService.establish()` — the already-
certified platform-global establish pattern (no `organization_id`; every
mutation `require_platform_admin`-gated; `except IntegrityError -> rollback`
concurrent-duplicate handling; `record_audit` + `publish_event`). Reuses that
mechanism, not C-021's own business semantics (`ROD-C022 §H` governs what is
established here, not `COM-001 §6`).

Scope, per `ROD-C022` §H / `ROD-C022-A` D7-D8 / `ROD-C022-B` D9-D10 / the
WP-21 charter:
  * establish exactly one standalone Authoritative Commercial Account in
    `status = 'active'` only.
  * PLATFORM-GLOBAL — no `organization_id`, no tenant predicate. The
    authority boundary is `require_platform_admin` (`ROD-C022` D2/D3),
    enforced at the router; this service assumes an already-authorized
    PLATFORM_ADMIN caller.
  * NO `classification` attribute (`ADR-038` Option A).
  * NO read/list endpoint or method (`ROD-C022-A` D8) — this service exposes
    `establish` only.
  * EXCLUDED (never implemented here): Customer establishment, the
    Customer–Account Relationship, reclassification, retirement/
    reactivation, merge/split/transfer, Subscription (C-020), Billing
    (C-024), Contract (C-025), Entitlement (C-023), any CRM/Organization-
    equivalence/Identity/Person wiring.
  * Single-call establish is the accepted minimum-slice realization of
    `COM-001-002`/`COM-001-003`'s Anchor/Intent/Proposed/Assessment lifecycle
    pattern (`ROD-C022-B` D9, Option A) — this method itself is the entire
    realization; no additional internal stage is introduced.

`account_reference`: system-assigned via an application-level monotonic
allocator (`_next_account_reference`) — `MAX(suffix)+1`, formatted
`ACCOUNT-NNNNNN`, with the UNIQUE constraint as the concurrency backstop and
an allocate-and-retry on collision. No PostgreSQL SEQUENCE, mirroring O1's
own disposition for `offering_reference`.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models.c022_commercial_account import (
    ACCOUNT_REFERENCE_PREFIX as _ACCOUNT_REFERENCE_PREFIX,
)
from models.c022_commercial_account import C022CommercialAccount
from observability import AuditStatus, publish_event, record_audit
from repositories.c022_commercial_account_repository import (
    C022CommercialAccountRepository,
)
from schemas.commercial_account import EstablishCommercialAccountRequest

_ESTABLISH_ACTION = "ESTABLISH_COMMERCIAL_ACCOUNT"

_REFERENCE_ALLOCATION_MAX_RETRIES = 5


class CommercialAccountService:
    """Business Activity orchestrator for C-022 WP-21 BA-01."""

    def __init__(self, account_repo: C022CommercialAccountRepository) -> None:
        self.account_repo = account_repo

    # ------------------------------------------------------------------
    # Write path — establish (the only path BA-01 authorizes)
    # ------------------------------------------------------------------

    async def establish(
        self,
        request: EstablishCommercialAccountRequest,
        *,
        actor_id: str | None,
    ) -> C022CommercialAccount:
        """
        Establish one standalone Authoritative Commercial Account in
        `status = 'active'`. Produces the first Authoritative Commercial
        Account Context and its stable, system-assigned Account Reference
        (`ROD-C022` §H, `COM-001-036`).

        `account_reference` is allocated by `_next_account_reference`; on a
        UNIQUE collision (a concurrent establish taking the same number) the
        insert is rolled back and retried with a freshly allocated number,
        mirroring `OfferingDefinitionService.establish`'s own
        concurrent-duplicate handling.
        """
        actor_uuid = self._coerce_actor_id(actor_id)

        last_error: IntegrityError | None = None
        for _ in range(_REFERENCE_ALLOCATION_MAX_RETRIES):
            reference = await self._next_account_reference()
            now = datetime.now(timezone.utc)
            try:
                row = await self.account_repo.create(
                    {
                        "account_reference": reference,
                        "account_name": request.account_name,
                        "status": "active",
                        "parent_account_id": None,
                        "created_by_actor_id": actor_uuid,
                        "created_at": now,
                    }
                )
                await self.account_repo.session.flush()
                break
            except IntegrityError as exc:  # pragma: no cover - race backstop
                last_error = exc
                await self.account_repo.session.rollback()
                continue
        else:
            record_audit(
                action=_ESTABLISH_ACTION,
                resource="c022_commercial_account:allocation",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "account_reference allocation exhausted retries"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Could not allocate a unique Account Reference; retry the request.",
            ) from last_error

        record_audit(
            action=_ESTABLISH_ACTION,
            resource=f"c022_commercial_account:{row.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "account_id": str(row.id),
                "account_reference": row.account_reference,
                "account_name": row.account_name,
                "status": row.status,
            },
        )
        publish_event(
            "COMMERCIAL_ACCOUNT_ESTABLISHED",
            {
                "account_id": str(row.id),
                "account_reference": row.account_reference,
                "account_name": row.account_name,
                "status": row.status,
            },
        )
        return row

    # ------------------------------------------------------------------
    # Internal — Account Reference allocation
    # ------------------------------------------------------------------

    async def _next_account_reference(self) -> str:
        current_max = await self.account_repo.max_reference_sequence()
        return f"{_ACCOUNT_REFERENCE_PREFIX}-{current_max + 1:06d}"

    @staticmethod
    def _coerce_actor_id(actor_id: str | None) -> uuid.UUID:
        """
        The `created_by_actor_id` column is a UUID audit citation
        (`TDS-C022 §6.1`). An authenticated `PLATFORM_ADMIN` caller always
        carries a `person_id` claim; a token without one is malformed and
        fails closed here rather than writing a NULL actor.
        """
        if not actor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authenticated caller has no person_id claim.",
            )
        try:
            return uuid.UUID(str(actor_id))
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authenticated caller's person_id claim is not a valid UUID.",
            )
