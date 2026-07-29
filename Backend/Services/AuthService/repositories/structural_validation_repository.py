from sqlalchemy.ext.asyncio import AsyncSession

from models.structural_validation import StructuralValidation
from repositories.base_repository import BaseRepository


class StructuralValidationRepository(BaseRepository[StructuralValidation]):
    """
    Repository for Validation Context records (VLC-000001 — see
    models/structural_validation.py).

    WP-04 BA-07 needs only BaseRepository's inherited create(). No
    natural-key lookup applies — a validation has no unique business
    key, the same disclosed difference already established for
    StructuralChangeIntentRepository/StructuralProposalRepository/
    ImpactAssessmentRepository/StructuralReviewRepository.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(StructuralValidation, session)
