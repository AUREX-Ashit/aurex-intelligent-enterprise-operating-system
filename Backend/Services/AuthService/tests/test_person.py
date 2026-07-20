import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from models.identity import Identity
from models.person import Person


@pytest.fixture
async def seeded_person_identity(db_session: AsyncSession) -> tuple[Person, Identity]:
    """
    Seeds one Person with one primary local Identity, for deterministic-match tests.
    """
    person = Person(
        first_name="Ashit",
        last_name="Padhi",
        display_name="Ashit Padhi",
    )
    db_session.add(person)
    await db_session.flush()

    identity = Identity(
        person_id=person.id,
        email="ashit@corpstage.com",
        password_hash="irrelevant-for-recognition",
        identity_type="LOCAL",
        is_primary=True,
    )
    db_session.add(identity)
    await db_session.commit()

    return person, identity


def test_recognize_deterministic_match(client: TestClient, seeded_person_identity) -> None:
    """
    EX-C006-01 deterministic path: a known email resolves to a MATCHED
    outcome carrying the existing Authoritative Person Context.
    """
    person, _identity = seeded_person_identity

    response = client.post(
        "/person/recognize",
        json={"email": "ashit@corpstage.com"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == "MATCHED"
    assert body["person"]["person_id"] == str(person.id)
    assert body["person"]["first_name"] == "Ashit"
    assert body["person"]["last_name"] == "Padhi"
    assert body["person"]["display_name"] == "Ashit Padhi"


def test_recognize_no_candidate(client: TestClient) -> None:
    """
    EX-C006-01 deterministic path: an email with no existing Identity
    produces an explicit NO_CANDIDATE signal, never a match or an error.
    """
    response = client.post(
        "/person/recognize",
        json={"email": f"{uuid.uuid4()}@corpstage.com"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == "NO_CANDIDATE"
    assert body["person"] is None


def test_recognize_invalid_email_format(client: TestClient) -> None:
    """
    Malformed email fails validation before reaching the service —
    the only error path this deterministic-only implementation has.
    """
    response = client.post(
        "/person/recognize",
        json={"email": "not-an-email"},
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_recognize_does_not_require_tenant_header(client: TestClient) -> None:
    """
    /person/recognize is tenant-agnostic (URA-001-15: Person is independent
    of any company) — unlike most endpoints, no X-Tenant-ID header is
    required, and omitting it must not be blocked by TenantMiddleware.
    """
    response = client.post(
        "/person/recognize",
        json={"email": f"{uuid.uuid4()}@corpstage.com"},
    )

    assert response.status_code != 400


# ---------------------------------------------------------------------------
# EX-C006-02 — Establish New Person Context
# ---------------------------------------------------------------------------

def test_establish_person_succeeds_when_no_existing_match(client: TestClient) -> None:
    """
    EX-C006-02: establishing a person for a reference with no existing
    match succeeds, creating exactly one new Person.
    """
    email = f"{uuid.uuid4()}@corpstage.com"

    response = client.post(
        "/person/establish",
        json={
            "email": email,
            "first_name": "Nova",
            "last_name": "Reyes",
            "display_name": "Nova Reyes",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["first_name"] == "Nova"
    assert body["last_name"] == "Reyes"
    assert body["display_name"] == "Nova Reyes"
    assert "person_id" in body


def test_establish_person_rejected_when_match_already_exists(
    client: TestClient, seeded_person_identity
) -> None:
    """
    EX-C006-02's Trigger requires an explicit no-candidate outcome from
    EX-C006-01. Establishment must be rejected (409), not silently allowed
    or silently deduplicated, when a match already exists for the same
    reference — no second Person is created.
    """
    _person, _identity = seeded_person_identity

    response = client.post(
        "/person/establish",
        json={
            "email": "ashit@corpstage.com",
            "first_name": "Duplicate",
            "last_name": "Attempt",
            "display_name": "Duplicate Attempt",
        },
    )

    assert response.status_code == 409


def test_establish_person_invalid_email_format(client: TestClient) -> None:
    """
    Malformed email fails validation before reaching the service, same as
    EX-C006-01.
    """
    response = client.post(
        "/person/establish",
        json={
            "email": "not-an-email",
            "first_name": "Nova",
            "last_name": "Reyes",
            "display_name": "Nova Reyes",
        },
    )

    assert response.status_code == 422


def test_establish_person_rejects_empty_required_field(client: TestClient) -> None:
    """
    An empty first_name fails validation — the minimal-legitimate-facts
    requirement is enforced before establishment is attempted.
    """
    response = client.post(
        "/person/establish",
        json={
            "email": f"{uuid.uuid4()}@corpstage.com",
            "first_name": "",
            "last_name": "Reyes",
            "display_name": "Nova Reyes",
        },
    )

    assert response.status_code == 422


def test_establish_person_does_not_require_tenant_header(client: TestClient) -> None:
    """
    /person/establish is tenant-agnostic on the same basis as
    /person/recognize (URA-001-15).
    """
    response = client.post(
        "/person/establish",
        json={
            "email": f"{uuid.uuid4()}@corpstage.com",
            "first_name": "Nova",
            "last_name": "Reyes",
            "display_name": "Nova Reyes",
        },
    )

    assert response.status_code != 400
