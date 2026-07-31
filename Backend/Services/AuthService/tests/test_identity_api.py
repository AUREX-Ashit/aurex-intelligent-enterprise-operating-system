import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.identity import Identity
from models.person import Person


def _access_token(person_id: str, identity_id: str, role_code: str = "ESG_MANAGER") -> str:
    """
    Mirrors test_person.py's _access_token() but with settable person_id/
    identity_id: BA-01/02/03 extract these claims and validate them
    against real seeded rows (self-referential actions), unlike /person's
    fixed-dummy-claims convention.
    """
    claims = {
        "person_id": person_id,
        "identity_id": identity_id,
        "organization_id": "33333333-3333-3333-3333-333333333333",
        "membership_id": "44444444-4444-4444-4444-444444444444",
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth_headers(person_id: str, identity_id: str, role_code: str = "ESG_MANAGER") -> dict[str, str]:
    return {"Authorization": f"Bearer {_access_token(person_id, identity_id, role_code)}"}


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


# ---------------------------------------------------------------------------
# BA-01 — POST /identity/refresh-status (EX-C001-06)
# ---------------------------------------------------------------------------

def test_refresh_status_returns_current(client: TestClient, seeded_person_identity) -> None:
    person, identity = seeded_person_identity

    response = client.post(
        "/identity/refresh-status",
        headers=_auth_headers(str(person.id), str(identity.id)),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "CURRENT"
    assert body["identity_id"] == str(identity.id)


def test_refresh_status_returns_unresolved_for_deactivated_person(
    client: TestClient, seeded_deactivated_person_identity
) -> None:
    person, identity = seeded_deactivated_person_identity

    response = client.post(
        "/identity/refresh-status",
        headers=_auth_headers(str(person.id), str(identity.id)),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "UNRESOLVED"


def test_refresh_status_requires_authentication(client: TestClient) -> None:
    response = client.post("/identity/refresh-status")

    assert response.status_code == 400


def test_refresh_status_does_not_require_tenant_header(client: TestClient, seeded_person_identity) -> None:
    person, identity = seeded_person_identity

    response = client.post(
        "/identity/refresh-status",
        headers=_auth_headers(str(person.id), str(identity.id)),
    )

    assert response.status_code != 400


# ---------------------------------------------------------------------------
# BA-02 — POST /identity/recover (EX-C001-07)
# ---------------------------------------------------------------------------

def test_recover_identity_succeeds_for_own_person(client: TestClient, seeded_person_identity) -> None:
    person, identity = seeded_person_identity

    response = client.post(
        "/identity/recover",
        json={"person_id": str(person.id), "reason": "Lost my authentication device."},
        headers=_auth_headers(str(person.id), str(identity.id)),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["routed_path"] == "RE_RESOLUTION"
    assert body["status"] == "PENDING"


def test_recover_identity_rejects_person_id_mismatch(client: TestClient, seeded_person_identity) -> None:
    person, identity = seeded_person_identity
    other_person_id = uuid.uuid4()

    response = client.post(
        "/identity/recover",
        json={"person_id": str(other_person_id), "reason": "On behalf of someone else."},
        headers=_auth_headers(str(person.id), str(identity.id)),
    )

    assert response.status_code == 403


def test_recover_identity_rejects_unknown_person(client: TestClient) -> None:
    caller_person_id = uuid.uuid4()

    response = client.post(
        "/identity/recover",
        json={"person_id": str(caller_person_id), "reason": "x"},
        headers=_auth_headers(str(caller_person_id), str(uuid.uuid4())),
    )

    assert response.status_code == 404


def test_recover_identity_rejects_empty_reason(client: TestClient, seeded_person_identity) -> None:
    person, identity = seeded_person_identity

    response = client.post(
        "/identity/recover",
        json={"person_id": str(person.id), "reason": ""},
        headers=_auth_headers(str(person.id), str(identity.id)),
    )

    assert response.status_code == 422


def test_recover_identity_requires_authentication(client: TestClient, seeded_person_identity) -> None:
    person, _identity = seeded_person_identity

    response = client.post(
        "/identity/recover",
        json={"person_id": str(person.id), "reason": "x"},
    )

    assert response.status_code == 400


# ---------------------------------------------------------------------------
# BA-03 — POST /identity/classify-handoff-rejection (EX-C001-08)
# ---------------------------------------------------------------------------

def test_classify_handoff_rejection_capability_scoped(
    client: TestClient, seeded_person_identity
) -> None:
    person, identity = seeded_person_identity

    response = client.post(
        "/identity/classify-handoff-rejection",
        json={
            "identity_id": str(identity.id),
            "rejecting_capability": "C-008",
            "stated_reason": "Workspace entry could not confirm the presented Identity Context.",
        },
        headers=_auth_headers(str(person.id), str(identity.id)),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "CAPABILITY_SCOPED_INSUFFICIENCY"
    assert body["identity_context_preserved"] is True


def test_classify_handoff_rejection_integrity_signal(
    client: TestClient, seeded_deactivated_person_identity
) -> None:
    person, identity = seeded_deactivated_person_identity

    response = client.post(
        "/identity/classify-handoff-rejection",
        json={
            "identity_id": str(identity.id),
            "rejecting_capability": "C-008",
            "stated_reason": "Workspace entry rejected this Identity Context.",
        },
        headers=_auth_headers(str(person.id), str(identity.id)),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "INTEGRITY_SIGNAL"
    assert body["identity_context_preserved"] is False
    assert body["routed_to"] is not None


def test_classify_handoff_rejection_unknown_identity(client: TestClient, seeded_person_identity) -> None:
    person, identity = seeded_person_identity

    response = client.post(
        "/identity/classify-handoff-rejection",
        json={
            "identity_id": str(uuid.uuid4()),
            "rejecting_capability": "C-008",
            "stated_reason": "x",
        },
        headers=_auth_headers(str(person.id), str(identity.id)),
    )

    assert response.status_code == 404


def test_classify_handoff_rejection_requires_authentication(
    client: TestClient, seeded_person_identity
) -> None:
    _person, identity = seeded_person_identity

    response = client.post(
        "/identity/classify-handoff-rejection",
        json={
            "identity_id": str(identity.id),
            "rejecting_capability": "C-008",
            "stated_reason": "x",
        },
    )

    assert response.status_code == 400
