from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from models.configuration_entry import ConfigurationFacet


class ConfigurationSource(str, Enum):
    """
    Where a resolved value in BA-01's own response came from — the
    CMD-001 §12.7 Resolution Rules tier that won for this key. Not
    persisted anywhere (nothing about "where a value came from" is
    itself stored — it is computed fresh on every resolve), unlike
    ConfigurationScopeLevel/ConfigurationFacet/ConfigurationLifecycleState
    in models/configuration_entry.py, which back real columns.
    """
    USER = "USER"
    TENANT = "TENANT"
    PLATFORM_DEFAULT = "PLATFORM_DEFAULT"


class ResolvedConfigurationValue(BaseModel):
    """
    One resolved key within one facet (BA-01, EX-C041-01). `source`
    names which CMD-001 §12.6 Scope Hierarchy tier actually produced
    `value` — never silently hides that a Platform Default was used
    (IRA-010 §7's own disclosed empty-state: "platform defaults render").
    """
    key: str
    value: Any
    source: ConfigurationSource
    version: int | None = Field(None, description="Populated only when source is USER or TENANT — the established version number.")

    model_config = {"from_attributes": True}


class ResolvedConfigurationBundle(BaseModel):
    """Response for BA-01 — Resolve Enterprise Configuration (EX-C041-01). One entry per requested facet, each holding every resolved key within it."""
    organization_id: UUID
    facets: dict[str, list[ResolvedConfigurationValue]] = Field(
        ..., description="Facet name (ConfigurationFacet) -> resolved key/value list."
    )
    resolved_at: datetime


class EstablishConfigurationEntryRequest(BaseModel):
    """
    Request body for BA-02 — Establish/Update Enterprise Configuration
    (EX-C041-02). Writes a TENANT-scope override for the caller's own
    X-Tenant-ID — USER-scope establishment is not chartered by IRA-010
    (no self-service, non-admin establish flow exists; ConfigurationScopeLevel.USER
    is declared in the model for schema completeness only).
    """
    facet: ConfigurationFacet
    key: str = Field(..., min_length=1, max_length=100)
    value: Any = Field(..., description="The override payload — shape depends on facet+key (e.g. a string for theme_class/default_language/logo_url, a bool for accessibility flags, a string for a single Terminology term).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "facet": "THEME",
                "key": "theme_class",
                "value": "DARK",
            }
        }
    }


class ConfigurationEntryResponse(BaseModel):
    """Result of BA-02 — the newly-established ACTIVE Configuration Entry (CFG-000001)."""
    id: UUID
    organization_id: UUID
    scope_level: str
    facet: str
    key: str
    value: Any
    version: int
    lifecycle_state: str
    effective_from: datetime
    established_by_person_id: UUID | None

    model_config = {"from_attributes": True}


class ConfigurationEntryListResponse(BaseModel):
    """BA-02's own establish/update admin screen listing — every currently-ACTIVE TENANT-scope override across all facets for the caller's own X-Tenant-ID."""
    entries: list[ConfigurationEntryResponse]
