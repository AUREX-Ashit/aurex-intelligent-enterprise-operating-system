"""
C-040 Authority Runtime Enforcement (TDS-016/TDS-017) — implementation
tests for Phases 1/3/4/5, per the Repository Owner's own Phase 6 minimum
test list. AI-002 is never populated by any fixture here except where a
test explicitly needs an isolated, function-scoped, in-memory
cross-authority comparison (test 12) — never the real, constitutional
AI-002 (which remains unpopulated, TD-157, untouched by this suite).
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.authority_holder import AuthorityHolder, AuthorityHolderStatus
from models.identity import Identity
from models.person import Person
from services.auth_service import pwd_context

_PASSWORD = "correctHorseBattery1"


def _access_token(
    person_id: str,
    identity_id: str,
    organization_id: str | None = None,
    membership_id: str | None = None,
    role_code: str | None = None,
) -> str:
    """Directly crafts a JWT with arbitrary claims, mirroring test_identity_api.py's own _access_token() helper."""
    claims = {
        "person_id": person_id,
        "identity_id": identity_id,
        "organization_id": organization_id,
        "membership_id": membership_id,
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth_headers(**kwargs) -> dict[str, str]:
    return {"Authorization": f"Bearer {_access_token(**kwargs)}"}


@pytest.fixture
async def seeded_person_with_password(db_session: AsyncSession) -> tuple[Person, Identity]:
    """A real Person+Identity with a genuine bcrypt password_hash, no Membership of any kind."""
    person = Person(first_name="Test", last_name="Holder", display_name="Test Holder")
    db_session.add(person)
    await db_session.flush()

    identity = Identity(
        person_id=person.id,
        email=f"{uuid.uuid4()}@corpstage.com",
        identity_type="LOCAL",
        is_primary=True,
        password_hash=pwd_context.hash(_PASSWORD),
    )
    db_session.add(identity)
    await db_session.commit()
    return person, identity


async def _seed_active_holder(
    db_session: AsyncSession, authority_identity: str, holder_person_id: uuid.UUID, ref: str = "AI-003"
) -> AuthorityHolder:
    holder = AuthorityHolder(
        authority_identity=authority_identity,
        holder_person_id=holder_person_id,
        appointment_instrument_ref=ref,
        status=AuthorityHolderStatus.ACTIVE.value,
    )
    db_session.add(holder)
    await db_session.commit()
    await db_session.refresh(holder)
    return holder


# ---------------------------------------------------------------------------
# 1. valid AI-001 holder succeeds
# ---------------------------------------------------------------------------

async def test_valid_ai001_holder_login_and_check_succeeds(
    client: TestClient, db_session: AsyncSession, seeded_person_with_password
) -> None:
    person, identity = seeded_person_with_password
    await _seed_active_holder(db_session, "AI-001", person.id)

    login_response = client.post(
        "/auth/authority-login/AI-001",
        json={"email": identity.email, "password": _PASSWORD},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    check_response = client.get(
        "/auth/authority-check/ai-001",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert check_response.status_code == 200
    assert check_response.json()["person_id"] == str(person.id)  # 14. audit attribution


# ---------------------------------------------------------------------------
# 2 / 3. non-holder fails; zero-membership non-holder cannot obtain token
# ---------------------------------------------------------------------------

async def test_non_holder_cannot_obtain_authority_token(
    client: TestClient, db_session: AsyncSession, seeded_person_with_password
) -> None:
    # This Person has zero Organization Memberships (never created for
    # this fixture) and is not registered as any AuthorityHolder —
    # explicitly the "zero-Membership non-holder" case, not merely a
    # generic non-holder.
    person, identity = seeded_person_with_password
    await _seed_active_holder(db_session, "AI-001", uuid.uuid4())  # a different, unrelated holder

    response = client.post(
        "/auth/authority-login/AI-001",
        json={"email": identity.email, "password": _PASSWORD},
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# 4. valid pre-Organization authority token can authenticate (claims shape)
# ---------------------------------------------------------------------------

async def test_authority_token_carries_no_organization_or_membership_claim(
    client: TestClient, db_session: AsyncSession, seeded_person_with_password
) -> None:
    person, identity = seeded_person_with_password
    await _seed_active_holder(db_session, "AI-001", person.id)

    login_response = client.post(
        "/auth/authority-login/AI-001",
        json={"email": identity.email, "password": _PASSWORD},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    claims = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    assert claims["person_id"] == str(person.id)
    assert claims.get("organization_id") is None
    assert claims.get("membership_id") is None


# ---------------------------------------------------------------------------
# 5. pre-Organization token cannot access ordinary Organization-scoped endpoints
# ---------------------------------------------------------------------------

async def test_authority_token_rejected_by_ordinary_org_scoped_endpoint(
    client: TestClient, db_session: AsyncSession, seeded_person_with_password
) -> None:
    person, identity = seeded_person_with_password
    await _seed_active_holder(db_session, "AI-001", person.id)

    login_response = client.post(
        "/auth/authority-login/AI-001",
        json={"email": identity.email, "password": _PASSWORD},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/configuration",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(uuid.uuid4()),
        },
    )
    # require_matching_tenant_or_platform_admin: claims["organization_id"]
    # (None) can never equal a real tenant UUID — rejected by construction,
    # no new code required to enforce this (TDS-017 §22's own verified finding).
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# 6 / 7. PLATFORM_ADMIN / AUREX_ADMIN are not implicit substitutes
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("role_code", ["PLATFORM_ADMIN", "AUREX_ADMIN"])
def test_role_claim_does_not_substitute_for_authority_holder(client: TestClient, role_code: str) -> None:
    headers = _auth_headers(
        person_id=str(uuid.uuid4()),  # not any real holder
        identity_id=str(uuid.uuid4()),
        role_code=role_code,
    )
    response = client.get("/auth/authority-check/ai-001", headers=headers)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# 8. stale/superseded holder fails
# ---------------------------------------------------------------------------

async def test_superseded_holder_fails(
    client: TestClient, db_session: AsyncSession, seeded_person_with_password
) -> None:
    person, identity = seeded_person_with_password
    holder = await _seed_active_holder(db_session, "AI-001", person.id)
    holder.status = AuthorityHolderStatus.SUPERSEDED.value
    holder.effective_to = datetime.now(timezone.utc)
    await db_session.commit()

    headers = _auth_headers(person_id=str(person.id), identity_id=str(identity.id))
    response = client.get("/auth/authority-check/ai-001", headers=headers)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# 9. replacement holder succeeds
# ---------------------------------------------------------------------------

async def test_replacement_holder_succeeds_and_prior_holder_no_longer_does(
    client: TestClient, db_session: AsyncSession
) -> None:
    prior_person = Person(first_name="Prior", last_name="Holder", display_name="Prior Holder")
    new_person = Person(first_name="New", last_name="Holder", display_name="New Holder")
    db_session.add_all([prior_person, new_person])
    await db_session.flush()

    prior = await _seed_active_holder(db_session, "AI-001", prior_person.id)
    prior.status = AuthorityHolderStatus.SUPERSEDED.value
    prior.effective_to = datetime.now(timezone.utc)
    await db_session.commit()

    new_holder = AuthorityHolder(
        authority_identity="AI-001",
        holder_person_id=new_person.id,
        appointment_instrument_ref="AI-005",
        status=AuthorityHolderStatus.ACTIVE.value,
        supersedes_id=prior.id,
    )
    db_session.add(new_holder)
    await db_session.commit()
    await db_session.refresh(new_holder)

    assert new_holder.supersedes_id == prior.id  # 13. appointment/version lineage retained

    prior_check = client.get(
        "/auth/authority-check/ai-001",
        headers=_auth_headers(person_id=str(prior_person.id), identity_id=str(uuid.uuid4())),
    )
    assert prior_check.status_code == 403

    new_check = client.get(
        "/auth/authority-check/ai-001",
        headers=_auth_headers(person_id=str(new_person.id), identity_id=str(uuid.uuid4())),
    )
    assert new_check.status_code == 200


# ---------------------------------------------------------------------------
# 10. two ACTIVE holders for one authority cannot coexist
# ---------------------------------------------------------------------------

async def test_two_active_holders_for_same_authority_cannot_coexist(db_session: AsyncSession) -> None:
    person_a = Person(first_name="A", last_name="Holder", display_name="A Holder")
    person_b = Person(first_name="B", last_name="Holder", display_name="B Holder")
    db_session.add_all([person_a, person_b])
    await db_session.flush()

    db_session.add(AuthorityHolder(
        authority_identity="AI-001",
        holder_person_id=person_a.id,
        appointment_instrument_ref="AI-003",
        status=AuthorityHolderStatus.ACTIVE.value,
    ))
    await db_session.commit()

    db_session.add(AuthorityHolder(
        authority_identity="AI-001",
        holder_person_id=person_b.id,
        appointment_instrument_ref="AI-006",
        status=AuthorityHolderStatus.ACTIVE.value,
    ))
    with pytest.raises(Exception):
        await db_session.commit()
    await db_session.rollback()


# ---------------------------------------------------------------------------
# 11. AI-002 cannot authorize because no holder exists
# ---------------------------------------------------------------------------

def test_ai002_denies_everyone_because_unpopulated(client: TestClient) -> None:
    headers = _auth_headers(person_id=str(uuid.uuid4()), identity_id=str(uuid.uuid4()))
    response = client.get("/auth/authority-check/ai-002", headers=headers)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# 12. cross-authority holder cannot satisfy another authority's dependency
# ---------------------------------------------------------------------------

async def test_cross_authority_holder_cannot_satisfy_other_authority(db_session: AsyncSession, client: TestClient) -> None:
    """
    Isolated to this test's own function-scoped, in-memory SQLite database
    only (conftest.py's own per-test engine). This seeds a TEST-ONLY
    AI-002 holder row to verify cross-authority isolation logic — this is
    not, and must never be read as, population of the real, constitutional
    AI-002 (TD-157, Open — BLOCKED, untouched by this repository's own
    production/governance state).
    """
    ai001_person = Person(first_name="AI001", last_name="Test", display_name="AI001 Test")
    ai002_person = Person(first_name="AI002", last_name="Test", display_name="AI002 Test")
    db_session.add_all([ai001_person, ai002_person])
    await db_session.flush()

    await _seed_active_holder(db_session, "AI-001", ai001_person.id)
    await _seed_active_holder(db_session, "AI-002", ai002_person.id)

    ai001_headers = _auth_headers(person_id=str(ai001_person.id), identity_id=str(uuid.uuid4()))
    ai002_headers = _auth_headers(person_id=str(ai002_person.id), identity_id=str(uuid.uuid4()))

    assert client.get("/auth/authority-check/ai-002", headers=ai001_headers).status_code == 403
    assert client.get("/auth/authority-check/ai-001", headers=ai002_headers).status_code == 403
    # each still succeeds against its own authority
    assert client.get("/auth/authority-check/ai-001", headers=ai001_headers).status_code == 200
    assert client.get("/auth/authority-check/ai-002", headers=ai002_headers).status_code == 200


# ---------------------------------------------------------------------------
# invalid authority_identity is rejected (input validation, not in the
# minimum list but directly adjacent to it — the login endpoint accepts
# an arbitrary path segment and must not silently accept an unrecognized one)
# ---------------------------------------------------------------------------

def test_authority_login_rejects_unknown_authority_identity(client: TestClient) -> None:
    response = client.post(
        "/auth/authority-login/AI-999",
        json={"email": "nobody@corpstage.com", "password": "irrelevantPassword1"},
    )
    assert response.status_code == 400
