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

    No Business Activity anywhere establishes rows in this table today
    (TD-032): MDP-001 explicitly excludes `organization_node` from
    build-time seeding ("populate exclusively through real tenant
    onboarding and real business operation"), and no capability
    (C-005/Enterprise Structure Management has no IRA yet) currently
    owns an "Establish Organization Node" Business Activity. Rows exist
    only via direct creation until that capability is implemented.
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

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc)
    )
