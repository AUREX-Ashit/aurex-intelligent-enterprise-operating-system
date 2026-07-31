from sqlalchemy.ext.asyncio import AsyncSession

from models.identity_recovery_request import IdentityRecoveryRequest
from repositories.base_repository import BaseRepository


class IdentityRecoveryRequestRepository(BaseRepository[IdentityRecoveryRequest]):
    """Repository for IdentityRecoveryRequest records (WP-08 BA-02)."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(IdentityRecoveryRequest, session)
