from sqlalchemy.ext.asyncio import AsyncSession

from models.impact_assessment import ImpactAssessment
from repositories.base_repository import BaseRepository


class ImpactAssessmentRepository(BaseRepository[ImpactAssessment]):
    """
    Repository for Impact Context records (IMC-000001 — see
    models/impact_assessment.py).

    WP-04 BA-05 needs only BaseRepository's inherited create()
    (Assess Structural Consequence). No natural-key lookup applies —
    an assessment has no unique business key, the same disclosed
    difference already established for StructuralChangeIntentRepository
    and StructuralProposalRepository.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ImpactAssessment, session)
