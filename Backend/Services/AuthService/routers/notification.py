from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import (
    PLATFORM_ADMIN_ROLE_CODE,
    get_current_claims,
    require_matching_tenant_or_platform_admin,
)
from middleware.tenant import get_current_tenant
from models.database import db_manager
from repositories.c132_notification_repository import C132NotificationRepository
from repositories.membership_repository import MembershipRepository
from schemas.notification import EstablishNotificationRequest, NotificationResponse
from services.notification_establishment_service import NotificationEstablishmentService

router = APIRouter()


async def get_notification_service(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> NotificationEstablishmentService:
    return NotificationEstablishmentService(
        notification_repo=C132NotificationRepository(session),
        membership_repo=MembershipRepository(session),
    )


def _is_platform_admin(claims: dict) -> bool:
    return claims.get("role_code") == PLATFORM_ADMIN_ROLE_CODE


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish an Enterprise Notification (C-132, WP-19 BA-01)",
    description=(
        "Establish one persisted, recipient-anchored, in-application "
        "Notification for a `Membership` in the X-Tenant-ID Organization "
        "(`(none) -> UNREAD`, charter §9). INTRA-SERVICE ONLY for this "
        "increment — cross-service triggering, delivery (email/SMS/push/"
        "webhook), a real event bus, and multi-channel orchestration are "
        "all out of scope (`ROD-C132` RO Decision 3; `TDS-C132 §3`/`§6.4`). "
        "A Notification is not an Audit Event (`TDS-C132 §7`). The "
        "authenticated caller's own Organization must match X-Tenant-ID "
        "unless the caller holds PLATFORM_ADMIN "
        "(`require_matching_tenant_or_platform_admin`, the WP-10 / "
        "`CERT-WP-10` Finding B-1 precedent), AND the recipient "
        "`membership_id` must belong to the X-Tenant-ID Organization."
    ),
    responses={
        201: {"description": "Notification established."},
        400: {"description": "Missing/malformed Authorization or X-Tenant-ID header."},
        401: {"description": "Access token invalid or expired."},
        403: {
            "description": (
                "The caller's own Organization does not match X-Tenant-ID and the "
                "caller is not PLATFORM_ADMIN, or the recipient Membership belongs to "
                "a different Organization than X-Tenant-ID."
            )
        },
        404: {"description": "The recipient Membership was not found."},
        422: {"description": "Invalid request body (severity, composition, or source_type)."},
    },
)
async def establish_notification(
    request: EstablishNotificationRequest,
    service: Annotated[NotificationEstablishmentService, Depends(get_notification_service)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant)],
    claims: Annotated[dict, Depends(require_matching_tenant_or_platform_admin)],
) -> NotificationResponse:
    row = await service.establish(
        target_organization_id=tenant_id,
        actor_id=claims.get("person_id"),
        membership_id=request.membership_id,
        severity=request.severity,
        what_happened=request.what_happened,
        why_it_matters=request.why_it_matters,
        what_happens_next=request.what_happens_next,
        source_type=request.source_type,
        source_id=request.source_id,
    )
    return NotificationResponse.model_validate(row)


@router.get(
    "",
    response_model=list[NotificationResponse],
    summary="List my Enterprise Notifications (C-132, WP-19 BA-01)",
    description=(
        "The authenticated caller's own Notifications for their active "
        "Membership in the X-Tenant-ID Organization, newest first. "
        "Tenant-scoped and recipient-scoped by construction — the recipient "
        "Membership is resolved from the caller's own claims, never from a "
        "caller-supplied value (`TDS-C132 §11`; `CLAUDE.md §21.4`). A caller "
        "with no active Membership in that Organization sees an empty list."
    ),
    responses={
        200: {"description": "The caller's own notifications (possibly empty)."},
        400: {"description": "Missing/malformed Authorization or X-Tenant-ID header."},
        401: {"description": "Access token invalid or expired."},
    },
)
async def list_my_notifications(
    service: Annotated[NotificationEstablishmentService, Depends(get_notification_service)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant)],
    claims: Annotated[dict, Depends(get_current_claims)],
) -> list[NotificationResponse]:
    rows = await service.list_for_caller(
        caller_person_id=claims.get("person_id"),
        target_organization_id=tenant_id,
    )
    return [NotificationResponse.model_validate(row) for row in rows]


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Read one Enterprise Notification (C-132, WP-19 BA-01)",
    description=(
        "One Notification by id. A normal caller may read only their own "
        "recipient Notification; PLATFORM_ADMIN may read any Notification "
        "whose recipient belongs to the X-Tenant-ID Organization. Any other "
        "id — a different recipient's, a different tenant's, or nonexistent "
        "— returns 404, never a 403 that would confirm it exists elsewhere "
        "(`TDS-C132 §11`, mirroring WP-17's certified anti-enumeration "
        "pattern)."
    ),
    responses={
        200: {"description": "The notification."},
        400: {"description": "Missing/malformed Authorization or X-Tenant-ID header."},
        401: {"description": "Access token invalid or expired."},
        404: {"description": "No such notification visible to this caller in this Organization."},
    },
)
async def read_notification(
    notification_id: UUID,
    service: Annotated[NotificationEstablishmentService, Depends(get_notification_service)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant)],
    claims: Annotated[dict, Depends(get_current_claims)],
) -> NotificationResponse:
    row = await service.get_for_caller(
        notification_id=notification_id,
        caller_person_id=claims.get("person_id"),
        target_organization_id=tenant_id,
        is_platform_admin=_is_platform_admin(claims),
    )
    return NotificationResponse.model_validate(row)


@router.post(
    "/{notification_id}/acknowledge",
    response_model=NotificationResponse,
    summary="Acknowledge one Enterprise Notification (C-132, WP-19 BA-01)",
    description=(
        "Transition one Notification `UNREAD -> ACKNOWLEDGED` (charter §9). "
        "Gated to the recipient or PLATFORM_ADMIN (charter §10). Idempotent "
        "— acknowledging an already-acknowledged Notification returns it "
        "unchanged (`TDS-C132 §6.6` item 6). A cross-tenant / "
        "other-recipient id returns 404."
    ),
    responses={
        200: {"description": "The acknowledged notification."},
        400: {"description": "Missing/malformed Authorization or X-Tenant-ID header."},
        401: {"description": "Access token invalid or expired."},
        404: {"description": "No such notification visible to this caller in this Organization."},
    },
)
async def acknowledge_notification(
    notification_id: UUID,
    service: Annotated[NotificationEstablishmentService, Depends(get_notification_service)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant)],
    claims: Annotated[dict, Depends(get_current_claims)],
) -> NotificationResponse:
    row = await service.acknowledge_for_caller(
        notification_id=notification_id,
        caller_person_id=claims.get("person_id"),
        target_organization_id=tenant_id,
        is_platform_admin=_is_platform_admin(claims),
        actor_id=claims.get("person_id"),
    )
    return NotificationResponse.model_validate(row)
