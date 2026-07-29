from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.structural_proposal import StructuralProposal
from repositories.base_repository import BaseRepository


class StructuralProposalRepository(BaseRepository[StructuralProposal]):
    """
    Repository for Proposed Outcome Context records (POC-000001 — see
    models/structural_proposal.py).

    WP-04 BA-04 needs BaseRepository's inherited create() (Shape,
    EX-C005-05) plus one new method, get_current_revision(), to find
    the revision a Refine (EX-C005-06) call supersedes and extends —
    the append-only model's own equivalent of a natural-key lookup, no
    OrganizationNode/StructuralChangeIntent-style get_by_code() applies
    here since revisions are identified by (proposal_id,
    revision_number), not a single unique business key.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(StructuralProposal, session)

    async def get_current_revision(self, proposal_id: UUID) -> StructuralProposal | None:
        """
        Returns the highest-revision_number row for a given proposal_id,
        or None if no proposal with that id exists. This is the "current"
        revision Refine (EX-C005-06) supersedes and the basis for its own
        next revision — mirroring the same append-only-lineage lookup
        POC-000001's own registered Versioning Policy requires.
        """
        result = await self.session.execute(
            select(StructuralProposal)
            .where(StructuralProposal.proposal_id == proposal_id)
            .order_by(StructuralProposal.revision_number.desc())
            .limit(1)
        )
        return result.scalars().first()
