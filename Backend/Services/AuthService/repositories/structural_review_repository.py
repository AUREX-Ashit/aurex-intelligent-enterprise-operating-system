from sqlalchemy.ext.asyncio import AsyncSession

from models.structural_review import StructuralReview
from repositories.base_repository import BaseRepository


class StructuralReviewRepository(BaseRepository[StructuralReview]):
    """
    Repository for Review Context records (RVC-000001 — see
    models/structural_review.py).

    WP-04 BA-06 needs only BaseRepository's inherited create() and
    get_by_id() (Review, then Resolve Concerns against the same row).
    No natural-key lookup applies — a review has no unique business
    key, the same disclosed difference already established for
    StructuralChangeIntentRepository/StructuralProposalRepository/
    ImpactAssessmentRepository.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(StructuralReview, session)
