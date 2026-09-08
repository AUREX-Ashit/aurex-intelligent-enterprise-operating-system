"""
C-132 Enterprise Notifications — WP-19 BA-01, "Establish / Manage Enterprise
Notification Context". Realizes `TDS-C132`'s finalized design on the
single-table schema recorded at `TDS-C132 §6.6` (schema-shape
STOP-and-report), hosted in `AuthService` per the Repository Owner's own
`TDS-C132 §6.5` H-1 decision.

Modeled directly on `EntitlementLicenseEstablishmentService` (WP-17) and
`MembershipService.establish()` — the already-certified establish pattern
(validate the anchor -> fail closed on a cross-Organization anchor ->
establish inside one DB transaction -> `record_audit` -> `publish_event`).

Scope, per `ROD-C132` RO Decision 3 / `WP-19` charter:
  * establish / list / read / acknowledge a persisted, tenant-scoped,
    recipient-anchored Notification record.
  * INTRA-SERVICE ONLY — every caller of `establish` in this first
    increment is inside `AuthService`. No cross-service call, no event
    bus, no delivery of any kind (`TDS-C132 §3`/`§6.4`; charter §19).
  * A Notification is NOT an Audit Event (`TDS-C132 §7`) — the
    `record_audit()` trail below is a separate, standard AuthService
    concern.

Tenant isolation (`CLAUDE.md §21.4`; `TDS-C132 §11`): every read/write
keys on a `membership_id` that this service resolves — from a
caller-supplied value validated against `X-Tenant-ID` (establish), or from
the caller's OWN claims + `X-Tenant-ID` (list / read / acknowledge). A
caller-supplied `membership_id` is never trusted for the read path. A
cross-Organization anchor on establish fails closed with 403; a
cross-tenant / other-recipient id on read/acknowledge returns 404, never a
403 that would confirm the row exists elsewhere.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status

from models.c132_notification import C132Notification
from observability import AuditStatus, publish_event, record_audit
from repositories.c132_notification_repository import C132NotificationRepository
from repositories.membership_repository import MembershipRepository

_ESTABLISH_ACTION = "ESTABLISH_NOTIFICATION"
_ACKNOWLEDGE_ACTION = "ACKNOWLEDGE_NOTIFICATION"


class NotificationEstablishmentService:
    """Business Activity orchestrator for C-132 WP-19 BA-01."""

    def __init__(
        self,
        notification_repo: C132NotificationRepository,
        membership_repo: MembershipRepository,
    ) -> None:
        self.notification_repo = notification_repo
        self.membership_repo = membership_repo

    # ------------------------------------------------------------------
    # Write path — establish
    # ------------------------------------------------------------------

    async def establish(
        self,
        *,
        target_organization_id: UUID,
        actor_id: str | None,
        membership_id: UUID,
        severity: str,
        what_happened: str,
        why_it_matters: str | None,
        what_happens_next: str | None,
        source_type: str,
        source_id: UUID | None,
    ) -> C132Notification:
        """
        Establish one Notification for `membership_id`. `membership_id` must
        resolve to a `Membership` in `target_organization_id` (the
        `X-Tenant-ID`-derived Organization) — a cross-Organization anchor
        fails closed with 403 (`TDS-C132 §11`; charter §13), mirroring
        `EntitlementLicenseEstablishmentService`'s own rejection.
        """
        membership = await self.membership_repo.get_by_id(membership_id)
        if membership is None:
            self._audit_denied(_ESTABLISH_ACTION, actor_id, target_organization_id, "recipient membership not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Membership exists with id '{membership_id}'.",
            )
        if membership.organization_id != target_organization_id:
            # Cross-Organization anchor — fail closed (`TDS-C132 §11`).
            self._audit_denied(
                _ESTABLISH_ACTION, actor_id, target_organization_id,
                "recipient membership belongs to a different Organization",
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Membership '{membership_id}' belongs to a different Organization "
                    f"than the X-Tenant-ID this request is scoped to."
                ),
            )

        now = datetime.now(timezone.utc)
        row = await self.notification_repo.create(
            {
                "membership_id": membership_id,
                "severity": severity,
                "what_happened": what_happened,
                "why_it_matters": why_it_matters,
                "what_happens_next": what_happens_next,
                "source_type": source_type,
                "source_id": source_id,
                "status": "UNREAD",
                "created_at": now,
            }
        )
        await self.notification_repo.session.flush()

        self._audit_success(
            action=_ESTABLISH_ACTION,
            actor_id=actor_id,
            target_organization_id=target_organization_id,
            notification=row,
        )
        publish_event(
            "ENTERPRISE_NOTIFICATION_ESTABLISHED",
            {
                "notification_id": str(row.id),
                "organization_id": str(target_organization_id),
                "membership_id": str(row.membership_id),
                "severity": row.severity,
                "source_type": row.source_type,
                "status": row.status,
            },
        )
        return row

    # ------------------------------------------------------------------
    # Read path — list / read
    # ------------------------------------------------------------------

    async def list_for_caller(
        self,
        *,
        caller_person_id: str | None,
        target_organization_id: UUID,
    ) -> list[C132Notification]:
        """
        Every Notification for the authenticated caller's OWN active
        Membership in `target_organization_id`, newest first. A caller with
        no active Membership in that Organization has no notifications to
        list — an empty list, never another tenant's data.
        """
        membership = await self._resolve_caller_membership(caller_person_id, target_organization_id)
        if membership is None:
            return []
        rows = await self.notification_repo.list_for_membership(membership.id)
        return list(rows)

    async def get_for_caller(
        self,
        *,
        notification_id: UUID,
        caller_person_id: str | None,
        target_organization_id: UUID,
        is_platform_admin: bool,
    ) -> C132Notification:
        """
        One Notification by id, tenant-isolated. A normal caller may read
        only their own recipient Notification; `PLATFORM_ADMIN` may read
        any Notification whose recipient Membership belongs to
        `target_organization_id`. Anything else -> 404 (`TDS-C132 §11`).
        """
        row = await self._resolve_visible_notification(
            notification_id, caller_person_id, target_organization_id, is_platform_admin
        )
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such notification.")
        return row

    # ------------------------------------------------------------------
    # State transition — acknowledge
    # ------------------------------------------------------------------

    async def acknowledge_for_caller(
        self,
        *,
        notification_id: UUID,
        caller_person_id: str | None,
        target_organization_id: UUID,
        is_platform_admin: bool,
        actor_id: str | None,
    ) -> C132Notification:
        """
        Transition one Notification `UNREAD -> ACKNOWLEDGED`. Gated to the
        recipient or `PLATFORM_ADMIN` (charter §10). Idempotent: an already
        `ACKNOWLEDGED` Notification is returned unchanged, no error, no
        second audit record (`TDS-C132 §6.6` item 6 — an authorized
        implementation-time choice). A cross-tenant / other-recipient id
        -> 404, never a 403.
        """
        row = await self._resolve_visible_notification(
            notification_id, caller_person_id, target_organization_id, is_platform_admin
        )
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such notification.")

        if row.status == "ACKNOWLEDGED":
            return row

        row.status = "ACKNOWLEDGED"
        row.acknowledged_at = datetime.now(timezone.utc)
        await self.notification_repo.session.flush()

        self._audit_success(
            action=_ACKNOWLEDGE_ACTION,
            actor_id=actor_id,
            target_organization_id=target_organization_id,
            notification=row,
        )
        publish_event(
            "ENTERPRISE_NOTIFICATION_ACKNOWLEDGED",
            {
                "notification_id": str(row.id),
                "organization_id": str(target_organization_id),
                "membership_id": str(row.membership_id),
                "status": row.status,
            },
        )
        return row

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _resolve_caller_membership(
        self, caller_person_id: str | None, target_organization_id: UUID
    ):
        if not caller_person_id:
            return None
        try:
            person_uuid = UUID(caller_person_id)
        except (ValueError, TypeError):
            return None
        return await self.membership_repo.get_active_membership(person_uuid, target_organization_id)

    async def _resolve_visible_notification(
        self,
        notification_id: UUID,
        caller_person_id: str | None,
        target_organization_id: UUID,
        is_platform_admin: bool,
    ) -> C132Notification | None:
        """
        Return the Notification only if the caller may see it in
        `target_organization_id`; otherwise `None` (the callers above turn
        that into a uniform 404). Never discloses that a hidden id exists.
        """
        if is_platform_admin:
            row = await self.notification_repo.get_by_id(notification_id)
            if row is None:
                return None
            recipient = await self.membership_repo.get_by_id(row.membership_id)
            if recipient is not None and recipient.organization_id == target_organization_id:
                return row
            return None

        membership = await self._resolve_caller_membership(caller_person_id, target_organization_id)
        if membership is None:
            return None
        return await self.notification_repo.get_for_membership(notification_id, membership.id)

    def _audit_denied(
        self, action: str, actor_id: str | None, organization_id: UUID, reason: str
    ) -> None:
        record_audit(
            action=action,
            resource=f"organization:{organization_id}",
            status=AuditStatus.DENIED,
            actor_id=actor_id or "SYSTEM",
            tenant_id=str(organization_id),
            metadata={"reason": reason},
        )

    def _audit_success(
        self,
        *,
        action: str,
        actor_id: str | None,
        target_organization_id: UUID,
        notification: C132Notification,
    ) -> None:
        record_audit(
            action=action,
            resource=f"c132_notification:{notification.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            tenant_id=str(target_organization_id),
            metadata={
                "notification_id": str(notification.id),
                "organization_id": str(target_organization_id),
                "membership_id": str(notification.membership_id),
                "severity": notification.severity,
                "source_type": notification.source_type,
                "source_id": str(notification.source_id) if notification.source_id else None,
                "status": notification.status,
            },
        )
