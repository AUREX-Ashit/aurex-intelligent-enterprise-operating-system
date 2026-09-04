"""
Request/response contracts for C-023 WP-17 BA-01 — "Establish
Entitlement/License Context (Administrative)". Design basis:
`TDS-C023 §17.1` (inputs), `TDS-C023-A §3.1`/`§3.2` (the approved schema),
`WP-17 §6` (Input Contract). Mirrors `EstablishMembershipRequest`'s own
optional-effective-dates precedent.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class EstablishEntitlementLicenseRequest(BaseModel):
    """
    One call may establish a License (Membership-anchored) and/or an
    Entitlement (Organization-anchored, optionally Domain-scoped) — at
    least one must be requested. The two authority attributions
    (`approval_authority_id`, `committed_by_actor_id`) are never
    caller-supplied: the first is resolved server-side from the currently
    ACTIVE `approval_authorities` row, the second from the verified caller
    claims. `status` is never caller-supplied — BA-01 writes only `ACTIVE`.
    """

    # License side
    membership_id: UUID | None = Field(
        None,
        description="Membership Anchor. Provide to establish a License. Must belong to the X-Tenant-ID Organization.",
    )
    c023_license_type: str | None = Field(
        None,
        description=(
            "Optional. One of SUPPLIER / AUDITOR / BOARD_MEMBER / CONSULTANT "
            "(the four URA-001-115 specialized C-023 license types). NOT the "
            "FULL/LIGHT base classification, which stays on the Membership."
        ),
    )

    # Entitlement side
    organization_id: UUID | None = Field(
        None,
        description="Entitlement Anchor. Provide to establish an Entitlement. Must equal the X-Tenant-ID.",
    )
    domain_id: UUID | None = Field(
        None,
        description="Optional Domain scoping for the Entitlement. Omit for an organization-wide entitlement.",
    )
    entitlement_type_ref: str | None = Field(
        None,
        description="Identifier of an ALREADY-RECOGNIZED Entitlement Type. Required when establishing an Entitlement.",
    )

    # Common
    entitlement_source_reference: str | None = Field(
        None,
        description=(
            "Optional free-text citation of the non-authoritative Entitlement "
            "Source Reference (Subscription id, Contract id). Defaults to "
            "'ADMINISTRATIVE' for a direct grant."
        ),
        max_length=255,
    )
    effective_from: datetime | None = Field(None, description="Independent Commit-time business date. Defaults to now.")
    effective_to: datetime | None = Field(None, description="NULL = open-ended. Must be after effective_from when set.")

    @model_validator(mode="after")
    def _at_least_one_anchor(self) -> "EstablishEntitlementLicenseRequest":
        if self.membership_id is None and self.organization_id is None:
            raise ValueError(
                "Provide 'membership_id' (to establish a License) and/or "
                "'organization_id' with 'entitlement_type_ref' (to establish an Entitlement)."
            )
        if self.organization_id is not None and not self.entitlement_type_ref:
            raise ValueError("'entitlement_type_ref' is required when 'organization_id' is provided.")
        if self.entitlement_type_ref and self.organization_id is None:
            raise ValueError("'organization_id' is required when 'entitlement_type_ref' is provided.")
        if self.domain_id is not None and self.organization_id is None:
            raise ValueError("'domain_id' is only valid together with 'organization_id' (Entitlement side).")
        if self.c023_license_type is not None and self.membership_id is None:
            raise ValueError("'c023_license_type' is only valid together with 'membership_id' (License side).")
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "membership_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "c023_license_type": "SUPPLIER",
                "effective_from": "2026-09-01T00:00:00Z",
            }
        }
    }


class LicenseContextResponse(BaseModel):
    """The established (or fetched) Authoritative License Context."""

    id: UUID
    membership_id: UUID
    status: str
    effective_from: datetime
    effective_to: datetime | None
    entitlement_source_reference: str | None
    approval_authority_id: UUID
    committed_by_actor_id: UUID
    committed_at: datetime
    c023_license_type: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class EntitlementContextResponse(BaseModel):
    """The established (or fetched) Authoritative Entitlement Context."""

    id: UUID
    organization_id: UUID
    domain_id: UUID | None
    entitlement_type_ref: str
    status: str
    effective_from: datetime
    effective_to: datetime | None
    entitlement_source_reference: str | None
    approval_authority_id: UUID
    committed_by_actor_id: UUID
    committed_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class EstablishEntitlementLicenseResponse(BaseModel):
    """
    The establish outcome — whichever of License / Entitlement was
    requested and established. Frontend item 1 renders the confirmation
    from this; frontend item 2 (`GET`) re-fetches the current status.
    """

    license: LicenseContextResponse | None = None
    entitlement: EntitlementContextResponse | None = None


class ContextOutcomeResponse(BaseModel):
    """
    Frontend item 2 (`TDS-C023 §17.2`) — the immediate resulting
    establishment/status outcome for one context id. `kind` discriminates
    which body is populated.
    """

    kind: str = Field(..., description="LICENSE or ENTITLEMENT")
    license: LicenseContextResponse | None = None
    entitlement: EntitlementContextResponse | None = None
