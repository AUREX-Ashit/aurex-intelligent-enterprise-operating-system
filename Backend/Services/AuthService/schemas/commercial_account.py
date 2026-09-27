"""
Request/response contracts for C-022 WP-21 BA-01 — "Establish Commercial
Account". Design basis: `TDS-C022 §8`/`§15` (endpoint shape), `TDS-C022 §6.1`
(the conceptual schema shape), the WP-21 BA-01 charter. Mirrors
`AuthService`'s own `schemas/offering.py` convention.

Every field maps 1:1 to `models/c022_commercial_account.py`. `account_reference`,
`status`, `parent_account_id`, `created_at`, `updated_at` are never
caller-supplied — BA-01 system-assigns `account_reference` and establishes
`status = 'active'`, `parent_account_id = NULL` (`ROD-C022 §H`, `ROD-C022-A`
D8). **No `classification` field exists anywhere in this module** —
`ADR-038` Option A / `ROD-C022-A` D7.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class EstablishCommercialAccountRequest(BaseModel):
    """
    One call establishes exactly one standalone Authoritative Commercial
    Account in `status = 'active'` (`ROD-C022` §H/D1/D5). The catalog is
    platform-global (`ROD-C022` D2) — no tenant/organization field. No
    `classification` field (`ADR-038` Option A).
    """

    account_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Minimum canonical identity of the Commercial Account (COM-001-033).",
    )

    @field_validator("account_name")
    @classmethod
    def _no_blank_strings(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("must not be blank")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "account_name": "Acme Global Holdings",
            }
        }
    }


class CommercialAccountResponse(BaseModel):
    """The established Commercial Account — the Authoritative Commercial Account Context."""

    id: UUID
    account_reference: str
    account_name: str
    status: str
    parent_account_id: UUID | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
