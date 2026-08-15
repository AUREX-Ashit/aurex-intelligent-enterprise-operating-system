# models/discovery_provider.py
"""WP-14 BA-01 — Establish Discovery Provider Configuration (C-090 Enterprise Discovery). Physical schema per `Master_Technical_Architecture.md` AMD-013 (`discovery_provider_registry`, line 3301, LOCKED) — no column added, removed, or retyped beyond what AMD-013 itself specifies (`IRA-014 §6` BA-01 row).

`organization_id` mirrors `models/search.py::VectorIndexRegistryModel`'s own
precedent exactly: a plain, nullable UUID column, not a database-level
`ForeignKey` to `organization_master` (that table lives in `AuthService`'s
own database, a separate service boundary, `CLAUDE.md §8`). `NULL` means a
platform-wide shared provider; a set value means a tenant-dedicated one —
the identical RLS-backed shape AMD-013's own policy uses
(`org_isolation ON discovery_provider_registry USING (organization_id IS
NULL OR organization_id = current_setting('app.organization_id')::uuid)`,
`Master_Technical_Architecture.md:4587-4589`).

`credential_id`/`governing_policy_id` are declared nullable with no FK,
logical or physical — `api_credential_registry`/`confidence_scoring_registry`
are architecturally real (AMD-013/AMD-003) but have no physical Backend
model anywhere in this repository, the identical disposition BA-04 already
found for `confidence_rule_id` (`models/knowledge_asset.py`).

`active_flag` defaults `FALSE` per AMD-013's own literal schema text — not
`TRUE`, unlike `vector_index_registry` (WP-11 BA-01). No status-transition
endpoint is built by this Business Activity (not named by `IRA-014 §6`
BA-01's own row); a caller-established provider is retrievable and visible
via `GET /discovery-providers` regardless of `active_flag`, per that row's
own acceptance criterion ("it is retrievable") — filtering by `active_flag`
would otherwise make every freshly-established row invisible.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class DiscoveryProviderRegistryModel(Base):
    """
    `discovery_provider_registry` (AMD-013). One row per configured
    Enterprise Intelligence discovery source. Configuration only — no live
    connector is built or invoked by this Business Activity (`IRA-014
    §5.6`'s own explicit exclusion, connector protocols remain unbuilt for
    all 30 `provider_type` values).

    WP-14 BA-01 (Establish Discovery Provider Configuration) writes this
    table.
    """

    __tablename__ = "discovery_provider_registry"
    __table_args__ = (
        CheckConstraint(
            "provider_category IN ('ENTERPRISE', 'EXTERNAL', 'REALTIME')",
            name="ck_discovery_provider_registry_provider_category",
        ),
        CheckConstraint(
            "provider_type IN ("
            "'UPLOADED_DOCUMENT', 'SHAREPOINT', 'ONEDRIVE', 'GOOGLE_DRIVE', 'TEAMS', 'SLACK', 'CONFLUENCE', "
            "'JIRA', 'SAP', 'ORACLE', 'SALESFORCE', 'SERVICENOW', 'SQL_DATABASE', 'DATA_WAREHOUSE', 'ENTERPRISE_API', "
            "'CORPORATE_WEBSITE', 'ANNUAL_REPORT', 'SUSTAINABILITY_REPORT', 'REGULATORY_FILING', "
            "'GOVERNMENT_DATABASE', 'STOCK_EXCHANGE_FILING', 'STANDARDS_BODY', 'PUBLIC_API', 'INTERNET_SEARCH', "
            "'BENCHMARK_PROVIDER', 'INDUSTRY_DATABASE', "
            "'EMAIL', 'EVENT_STREAM', 'IOT', 'SENSOR', 'MESSAGE_QUEUE'"
            ")",
            name="ck_discovery_provider_registry_provider_type",
        ),
        CheckConstraint(
            "discovery_cadence IN ('CONTINUOUS', 'SCHEDULED', 'ON_DEMAND')",
            name="ck_discovery_provider_registry_discovery_cadence",
        ),
    )

    discovery_provider_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    provider_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provider_category: Mapped[str] = mapped_column(String(50), nullable=False)
    provider_type: Mapped[str] = mapped_column(String(100), nullable=False)
    connection_config_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    credential_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """AMD-013 logical FK to `api_credential_registry` — no physical model anywhere in this repository."""
    discovery_cadence: Mapped[str] = mapped_column(String(50), nullable=False, default="ON_DEMAND", server_default="ON_DEMAND")
    governing_policy_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """AMD-013 logical FK to `confidence_scoring_registry` — no physical model anywhere in this repository (same disposition as `knowledge_asset_registry.confidence_rule_id`)."""
    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    organization_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    """NULL for a platform-wide shared provider; set for a tenant-dedicated one (AMD-013). Logical, not physical, FK — see module docstring."""
