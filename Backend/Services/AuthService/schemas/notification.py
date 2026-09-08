"""
Request/response contracts for C-132 WP-19 BA-01 — "Establish / Manage
Enterprise Notification Context". Design basis: `TDS-C132 §16` (endpoint
shapes), `TDS-C132 §6.6` (the conceptual schema shape), `WP-19` BA-01
charter §6 (Input Contract). Mirrors AuthService's own
`schemas/entitlement_license.py` conventions.

Every field maps 1:1 to `models/c132_notification.py`. `status`,
`created_at`, `acknowledged_at` are never caller-supplied — BA-01
establishes `status = 'UNREAD'` and transitions once to `'ACKNOWLEDGED'`.
"""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

# DS-001 Chapter 21 (`DS-001-350`) — the closed severity taxonomy, mirrored
# from `models.c132_notification.NOTIFICATION_SEVERITIES`.
NotificationSeverity = Literal["success", "info", "warning", "danger"]
NotificationStatus = Literal["UNREAD", "ACKNOWLEDGED"]


class EstablishNotificationRequest(BaseModel):
    """
    One call establishes exactly one Notification for one recipient
    `Membership`. The recipient's own `Membership.organization_id` must
    equal the `X-Tenant-ID` this request is scoped to — a cross-tenant
    `membership_id` is rejected (`TDS-C132 §11`; charter §13).

    `severity` and the three composition elements realize `DS-001-351`'s
    closed structure. `source_type` / `source_id` are a non-authoritative,
    point-in-time citation of the causing action — never an FK
    (`TDS-C132 §6.6` item 1).
    """

    membership_id: UUID = Field(
        ...,
        description="Recipient anchor. Must belong to the X-Tenant-ID Organization.",
    )
    severity: NotificationSeverity = Field(
        ...,
        description="One of DS-001's four closed values (DS-001-350): success / info / warning / danger.",
    )
    what_happened: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="DS-001-351's mandatory composition element.",
    )
    why_it_matters: str | None = Field(
        None,
        max_length=2000,
        description="DS-001-351's optional composition element.",
    )
    what_happens_next: str | None = Field(
        None,
        max_length=2000,
        description="DS-001-351's optional composition element.",
    )
    source_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description=(
            "Free-text, non-authoritative citation of the causing capability/table "
            "(e.g. 'C023_ENTITLEMENT_CONTEXT', 'MEMBERSHIP'). A reference, never a definition."
        ),
    )
    source_id: UUID | None = Field(
        None,
        description="Optional point-in-time citation of the causing row's id. NOT a foreign key.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "membership_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "severity": "info",
                "what_happened": "Your supplier license was established.",
                "why_it_matters": "You can now access supplier workspaces.",
                "what_happens_next": "No action required.",
                "source_type": "C023_LICENSE_CONTEXT",
                "source_id": "9a1b2c3d-4e5f-6071-8293-a4b5c6d7e8f9",
            }
        }
    }


class NotificationResponse(BaseModel):
    """The established (or fetched) Notification."""

    id: UUID
    membership_id: UUID
    severity: str
    what_happened: str
    why_it_matters: str | None
    what_happens_next: str | None
    source_type: str
    source_id: UUID | None
    status: str
    created_at: datetime
    acknowledged_at: datetime | None

    model_config = {"from_attributes": True}
