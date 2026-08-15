# schemas/discovery_provider.py
"""WP-14 BA-01 — Establish Discovery Provider Configuration (C-090). Request/response contracts (`IRA-014 §6` BA-01 row)."""
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

PROVIDER_CATEGORIES = ("ENTERPRISE", "EXTERNAL", "REALTIME")

# Category grouping per AMD-013's own literal CREATE TABLE structure
# (`Master_Technical_Architecture.md:3305-3309`) — three visually-grouped
# blocks within the single `provider_type` CHECK constraint, in the same
# declared order as `provider_category`'s own three values. The DB itself
# enforces no cross-column consistency (two independent CHECK constraints,
# not one combined one) — this mapping is an application-layer
# interpretation of the schema's own grouping, not a directly-stated
# business rule, disclosed here rather than silently assumed. It conflicts
# with `CANONICAL-ENTERPRISE-SEARCH-ARCHITECTURE-SPECIFICATION.md`'s own
# prose taxonomy (a self-disclosed "reconstruction only" document, which
# lumps EMAIL/EVENT_STREAM/IOT/SENSOR/MESSAGE_QUEUE into "ENTERPRISE") —
# the physical schema's own structure is treated as more authoritative.
PROVIDER_TYPES_BY_CATEGORY: dict[str, tuple[str, ...]] = {
    "ENTERPRISE": (
        "UPLOADED_DOCUMENT", "SHAREPOINT", "ONEDRIVE", "GOOGLE_DRIVE", "TEAMS", "SLACK", "CONFLUENCE",
        "JIRA", "SAP", "ORACLE", "SALESFORCE", "SERVICENOW", "SQL_DATABASE", "DATA_WAREHOUSE", "ENTERPRISE_API",
    ),
    "EXTERNAL": (
        "CORPORATE_WEBSITE", "ANNUAL_REPORT", "SUSTAINABILITY_REPORT", "REGULATORY_FILING",
        "GOVERNMENT_DATABASE", "STOCK_EXCHANGE_FILING", "STANDARDS_BODY", "PUBLIC_API", "INTERNET_SEARCH",
        "BENCHMARK_PROVIDER", "INDUSTRY_DATABASE",
    ),
    "REALTIME": ("EMAIL", "EVENT_STREAM", "IOT", "SENSOR", "MESSAGE_QUEUE"),
}
ALL_PROVIDER_TYPES = tuple(t for types in PROVIDER_TYPES_BY_CATEGORY.values() for t in types)
DISCOVERY_CADENCES = ("CONTINUOUS", "SCHEDULED", "ON_DEMAND")


class EstablishDiscoveryProviderRequest(BaseModel):
    """
    Request body for BA-01's own establish path. `provider_category` and
    `provider_type` must be mutually consistent per
    `PROVIDER_TYPES_BY_CATEGORY` (application-layer enforcement — the
    physical schema's own two CHECK constraints validate each column
    independently, not the cross-column combination, per this module's own
    disclosed mapping rationale above).
    """

    provider_name: str | None = Field(None, max_length=255)
    provider_category: str = Field(...)
    provider_type: str = Field(...)
    connection_config_json: dict[str, Any] | None = Field(
        None, description="Connector-specific configuration only — never credentials (use credential_id)."
    )
    credential_id: UUID | None = Field(
        None,
        description="Optional — api_credential_registry has no physical model in this repository yet; leave unset until it does.",
    )
    discovery_cadence: str = Field("ON_DEMAND")
    governing_policy_id: UUID | None = Field(
        None,
        description="Optional — confidence_scoring_registry has no physical model in this repository yet; leave unset until it does.",
    )
    platform_wide: bool = Field(
        False,
        description="PLATFORM_ADMIN only — establishes a platform-wide shared provider (organization_id NULL) rather than the caller's own tenant-dedicated provider.",
    )

    @field_validator("provider_category")
    @classmethod
    def _validate_category(cls, value: str) -> str:
        if value not in PROVIDER_CATEGORIES:
            raise ValueError(f"provider_category must be one of {PROVIDER_CATEGORIES}")
        return value

    @field_validator("provider_type")
    @classmethod
    def _validate_type(cls, value: str) -> str:
        if value not in ALL_PROVIDER_TYPES:
            raise ValueError(f"provider_type must be one of {ALL_PROVIDER_TYPES}")
        return value

    @field_validator("discovery_cadence")
    @classmethod
    def _validate_cadence(cls, value: str) -> str:
        if value not in DISCOVERY_CADENCES:
            raise ValueError(f"discovery_cadence must be one of {DISCOVERY_CADENCES}")
        return value

    @model_validator(mode="after")
    def _validate_category_type_consistency(self) -> "EstablishDiscoveryProviderRequest":
        allowed = PROVIDER_TYPES_BY_CATEGORY.get(self.provider_category, ())
        if self.provider_type not in allowed:
            raise ValueError(
                f"provider_type '{self.provider_type}' is not valid for provider_category "
                f"'{self.provider_category}' — expected one of {allowed}"
            )
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "provider_name": "Finance SharePoint",
                "provider_category": "ENTERPRISE",
                "provider_type": "SHAREPOINT",
                "discovery_cadence": "SCHEDULED",
                "platform_wide": False,
            }
        }
    }


class DiscoveryProviderResponse(BaseModel):
    """Result of BA-01's own establish path, and each row in its list path."""

    discovery_provider_id: UUID
    provider_name: str | None
    provider_category: str
    provider_type: str
    connection_config_json: dict[str, Any] | None
    credential_id: UUID | None
    discovery_cadence: str
    governing_policy_id: UUID | None
    active_flag: bool
    organization_id: UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DiscoveryProviderListResponse(BaseModel):
    """BA-01's own list path — every Discovery Provider configuration visible to the caller (their own tenant-dedicated rows plus platform-wide rows)."""

    discovery_providers: list[DiscoveryProviderResponse]
