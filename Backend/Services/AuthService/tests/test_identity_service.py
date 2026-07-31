import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.identity import Identity
from models.person import Person
from repositories.identity_recovery_request_repository import IdentityRecoveryRequestRepository
from repositories.identity_repository import IdentityRepository
from repositories.person_repository import PersonRepository
from schemas.identity import (
    ClassifyHandoffRejectionRequest,
    IdentityContextStatus,
    IdentityHandoffClassification,
    RecoverIdentityRequest,
    RoutedPath,
)
from services.identity_handoff_classification_service import IdentityHandoffClassificationService
from services.identity_recovery_service import IdentityRecoveryService
from services.identity_status_service import IdentityStatusService


@pytest.fixture
async def seeded_person_identity(db_session: AsyncSession) -> tuple[Person, Identity]:
    person = Person(first_name="Ida", last_name="Nguyen", display_name="Ida Nguyen")
    db_session.add(person)
    await db_session.flush()

    identity = Identity(
        person_id=person.id,
        email=f"{uuid.uuid4()}@corpstage.com",
        identity_type="LOCAL",
        is_primary=True,
    )
    db_session.add(identity)
    await db_session.commit()
    return person, identity


@pytest.fixture
async def seeded_deactivated_person_identity(db_session: AsyncSession) -> tuple[Person, Identity]:
    person = Person(first_name="Old", last_name="Account", display_name="Old Account", is_active=False)
    db_session.add(person)
    await db_session.flush()

    identity = Identity(
        person_id=person.id,
        email=f"{uuid.uuid4()}@corpstage.com",
        identity_type="LOCAL",
        is_primary=True,
    )
    db_session.add(identity)
    await db_session.commit()
    return person, identity


def _status_service(session: AsyncSession) -> IdentityStatusService:
    return IdentityStatusService(IdentityRepository(session), PersonRepository(session))


def _recovery_service(session: AsyncSession) -> IdentityRecoveryService:
    return IdentityRecoveryService(
        IdentityRecoveryRequestRepository(session),
        IdentityRepository(session),
        PersonRepository(session),
    )


def _classification_service(session: AsyncSession) -> IdentityHandoffClassificationService:
    return IdentityHandoffClassificationService(_status_service(session))


# ---------------------------------------------------------------------------
# BA-01 — Detect and Resolve Disrupted Identity Context (EX-C001-06)
# ---------------------------------------------------------------------------

async def test_refresh_status_current_for_active_person(
    db_session: AsyncSession, seeded_person_identity
) -> None:
    _person, identity = seeded_person_identity
    service = _status_service(db_session)

    result = await service.refresh(identity.id)

    assert result.status == IdentityContextStatus.CURRENT
    assert result.identity_id == identity.id


async def test_refresh_status_unresolved_for_deactivated_person(
    db_session: AsyncSession, seeded_deactivated_person_identity
) -> None:
    _person, identity = seeded_deactivated_person_identity
    service = _status_service(db_session)

    result = await service.refresh(identity.id)

    assert result.status == IdentityContextStatus.UNRESOLVED


async def test_refresh_status_raises_404_for_unknown_identity(db_session: AsyncSession) -> None:
    service = _status_service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.refresh(uuid.uuid4())

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# BA-02 — Recover Inaccessible Identity Context, self-service (EX-C001-07)
# ---------------------------------------------------------------------------

async def test_request_recovery_routes_to_re_resolution_when_identity_exists(
    db_session: AsyncSession, seeded_person_identity
) -> None:
    person, identity = seeded_person_identity
    service = _recovery_service(db_session)

    result = await service.request_recovery(
        RecoverIdentityRequest(person_id=person.id, reason="Lost device."),
        requested_by_identity_id=identity.id,
    )

    assert result.routed_path == RoutedPath.RE_RESOLUTION
    assert result.status == "PENDING"
    assert result.person_id == person.id


async def test_request_recovery_routes_to_new_identity_when_no_identity_exists(
    db_session: AsyncSession,
) -> None:
    person = Person(first_name="No", last_name="Identity", display_name="No Identity")
    db_session.add(person)
    await db_session.commit()

    service = _recovery_service(db_session)
    result = await service.request_recovery(
        RecoverIdentityRequest(person_id=person.id, reason="Never provisioned."),
        requested_by_identity_id=None,
    )

    assert result.routed_path == RoutedPath.NEW_IDENTITY


async def test_request_recovery_raises_404_for_unknown_person(db_session: AsyncSession) -> None:
    service = _recovery_service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.request_recovery(
            RecoverIdentityRequest(person_id=uuid.uuid4(), reason="x"),
            requested_by_identity_id=None,
        )

    assert exc_info.value.status_code == 404


async def test_request_recovery_raises_404_for_deactivated_person(
    db_session: AsyncSession, seeded_deactivated_person_identity
) -> None:
    person, _identity = seeded_deactivated_person_identity
    service = _recovery_service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.request_recovery(
            RecoverIdentityRequest(person_id=person.id, reason="x"),
            requested_by_identity_id=None,
        )

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# BA-03 — Classify Identity Hand-off Rejection (EX-C001-08)
# ---------------------------------------------------------------------------

async def test_classify_capability_scoped_when_identity_current(
    db_session: AsyncSession, seeded_person_identity
) -> None:
    _person, identity = seeded_person_identity
    service = _classification_service(db_session)

    result = await service.classify(
        ClassifyHandoffRejectionRequest(
            identity_id=identity.id,
            rejecting_capability="C-008",
            stated_reason="Workspace entry could not confirm the presented Identity Context.",
        )
    )

    assert result.classification == IdentityHandoffClassification.CAPABILITY_SCOPED_INSUFFICIENCY
    assert result.identity_context_preserved is True
    assert result.routed_to is None


async def test_classify_integrity_signal_when_identity_unresolved(
    db_session: AsyncSession, seeded_deactivated_person_identity
) -> None:
    _person, identity = seeded_deactivated_person_identity
    service = _classification_service(db_session)

    result = await service.classify(
        ClassifyHandoffRejectionRequest(
            identity_id=identity.id,
            rejecting_capability="C-008",
            stated_reason="Workspace entry rejected this Identity Context.",
        )
    )

    assert result.classification == IdentityHandoffClassification.INTEGRITY_SIGNAL
    assert result.identity_context_preserved is False
    assert result.routed_to is not None


async def test_classify_never_uses_stated_reason_as_basis(
    db_session: AsyncSession, seeded_person_identity
) -> None:
    """
    Contract 5.7: 'the dependent capability's stated rejection reason is
    a signal, not an authority.' Even a stated_reason that claims an
    integrity problem must not change the classification when the
    Identity Context's own independently-verifiable state is CURRENT.
    """
    _person, identity = seeded_person_identity
    service = _classification_service(db_session)

    result = await service.classify(
        ClassifyHandoffRejectionRequest(
            identity_id=identity.id,
            rejecting_capability="C-008",
            stated_reason="This Identity Context is definitely invalid and corrupted.",
        )
    )

    assert result.classification == IdentityHandoffClassification.CAPABILITY_SCOPED_INSUFFICIENCY
