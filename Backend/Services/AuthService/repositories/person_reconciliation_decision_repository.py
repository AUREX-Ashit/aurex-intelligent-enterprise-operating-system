from sqlalchemy.ext.asyncio import AsyncSession

from models.person_reconciliation_decision import PersonReconciliationDecision
from repositories.base_repository import BaseRepository


class PersonReconciliationDecisionRepository(BaseRepository[PersonReconciliationDecision]):
    """Repository for Person Reconciliation Decision records (WP-07 BA-06)."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(PersonReconciliationDecision, session)
