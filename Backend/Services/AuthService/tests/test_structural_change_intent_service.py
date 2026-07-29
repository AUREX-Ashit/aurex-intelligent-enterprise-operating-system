from sqlalchemy.ext.asyncio import AsyncSession

from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from schemas.structural_change_intent import FrameStructuralChangeIntentRequest
from services.structural_change_intent_service import StructuralChangeIntentService


def _service(session: AsyncSession) -> StructuralChangeIntentService:
    return StructuralChangeIntentService(StructuralChangeIntentRepository(session))


async def test_frame_change_intent_creates_structural_change_intent(db_session: AsyncSession) -> None:
    """
    Business Activity Contract (WP-04 BA-03, ADR-006, IRA-004 §21): a
    Frame Structural Change Intent call creates exactly one row with the
    supplied change_rationale/target_outcome/decision_boundary, and a
    real, identity-bearing id (SD-002-004).
    """
    service = _service(db_session)
    request = FrameStructuralChangeIntentRequest(
        change_rationale="APAC Holding's reporting structure no longer reflects the post-acquisition entity footprint.",
        target_outcome="Consolidate the three newly-acquired APAC entities under a single regional holding node.",
        decision_boundary="Must not alter any existing EU or Americas structural relationships.",
    )

    intent = await service.frame_change_intent(request, actor_id="platform-admin-1")

    assert intent.id is not None
    assert intent.change_rationale == request.change_rationale
    assert intent.target_outcome == request.target_outcome
    assert intent.decision_boundary == request.decision_boundary


async def test_frame_change_intent_defaults_to_created_status(db_session: AsyncSession) -> None:
    """
    IRA-004 §21's own Lifecycle Model: BA-03 realizes only the CREATED
    transition — no other status is ever written by this Business
    Activity.
    """
    service = _service(db_session)
    request = FrameStructuralChangeIntentRequest(
        change_rationale="Observed structural gap.",
        target_outcome="Target structural outcome.",
    )

    intent = await service.frame_change_intent(request)

    assert intent.status == "CREATED"


async def test_frame_change_intent_allows_decision_boundary_to_be_omitted(db_session: AsyncSession) -> None:
    """decision_boundary is optional — EX-C005-04's own text does not mark it a mandatory input."""
    service = _service(db_session)
    request = FrameStructuralChangeIntentRequest(
        change_rationale="Observed structural gap.",
        target_outcome="Target structural outcome.",
    )

    intent = await service.frame_change_intent(request)

    assert intent.decision_boundary is None


async def test_frame_change_intent_does_not_deduplicate_identical_requests(db_session: AsyncSession) -> None:
    """
    Deliberate difference from OrganizationNodeService.establish() (BA-01):
    EX-C005-04's own text names no unique business key for a Change
    Intent Context — two structurally-identical Frame Structural Change
    Intent calls each create their own distinct decision record, not a
    409.
    """
    service = _service(db_session)
    request = FrameStructuralChangeIntentRequest(
        change_rationale="Observed structural gap.",
        target_outcome="Target structural outcome.",
    )

    first = await service.frame_change_intent(request)
    second = await service.frame_change_intent(request)

    assert first.id != second.id
