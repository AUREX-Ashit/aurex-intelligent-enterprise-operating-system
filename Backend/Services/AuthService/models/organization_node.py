import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class OrganizationNode(Base):
    """
    Organization Node — WP-03 BA-01's minimal, disclosed subset of
    Master Technical Architecture's canonical `organization_node`
    (ERG-001-02/03's EnterpriseNode), realizing the home-node anchor
    URA-001-17b requires every Membership to declare.

    Deliberately minimal, mirroring ADR-004's own precedent for
    `organizations` vs. `organization_master`: the canonical
    `organization_node` carries ~20 further columns (legal_entity_name,
    business_unit, sector, geography_id, materiality/risk scores,
    ESG passport flags, etc.) that belong to Enterprise Structure
    Management (C-005)'s own future scope, not Membership Management's.
    Only the columns a home-node reference itself needs are implemented
    here (TD-032); the remaining canonical columns are deferred, not
    silently omitted.

    `organization_hierarchy` (parent/child relationships) is a
    deliberately separate table per Master Technical Architecture's own
    note ("Hierarchy intentionally separated from organization_node")
    and is out of BA-01's own scope entirely — no hierarchy concept is
    modeled here.

    WP-04 BA-01 (Establish Organization Node, ERB-C005-01/EX-C005-01/02
    per PE-001-C005, IRA-004 §9/§11) extends this WP-03-era minimal
    table with `legal_entity_name`, `business_unit`, `sector` and
    `operational_status` — the Structural Identity subset of Master
    Technical Architecture's canonical `organization_node` DDL
    (ERG-001-02's "Structural Identity" extension context). The
    remaining canonical columns (geography_id, parent_available_flag,
    and the materiality/risk/scenario/passport scores) are deferred,
    not silently omitted — see TD-043/TD-044.
    """

    __tablename__ = "organization_nodes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    node_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    node_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    node_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    """Free-text per Master Technical Architecture's own shape (e.g. holding/region/entity/site/supplier/JV) — not a closed enum; the canonical DDL does not constrain this to a fixed value set."""

    active_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    legal_entity_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    business_unit: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    sector: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    operational_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )
    """Free-text per Master Technical Architecture's own DDL comment ('active/inactive/divested') — not a closed enum, mirroring `node_type`'s own treatment. Deliberately independent of `active_flag` (TD-044): reconciling the two into a single authoritative lifecycle field is deferred, not assumed here."""

    effective_from: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    """`DateTime`, not the canonical DDL's literal `VARCHAR(255)` — a deliberate departure disclosed in IRA-004 §5/§11, mirroring `memberships.effective_from`/`effective_to`'s own established `DateTime(timezone=True)` shape (WP-03 BA-01) rather than reproducing an inconsistent column type."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc)
    )
