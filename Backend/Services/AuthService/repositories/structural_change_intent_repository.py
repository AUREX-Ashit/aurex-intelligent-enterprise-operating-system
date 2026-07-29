from sqlalchemy.ext.asyncio import AsyncSession

from models.structural_change_intent import StructuralChangeIntent
from repositories.base_repository import BaseRepository


class StructuralChangeIntentRepository(BaseRepository[StructuralChangeIntent]):
    """
    Repository for Structural Change Intent records (SCI-000001 — see
    models/structural_change_intent.py).

    WP-04 BA-03 needs only BaseRepository's inherited create()
    (Frame Structural Change Intent). No get_by_*() natural-key lookup
    is added: unlike node_code/organization_code, EX-C005-04's own text
    names no unique business key for a Change Intent Context — every
    Frame Structural Change Intent call is a distinct decision record,
    not a deduplicated entity, so there is no pre-flight duplicate
    check to support (a deliberate difference from
    OrganizationNodeRepository.get_by_code(), disclosed rather than
    silently copied). get_by_id() is already inherited and sufficient
    for any future read path a later Business Activity (BA-04) may add.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(StructuralChangeIntent, session)
