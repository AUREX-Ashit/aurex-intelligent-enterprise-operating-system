import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.organization import Organization
    from models.person import Person


class ConfigurationScopeLevel(str, Enum):
    """
    CMD-001 §12.6 Scope Hierarchy, restricted to the tiers this repository
    can actually anchor today (IRA-010 §4.8/§6): Global Platform, Region,
    Country, Enterprise, Business Domain, and Business Object have no
    existing entity anywhere in this codebase to anchor an override to —
    the same disclosed limitation IRA-009/TD-032 already found for
    OrganizationNode. Global Platform is deliberately never a persisted
    row at all (see ConfigurationEntry's own docstring) — only TENANT and
    USER are persisted scope levels.

    USER is declared for schema completeness (mirrors
    AccessEvaluationOutcomeType's own precedent of declaring the full
    registered model even where the current Work Package's own code path
    writes only a subset) — WP-10's BA-02 (PLATFORM_ADMIN-gated
    establish/update) writes TENANT only; no self-service, non-admin
    establish flow for a User-level override is chartered by IRA-010.
    """
    TENANT = "TENANT"
    USER = "USER"


class ConfigurationFacet(str, Enum):
    """
    WP-10's own five in-scope facets (IRA-010 §4.8), each mapped to a
    CMD-001 §12.3 Configuration Category:

    - TERMINOLOGY -> Platform Configuration (closest-fit category; not
      separately named in §12.3's own examples, grounded instead in
      SD-002 §10 / SD-002-079 per IRA-010 §4.1).
    - BRANDING -> Platform Configuration (§12.3 example: "Branding").
      Core/single-logo only — dual-logo excluded (IRA-010 §4.3/§9).
    - THEME -> UI Configuration (§12.3 example: "Themes"). Light, Dark,
      High-Contrast, Boardroom — White-label excluded (IRA-010 §4.3).
    - ACCESSIBILITY -> UI Configuration (the accessibility-mode facet of
      the same DS-001 §11.3 Theme Model, SE-002).
    - LOCALIZATION -> Tenant Configuration (§12.3 example: "Default
      Language"). Default Language value only, not full i18n
      (IRA-010 §4.8).
    """
    TERMINOLOGY = "TERMINOLOGY"
    BRANDING = "BRANDING"
    THEME = "THEME"
    ACCESSIBILITY = "ACCESSIBILITY"
    LOCALIZATION = "LOCALIZATION"


class ConfigurationLifecycleState(str, Enum):
    """
    CMD-001 §12.5's mandatory Lifecycle State. ACTIVE -> SUPERSEDED (a
    newer version established) | RETIRED (explicitly withdrawn, no
    replacement). At most one ACTIVE row per (organization_id, person_id,
    facet, key) is enforced by ConfigurationService at write time (BA-02),
    not by a database constraint — SQLite (this repository's own test
    engine, tests/conftest.py) has no portable equivalent of the
    Postgres partial/functional unique index this would require,
    mirroring this repository's existing convention of enforcing
    single-active-row invariants at the service layer (e.g. Organization
    status, Access Evaluation Outcome validity_status transitions).
    """
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    RETIRED = "RETIRED"


class ConfigurationEntry(Base):
    """
    Configuration Entry (CFG-000001, WP-10 / C-041, ADR-019).

    A single resolved Configuration value at a specific point in the
    CMD-001 §12.6 Scope Hierarchy, for one of WP-10's five in-scope
    Configuration facets (ConfigurationFacet), identified by
    Scope + Facet + Key. Global Platform scope is never a persisted row
    — it is the implicit fallback (existing hardcoded defaults already in
    code / theme.css / copy) when no TENANT or USER override row is
    ACTIVE for a given Facet + Key, per CMD-001 §12.7's own "Platform
    Default -> ... -> User Override" resolution chain and IRA-010 §7's
    own disclosure that the empty state is "platform defaults render,"
    not a seeded database row.
    """

    __tablename__ = "configuration_entries"
    __table_args__ = (
        CheckConstraint(
            "scope_level IN ('TENANT', 'USER')",
            name="ck_configuration_entries_scope_level",
        ),
        CheckConstraint(
            "facet IN ('TERMINOLOGY', 'BRANDING', 'THEME', 'ACCESSIBILITY', 'LOCALIZATION')",
            name="ck_configuration_entries_facet",
        ),
        CheckConstraint(
            "lifecycle_state IN ('ACTIVE', 'SUPERSEDED', 'RETIRED')",
            name="ck_configuration_entries_lifecycle_state",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    """Every persisted row is at least Tenant-anchored — Global Platform scope is never persisted (see class docstring). CMD-001 §12.5's mandatory Tenant Scope characteristic."""

    person_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        nullable=True,
    )
    """Populated only for scope_level=USER. NULL for TENANT."""

    scope_level: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    facet: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    key: Mapped[str] = mapped_column(String(100), nullable=False)
    """The specific override key within facet — e.g. a Terminology term key ('role.ceo'), or 'logo_url' (Branding), 'theme_class' (Theme), 'high_contrast_enabled' (Accessibility), 'default_language' (Localization)."""

    value: Mapped[Any] = mapped_column(JSON, nullable=False)
    """Facet+key-shaped override payload. One flexible JSON column, not one column per facet's own payload shape, per SD-002-077's metadata-driven object pattern (IRA-010 §6's own registration-shape rationale)."""

    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    """CMD-001 §12.5's mandatory Versioning — monotonic increment per (organization_id, person_id, facet, key); the prior version's row is retained as SUPERSEDED, never deleted or overwritten in place."""

    lifecycle_state: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=ConfigurationLifecycleState.ACTIVE.value,
        server_default=ConfigurationLifecycleState.ACTIVE.value,
    )

    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    """Set when this row transitions to SUPERSEDED or RETIRED — CMD-001 §12.5's mandatory Effective Dating."""

    established_by_person_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("persons.id"),
        nullable=True,
    )
    """CMD-001 §12.5's mandatory Audit Trail — the PLATFORM_ADMIN caller who established this version (BA-02)."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization")
    person: Mapped["Person | None"] = relationship("Person", foreign_keys=[person_id])
