import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.c132_notification import C132Notification
from repositories.base_repository import BaseRepository

# A defensive upper bound on the recipient list query. BA-01 charters no
# pagination contract (`TDS-C132 §16` names `GET /notifications` with no
# page parameters); this cap simply prevents an unbounded scan. Exposing
# real pagination is an implementation-time follow-up if a recipient ever
# accumulates more than this (`TDS-C132 §26`).
_LIST_HARD_CAP = 200


class C132NotificationRepository(BaseRepository[C132Notification]):
    """
    Repository for `c132_notification` records (C-132, WP-19 BA-01).

    The write path (`establish`) uses the inherited `create()` directly,
    mirroring every prior WP-0X establish repository. The two read helpers
    below are the recipient-scoped list and the tenant-isolated single
    read `TDS-C132 §16` requires — both key on `membership_id`, which is
    also the tenant anchor (`TDS-C132 §6.6` item 3), so tenant isolation
    is a property of the caller-membership the service resolves, not a
    separate predicate.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(C132Notification, session)

    async def list_for_membership(
        self, membership_id: uuid.UUID
    ) -> Sequence[C132Notification]:
        """
        Every Notification for one recipient `Membership`, newest first.
        The caller (service layer) resolves `membership_id` from the
        authenticated caller's own claims + `X-Tenant-ID` — never from a
        caller-supplied value — so this query is inherently
        recipient-scoped and tenant-scoped (`CLAUDE.md §21.4`;
        `TDS-C132 §11`).
        """
        query = (
            select(C132Notification)
            .where(C132Notification.membership_id == membership_id)
            .order_by(C132Notification.created_at.desc())
            .limit(_LIST_HARD_CAP)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_for_membership(
        self, notification_id: uuid.UUID, membership_id: uuid.UUID
    ) -> C132Notification | None:
        """
        One Notification by id, but only if it belongs to the given
        recipient `Membership`. A mismatch (different recipient, different
        tenant, or no such row) returns `None` — the service turns that
        into a 404, never a 403 that would confirm the row exists
        elsewhere (`TDS-C132 §11`, mirroring `WP-17`'s certified
        anti-enumeration pattern).
        """
        query = select(C132Notification).where(
            C132Notification.id == notification_id,
            C132Notification.membership_id == membership_id,
        )
        result = await self.session.execute(query)
        return result.scalars().first()
