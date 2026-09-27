"""
Request/response contracts for C-021 WP-20 BA-01 — "Establish / Manage
Offering Definition". Design basis: `TDS-C021 §13` (endpoint shapes),
`TDS-C021 §9` (the conceptual schema shape, as amended by Repository Owner
decisions O1 and O2), the WP-20 BA-01 charter. Mirrors AuthService's own
`schemas/notification.py` / `schemas/entitlement_license.py` conventions.

Every field maps 1:1 to `models/c021_offering_definition.py`.
`offering_reference`, `state`, `version`, `created_at`, `updated_at` are
never caller-supplied — BA-01 system-assigns `offering_reference` (O1) and
establishes `state = 'draft'`, `version = 1` (`ROD-C021` D7).
"""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

# `COM-001-021` Product↔Service axis — the closed classification set, mirrored
# from `models.c021_offering_definition.OFFERING_KINDS`.
OfferingKind = Literal["PRODUCT", "SERVICE"]
OfferingState = Literal["draft", "published", "retired"]


class EstablishOfferingDefinitionRequest(BaseModel):
    """
    One call establishes exactly one standalone Atomic Offering Definition in
    `state = 'draft'` (`ROD-C021` D4/D7). The catalog is platform-global
    (`ROD-C021` D8) — no tenant/organization field.

    `category_ref` is OPTIONAL / NULLABLE (`[RO DECISION]` O2) — omit it and
    the row persists with NULL; supply a value and it must be non-empty.
    `list_price_reference` is an optional opaque reference string only
    (`ROD-C021` D6) — never a number, never computed.
    """

    offering_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Canonical name of the Offering Definition (ROD-C021 D4).",
    )
    offering_kind: OfferingKind = Field(
        ...,
        description="Product / Service classification (COM-001-021 Product↔Service axis).",
    )
    category_ref: str | None = Field(
        None,
        max_length=100,
        description=(
            "Optional opaque, non-authoritative category reference (RO decision O2). "
            "Not a taxonomy key; no governed vocabulary. If supplied, must be non-empty."
        ),
    )
    list_price_reference: str | None = Field(
        None,
        max_length=100,
        description=(
            "Optional opaque list-price reference (ROD-C021 D6). A reference string only "
            "— never a numeric or computed price."
        ),
    )

    @field_validator("offering_name", "category_ref", "list_price_reference")
    @classmethod
    def _no_blank_strings(cls, v: str | None) -> str | None:
        if v is not None and v.strip() == "":
            raise ValueError("must not be blank when supplied")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "offering_name": "Enterprise ESG Reporting",
                "offering_kind": "SERVICE",
                "category_ref": "REPORTING",
                "list_price_reference": "PRICEBOOK-2026-ESG-STD",
            }
        }
    }


class OfferingDefinitionResponse(BaseModel):
    """The established (or fetched) Offering Definition — the Authoritative Offering Definition Context."""

    id: UUID
    offering_reference: str
    offering_name: str
    offering_kind: str
    category_ref: str | None
    list_price_reference: str | None
    state: str
    version: int
    supersedes_id: UUID | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
