from sqlalchemy.ext.asyncio import AsyncSession

from models.person_enrichment import PersonEnrichment
from repositories.base_repository import BaseRepository


class PersonEnrichmentRepository(BaseRepository[PersonEnrichment]):
    """Repository for Person Enrichment records (WP-07 BA-08)."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(PersonEnrichment, session)
