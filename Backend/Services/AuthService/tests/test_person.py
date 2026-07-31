import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.identity import Identity
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role


def _access_token(role_code: str = "PLATFORM_ADMIN") -> str:
    """Mirrors test_domain_permission_api.py's _access_token() exactly."""
    claims = {
        "person_id": "11111111-1111-1111-1111-111111111111",
        "identity_id": "22222222-2222-2222-2222-222222222222",
        "organization_id": "33333333-3333-3333-3333-333333333333",
        "membership_id": "44444444-4444-4444-4444-444444444444",
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth_headers(role_code: str = "PLATFORM_ADMIN") -> dict[str, str]:
    return {"Authorization": f"Bearer {_access_token(role_code)}"}


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


# ---------------------------------------------------------------------------
# Fixtures for BA-03 through BA-10 (WP-07)
# ---------------------------------------------------------------------------

@pytest.fixture
async def seeded_bare_person(db_session: AsyncSession) -> Person:
    """A Person with no Identity and no Membership — for has_identity/has_active_membership=False assertions."""
    person = Person(first_name="Bare", last_name="Person", display_name="Bare Person")
    db_session.add(person)
    await db_session.commit()
    return person


@pytest.fixture
async def seeded_person_with_identity_and_membership(db_session: AsyncSession) -> Person:
    """A Person with an Identity and an ACTIVE Membership — for has_identity/has_active_membership=True assertions."""
    person = Person(first_name="Full", last_name="Context", display_name="Full Context")
    organization = Organization(
        organization_code="WP07-TEST-ORG",
        organization_name="WP-07 Test Org",
        organization_type="CORPORATE",
    )
    role = Role(role_code="WP07_TEST_ROLE", role_name="WP-07 Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    identity = Identity(person_id=person.id, email=f"{uuid.uuid4()}@corpstage.com", identity_type="LOCAL")
    membership = Membership(person_id=person.id, organization_id=organization.id, role_id=role.id, membership_status="ACTIVE")
    db_session.add_all([identity, membership])
    await db_session.commit()
    return person


@pytest.fixture
async def seeded_two_persons(db_session: AsyncSession) -> tuple[Person, Person]:
    person_a = Person(first_name="Alice", last_name="A", display_name="Alice A")
    person_b = Person(first_name="Alicia", last_name="B", display_name="Alicia B")
    db_session.add_all([person_a, person_b])
    await db_session.commit()
    return person_a, person_b


# ---------------------------------------------------------------------------
# BA-03 — Understand Authoritative Person Context (EX-C006-03)
# ---------------------------------------------------------------------------

def test_understand_person_returns_full_context(
    client: TestClient, seeded_person_with_identity_and_membership: Person
) -> None:
    response = client.get(
        f"/person/{seeded_person_with_identity_and_membership.id}",
        headers=_auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["person_id"] == str(seeded_person_with_identity_and_membership.id)
    assert body["has_identity"] is True
    assert body["has_active_membership"] is True


def test_understand_person_without_identity_or_membership(
    client: TestClient, seeded_bare_person: Person
) -> None:
    response = client.get(f"/person/{seeded_bare_person.id}", headers=_auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["has_identity"] is False
    assert body["has_active_membership"] is False


def test_understand_person_rejects_unknown_id(client: TestClient) -> None:
    response = client.get(f"/person/{uuid.uuid4()}", headers=_auth_headers())

    assert response.status_code == 404


def test_understand_person_requires_authorization_header(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.get(f"/person/{seeded_bare_person.id}")

    assert response.status_code == 400


def test_understand_person_rejects_non_platform_admin(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.get(f"/person/{seeded_bare_person.id}", headers=_auth_headers(role_code="ESG_MANAGER"))

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# BA-04 — Distinguish Candidate Person Matches (EX-C006-04)
# ---------------------------------------------------------------------------

def test_distinguish_selects_existing_candidate(
    client: TestClient, seeded_two_persons: tuple[Person, Person]
) -> None:
    person_a, person_b = seeded_two_persons

    response = client.post(
        "/person/distinguish",
        headers=_auth_headers(),
        json={
            "candidate_person_ids": [str(person_a.id), str(person_b.id)],
            "decision_type": "SELECTED_EXISTING",
            "selected_person_id": str(person_a.id),
            "rationale": "Confirmed via secondary identifier.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["decision_type"] == "SELECTED_EXISTING"
    assert body["selected_person_id"] == str(person_a.id)


def test_distinguish_single_candidate_requires_explicit_decision(
    client: TestClient, seeded_two_persons: tuple[Person, Person]
) -> None:
    """Recognition Authority Rule (§1.7): applies identically for exactly one candidate — still requires an explicit decision, never auto-confirmed."""
    person_a, _person_b = seeded_two_persons

    response = client.post(
        "/person/distinguish",
        headers=_auth_headers(),
        json={
            "candidate_person_ids": [str(person_a.id)],
            "decision_type": "SELECTED_EXISTING",
            "selected_person_id": str(person_a.id),
            "rationale": "Sole candidate explicitly confirmed by Person Steward.",
        },
    )

    assert response.status_code == 201
    assert response.json()["candidate_person_ids"] == [str(person_a.id)]


def test_distinguish_declares_new_person(client: TestClient, seeded_two_persons: tuple[Person, Person]) -> None:
    person_a, person_b = seeded_two_persons

    response = client.post(
        "/person/distinguish",
        headers=_auth_headers(),
        json={
            "candidate_person_ids": [str(person_a.id), str(person_b.id)],
            "decision_type": "NEW_PERSON",
            "rationale": "Neither candidate matches; establishing a new person.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["decision_type"] == "NEW_PERSON"
    assert body["selected_person_id"] is None


def test_distinguish_rejects_unknown_candidate(client: TestClient) -> None:
    response = client.post(
        "/person/distinguish",
        headers=_auth_headers(),
        json={
            "candidate_person_ids": [str(uuid.uuid4())],
            "decision_type": "NEW_PERSON",
            "rationale": "No match.",
        },
    )

    assert response.status_code == 404


def test_distinguish_rejects_selected_not_in_candidates(
    client: TestClient, seeded_two_persons: tuple[Person, Person]
) -> None:
    person_a, person_b = seeded_two_persons

    response = client.post(
        "/person/distinguish",
        headers=_auth_headers(),
        json={
            "candidate_person_ids": [str(person_a.id)],
            "decision_type": "SELECTED_EXISTING",
            "selected_person_id": str(person_b.id),
            "rationale": "Invalid selection.",
        },
    )

    assert response.status_code == 422


def test_distinguish_requires_authorization_header(client: TestClient) -> None:
    response = client.post(
        "/person/distinguish",
        json={"candidate_person_ids": [str(uuid.uuid4())], "decision_type": "NEW_PERSON", "rationale": "x"},
    )

    assert response.status_code == 400


def test_distinguish_rejects_non_platform_admin(client: TestClient, seeded_two_persons: tuple[Person, Person]) -> None:
    person_a, _person_b = seeded_two_persons

    response = client.post(
        "/person/distinguish",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"candidate_person_ids": [str(person_a.id)], "decision_type": "NEW_PERSON", "rationale": "x"},
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# BA-05 — Resolve Conflicting Person Context (EX-C006-05)
# ---------------------------------------------------------------------------

def test_resolve_conflict_classifies_ambiguity(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/resolve-conflict",
        headers=_auth_headers(),
        json={"conflicting_reference": "A different person may be meant.", "classification": "AMBIGUITY"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "AMBIGUITY"
    assert "EX-C006-04" in body["routed_to"]


def test_resolve_conflict_classifies_correction_needed(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/resolve-conflict",
        headers=_auth_headers(),
        json={"conflicting_reference": "Last name differs from authoritative record.", "classification": "CORRECTION_NEEDED"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "CORRECTION_NEEDED"
    assert "EX-C006-07" in body["routed_to"]


def test_resolve_conflict_rejects_unknown_person(client: TestClient) -> None:
    response = client.post(
        f"/person/{uuid.uuid4()}/resolve-conflict",
        headers=_auth_headers(),
        json={"conflicting_reference": "x", "classification": "AMBIGUITY"},
    )

    assert response.status_code == 404


def test_resolve_conflict_requires_authorization_header(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/resolve-conflict",
        json={"conflicting_reference": "x", "classification": "AMBIGUITY"},
    )

    assert response.status_code == 400


def test_resolve_conflict_rejects_non_platform_admin(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/resolve-conflict",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"conflicting_reference": "x", "classification": "AMBIGUITY"},
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# BA-06 — Review Potential Duplicate Person Indication (EX-C006-06)
# ---------------------------------------------------------------------------

def test_reconcile_confirms_duplicate(client: TestClient, seeded_two_persons: tuple[Person, Person]) -> None:
    person_a, person_b = seeded_two_persons

    response = client.post(
        "/person/reconcile",
        headers=_auth_headers(),
        json={
            "person_id_a": str(person_a.id),
            "person_id_b": str(person_b.id),
            "decision": "CONFIRMED_DUPLICATE",
            "rationale": "Same date of birth and matching secondary email confirmed.",
        },
    )

    assert response.status_code == 201
    assert response.json()["decision"] == "CONFIRMED_DUPLICATE"


def test_reconcile_confirms_distinct(client: TestClient, seeded_two_persons: tuple[Person, Person]) -> None:
    person_a, person_b = seeded_two_persons

    response = client.post(
        "/person/reconcile",
        headers=_auth_headers(),
        json={
            "person_id_a": str(person_a.id),
            "person_id_b": str(person_b.id),
            "decision": "CONFIRMED_DISTINCT",
            "rationale": "Different dates of birth confirmed.",
        },
    )

    assert response.status_code == 201
    assert response.json()["decision"] == "CONFIRMED_DISTINCT"


def test_reconcile_rejects_same_person_twice(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        "/person/reconcile",
        headers=_auth_headers(),
        json={
            "person_id_a": str(seeded_bare_person.id),
            "person_id_b": str(seeded_bare_person.id),
            "decision": "CONFIRMED_DISTINCT",
            "rationale": "x",
        },
    )

    assert response.status_code == 422


def test_reconcile_rejects_unknown_person(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        "/person/reconcile",
        headers=_auth_headers(),
        json={
            "person_id_a": str(seeded_bare_person.id),
            "person_id_b": str(uuid.uuid4()),
            "decision": "ESCALATED",
            "rationale": "x",
        },
    )

    assert response.status_code == 404


def test_reconcile_requires_authorization_header(client: TestClient, seeded_two_persons: tuple[Person, Person]) -> None:
    person_a, person_b = seeded_two_persons

    response = client.post(
        "/person/reconcile",
        json={"person_id_a": str(person_a.id), "person_id_b": str(person_b.id), "decision": "ESCALATED", "rationale": "x"},
    )

    assert response.status_code == 400


def test_reconcile_rejects_non_platform_admin(client: TestClient, seeded_two_persons: tuple[Person, Person]) -> None:
    person_a, person_b = seeded_two_persons

    response = client.post(
        "/person/reconcile",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"person_id_a": str(person_a.id), "person_id_b": str(person_b.id), "decision": "ESCALATED", "rationale": "x"},
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# BA-07 — Correct Person Context (EX-C006-07)
# ---------------------------------------------------------------------------

def test_correct_person_updates_field_and_preserves_prior_value(
    client: TestClient, seeded_bare_person: Person
) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/correct",
        headers=_auth_headers(),
        json={
            "field_name": "last_name",
            "corrected_value": "CorrectedLastName",
            "reason": "Legal name change confirmed via updated identification document.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["field_name"] == "last_name"
    assert body["prior_value"] == "Person"
    assert body["corrected_value"] == "CorrectedLastName"
    assert body["person"]["last_name"] == "CorrectedLastName"


def test_correct_person_rejects_unknown_id(client: TestClient) -> None:
    response = client.post(
        f"/person/{uuid.uuid4()}/correct",
        headers=_auth_headers(),
        json={"field_name": "last_name", "corrected_value": "X", "reason": "x"},
    )

    assert response.status_code == 404


def test_correct_person_requires_authorization_header(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/correct",
        json={"field_name": "last_name", "corrected_value": "X", "reason": "x"},
    )

    assert response.status_code == 400


def test_correct_person_rejects_non_platform_admin(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/correct",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"field_name": "last_name", "corrected_value": "X", "reason": "x"},
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# BA-08 — Enrich Person Context (EX-C006-08)
# ---------------------------------------------------------------------------

def test_enrich_person_adds_attribute(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/enrich",
        headers=_auth_headers(),
        json={
            "attribute_name": "preferred_pronoun",
            "attribute_value": "they/them",
            "source": "Self-reported during onboarding.",
            "sensitivity_classification": "INTERNAL",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["attribute_name"] == "preferred_pronoun"
    assert body["person_id"] == str(seeded_bare_person.id)


def test_enrich_person_rejects_unknown_id(client: TestClient) -> None:
    response = client.post(
        f"/person/{uuid.uuid4()}/enrich",
        headers=_auth_headers(),
        json={"attribute_name": "x", "attribute_value": "y", "source": "z", "sensitivity_classification": "PUBLIC"},
    )

    assert response.status_code == 404


def test_enrich_person_requires_authorization_header(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/enrich",
        json={"attribute_name": "x", "attribute_value": "y", "source": "z", "sensitivity_classification": "PUBLIC"},
    )

    assert response.status_code == 400


def test_enrich_person_rejects_non_platform_admin(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/enrich",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"attribute_name": "x", "attribute_value": "y", "source": "z", "sensitivity_classification": "PUBLIC"},
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# BA-09 — Hand Off Person Context to Identity Establishment (EX-C006-10)
# ---------------------------------------------------------------------------

def test_handoff_to_identity_accepted(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/handoff-to-identity",
        headers=_auth_headers(),
        json={"outcome": "ACCEPTED"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == "ACCEPTED"
    assert body["target_capability"] == "C-001"


def test_handoff_to_identity_returned_requires_reason(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/handoff-to-identity",
        headers=_auth_headers(),
        json={"outcome": "RETURNED"},
    )

    assert response.status_code == 422


def test_handoff_to_identity_returned_with_reason(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/handoff-to-identity",
        headers=_auth_headers(),
        json={"outcome": "RETURNED", "reason": "Insufficient Person context to link the presenting Identity."},
    )

    assert response.status_code == 200
    assert response.json()["outcome"] == "RETURNED"


def test_handoff_to_identity_rejects_unknown_person(client: TestClient) -> None:
    response = client.post(
        f"/person/{uuid.uuid4()}/handoff-to-identity",
        headers=_auth_headers(),
        json={"outcome": "ACCEPTED"},
    )

    assert response.status_code == 404


def test_handoff_to_identity_requires_authorization_header(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/handoff-to-identity",
        json={"outcome": "ACCEPTED"},
    )

    assert response.status_code == 400


def test_handoff_to_identity_rejects_non_platform_admin(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/handoff-to-identity",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"outcome": "ACCEPTED"},
    )

    assert response.status_code == 403


# ---------------------------------------------------------------------------
# BA-10 — Hand Off Person Context to Membership Establishment (EX-C006-11)
# ---------------------------------------------------------------------------

def test_handoff_to_membership_accepted(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/handoff-to-membership",
        headers=_auth_headers(),
        json={"outcome": "ACCEPTED"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == "ACCEPTED"
    assert body["target_capability"] == "C-007"


def test_handoff_to_membership_returned_with_reason(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/handoff-to-membership",
        headers=_auth_headers(),
        json={"outcome": "RETURNED", "reason": "Person context insufficient to anchor a Membership."},
    )

    assert response.status_code == 200
    assert response.json()["outcome"] == "RETURNED"


def test_handoff_to_membership_rejects_unknown_person(client: TestClient) -> None:
    response = client.post(
        f"/person/{uuid.uuid4()}/handoff-to-membership",
        headers=_auth_headers(),
        json={"outcome": "ACCEPTED"},
    )

    assert response.status_code == 404


def test_handoff_to_membership_requires_authorization_header(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/handoff-to-membership",
        json={"outcome": "ACCEPTED"},
    )

    assert response.status_code == 400


def test_handoff_to_membership_rejects_non_platform_admin(client: TestClient, seeded_bare_person: Person) -> None:
    response = client.post(
        f"/person/{seeded_bare_person.id}/handoff-to-membership",
        headers=_auth_headers(role_code="ESG_MANAGER"),
        json={"outcome": "ACCEPTED"},
    )

    assert response.status_code == 403
