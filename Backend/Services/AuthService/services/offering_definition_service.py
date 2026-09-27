"""
C-021 Product & Service Catalog — WP-20 BA-01, "Establish / Manage Offering
Definition". Realizes `TDS-C021`'s independently-reviewed design on the
single-table schema recorded at `TDS-C021 §9` (schema-shape STOP-and-report),
hosted in `AuthService` per the Repository Owner's own `TDS-C021 §5` Option A
decision, as amended by Repository Owner decisions O1 (identity generation is
a set of acceptance properties, not a mandated PostgreSQL SEQUENCE) and O2
(`category_ref` is OPTIONAL / NULLABLE).

Modeled directly on `RoleService.establish()` — the already-certified
platform-global establish pattern (`roles` has no `organization_id`; every
mutation `require_platform_admin`-gated; `except IntegrityError -> rollback`
concurrent-duplicate handling; `record_audit` + `publish_event`).

Scope, per `ROD-C021` D1–D8 / the WP-20 charter:
  * establish / list / read a standalone Atomic Offering Definition in
    `state = 'draft'` only.
  * PLATFORM-GLOBAL — no `organization_id`, no tenant predicate. The
    authority boundary is `require_platform_admin` (`ROD-C021` D8), enforced
    at the router; this service assumes an already-authorized PLATFORM_ADMIN
    caller.
  * EXCLUDED (never implemented here): composition, relationships,
    publication, retirement, any state transition, pricing computation,
    availability, Subscription, Customer/Account, Entitlement/Feature
    semantics (C-023 Decision 3 untouched), Billing, Contract, taxonomy
    governance, tenant overlays.

`offering_reference` (O1): system-assigned via an application-level monotonic
allocator (`_next_offering_reference`) — `MAX(suffix)+1`, formatted
`OFFERING-NNNNNN`, with the UNIQUE constraint as the concurrency backstop and
an allocate-and-retry on collision. No PostgreSQL SEQUENCE. If a future
increment needs a stronger allocator that requires a new DB object, that goes
through a separate `CLAUDE.md §18`/`§19.4` change-control pass.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models.c021_offering_definition import (
    OFFERING_REFERENCE_PREFIX as _OFFERING_REFERENCE_PREFIX,
)
from models.c021_offering_definition import C021OfferingDefinition
from observability import AuditStatus, publish_event, record_audit
from repositories.c021_offering_definition_repository import (
    C021OfferingDefinitionRepository,
)
from schemas.offering import EstablishOfferingDefinitionRequest

_ESTABLISH_ACTION = "ESTABLISH_OFFERING_DEFINITION"

# `COM-001-001` Universal Identity prefix for the Offering Definition
# Business Object. The `PREFIX-NNNNNN` shape is mandated by `COM-001-001`;
# the exact token is aligned with the CBOR Business Object registration
# (`ADR-037`). 6-digit zero-padded suffix. Single source of truth is
# `models.c021_offering_definition.OFFERING_REFERENCE_PREFIX` — the
# repository's `max_reference_sequence` derives a fixed string offset from
# the same constant, so the two must never drift apart.
_REFERENCE_ALLOCATION_MAX_RETRIES = 5


class OfferingDefinitionService:
    """Business Activity orchestrator for C-021 WP-20 BA-01."""

    def __init__(self, offering_repo: C021OfferingDefinitionRepository) -> None:
        self.offering_repo = offering_repo

    # ------------------------------------------------------------------
    # Write path — establish
    # ------------------------------------------------------------------

    async def establish(
        self,
        request: EstablishOfferingDefinitionRequest,
        *,
        actor_id: str | None,
    ) -> C021OfferingDefinition:
        """
        Establish one standalone Atomic Offering Definition in `state =
        'draft'`. Produces the first Authoritative Offering Definition Context
        and its stable, system-assigned Offering Reference (`ROD-C021` D4).

        `offering_reference` is allocated by `_next_offering_reference`; on a
        UNIQUE collision (a concurrent establish taking the same number) the
        insert is rolled back and retried with a freshly allocated number,
        mirroring `RoleService.establish`'s own concurrent-duplicate
        handling. This satisfies O1's "concurrency-safe" property without a
        PostgreSQL SEQUENCE.
        """
        actor_uuid = self._coerce_actor_id(actor_id)

        last_error: IntegrityError | None = None
        for _ in range(_REFERENCE_ALLOCATION_MAX_RETRIES):
            reference = await self._next_offering_reference()
            now = datetime.now(timezone.utc)
            try:
                row = await self.offering_repo.create(
                    {
                        "offering_reference": reference,
                        "offering_name": request.offering_name,
                        "offering_kind": request.offering_kind,
                        "category_ref": request.category_ref,
                        "list_price_reference": request.list_price_reference,
                        "state": "draft",
                        "version": 1,
                        "supersedes_id": None,
                        "created_by_actor_id": actor_uuid,
                        "created_at": now,
                    }
                )
                await self.offering_repo.session.flush()
                break
            except IntegrityError as exc:  # pragma: no cover - race backstop
                last_error = exc
                await self.offering_repo.session.rollback()
                continue
        else:
            record_audit(
                action=_ESTABLISH_ACTION,
                resource="c021_offering_definition:allocation",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "offering_reference allocation exhausted retries"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Could not allocate a unique Offering Reference; retry the request.",
            ) from last_error

        record_audit(
            action=_ESTABLISH_ACTION,
            resource=f"c021_offering_definition:{row.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "offering_id": str(row.id),
                "offering_reference": row.offering_reference,
                "offering_kind": row.offering_kind,
                "category_ref": row.category_ref,
                "list_price_reference": row.list_price_reference,
                "state": row.state,
            },
        )
        publish_event(
            "OFFERING_DEFINITION_ESTABLISHED",
            {
                "offering_id": str(row.id),
                "offering_reference": row.offering_reference,
                "offering_name": row.offering_name,
                "offering_kind": row.offering_kind,
                "state": row.state,
            },
        )
        return row

    # ------------------------------------------------------------------
    # Read path — list / read
    # ------------------------------------------------------------------

    async def list_offerings(self) -> list[C021OfferingDefinition]:
        """Every Offering Definition in the one platform-global catalog, newest first (`ROD-C021` D4/D8)."""
        rows = await self.offering_repo.list_all()
        return list(rows)

    async def get_offering(self, offering_id) -> C021OfferingDefinition:
        """One Offering Definition by id. Unknown id -> 404 (`TDS-C021 §13`)."""
        row = await self.offering_repo.get_by_id(offering_id)
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Offering Definition exists with id '{offering_id}'.",
            )
        return row

    # ------------------------------------------------------------------
    # Internal — Offering Reference allocation (O1)
    # ------------------------------------------------------------------

    async def _next_offering_reference(self) -> str:
        current_max = await self.offering_repo.max_reference_sequence()
        return f"{_OFFERING_REFERENCE_PREFIX}-{current_max + 1:06d}"

    @staticmethod
    def _coerce_actor_id(actor_id: str | None) -> uuid.UUID:
        """
        The `created_by_actor_id` column is a UUID audit citation
        (`TDS-C021 §9.1`). An authenticated `PLATFORM_ADMIN` caller always
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
