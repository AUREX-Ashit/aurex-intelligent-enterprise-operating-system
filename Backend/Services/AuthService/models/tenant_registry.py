import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import CheckConstraint, String, DateTime, Integer, UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class TenantLifecycleState(str, Enum):
    """
    TDS-016 §10's own corrected, four-state lifecycle (PE-001-C040 §5.5,
    verbatim). No fifth "pending"/pre-provisioned state is added — a Tenant
    has no row in this table at all before the Establishment transaction
    (§8) commits; PROVISIONED is the first and only state a row is ever
    created in.
    """
    PROVISIONED = "PROVISIONED"
    MIGRATING = "MIGRATING"
    OFFBOARDING = "OFFBOARDING"
    OFFBOARDED = "OFFBOARDED"


class TenantRegistry(Base):
    """
    Realizes TDS-016 §5's schema remediation design for the Tenant system
    of record (ADR-034 §7, ADR-027's dedicated infrastructure domain).

    Deliberately does NOT carry every column `Master_Technical_Architecture.
    md`'s own `tenant_registry` draft lists (deployment_model, azure_region,
    azure_subscription_id, database_schema, storage_container_prefix,
    cache_key_prefix, encryption_key_reference, data_residency_country,
    tier, contract_start_date, contract_end_date, tenant_name) — every one
    of those is a Technical Provisioning Authority concern (`ADR-026 §13`),
    explicitly out of scope for this remediation (`TDS-016 §1`) and for the
    chartered minimum BA (Business Approval -> Infrastructure Allocation
    only). Adding empty placeholder columns for that still-undecided future
    authority would itself be designing scope this implementation is
    explicitly instructed not to invent. Only the columns TDS-016 §5/§8
    actually specifies — the corrected lifecycle/versioning/temporal
    columns and the two-authority actor/audit columns the Establishment
    transaction (§8) itself writes — are implemented here.

    Deliberately does NOT carry a back-reference `organization_id` column
    either (TDS-016 §5's own explicit, reasoned non-addition) — the
    Tenant<->Organization "exactly one" invariant is enforced by the
    atomic Establishment transaction (services/tenant_establishment_
    service.py) and by `organizations.tenant_id`'s own UNIQUE constraint,
    not by a second FK.
    """

    __tablename__ = "tenant_registry"
    __table_args__ = (
        CheckConstraint(
            "lifecycle_state IN ('PROVISIONED', 'MIGRATING', 'OFFBOARDING', 'OFFBOARDED')",
            name="ck_tenant_registry_lifecycle_state",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    """The Tenant's own canonical identity (referenced from organizations.tenant_id)."""

    tenant_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    """
    Deterministically set to the establishing Organization's own
    organization_code at Establishment time (TDS-016 §8 step 4 leaves the
    exact value an implementation-level choice; reusing organization_code
    avoids inventing a second, parallel naming scheme, and remains unique
    by construction under ADR-025's 1:1 cardinality).
    """

    lifecycle_state: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    """TenantLifecycleState. Always PROVISIONED at row creation (§8)."""

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        server_default="1",
    )
    """SD-002-010 Universal Versioning."""

    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    """SD-002-011 Canonical Temporal Model."""

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    approved_by_actor_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(),
        nullable=False,
    )
    """
    The Business Approval Authority's (AI-001) currently-appointed
    accountability point at the moment of Establishment — the live
    `authority_holders` row's own holder_person_id (TDS-016 §11,
    §8 step 2). Not a foreign key: authority_holders is a runtime
    projection that may later supersede this row (TDS-017 §23); this
    column is a point-in-time audit citation, not a live reference.
    """

    approved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    allocated_by_actor_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(),
        nullable=False,
    )
    """The Infrastructure Allocation Authority's (AI-002) accountability point that executed the transaction (TDS-016 §11)."""

    allocated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
