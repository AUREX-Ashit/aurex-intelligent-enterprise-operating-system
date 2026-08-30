"""
C-040 Tenant Administration — chartered minimum Business Activity
"Tenant Establishment only" (Repository Owner Decision, 2026-08-26).
Implementation tests for TDS-016 §8's own atomic Establishment
transaction, per the Repository Owner's own minimum test list (A-L).

AI-002 is never populated by any fixture here except as an isolated,
function-scoped, in-memory test-only holder (mirroring
test_authority_holder.py's own established convention) — never the real,
constitutional AI-002 (TD-157, Open — BLOCKED, untouched by this suite).
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.authority_holder import AuthorityHolder, AuthorityHolderStatus
from models.organization import Organization
from models.tenant_registry import TenantRegistry


def _access_token(person_id: str, identity_id: str, role_code: str | None = None) -> str:
    """Directly crafts a JWT, mirroring test_authority_holder.py's own helper."""
    claims = {
        "person_id": person_id,
        "identity_id": identity_id,
        "organization_id": None,
        "membership_id": None,
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _auth_headers(**kwargs) -> dict[str, str]:
    return {"Authorization": f"Bearer {_access_token(**kwargs)}"}


async def _seed_holder(db_session: AsyncSession, authority_identity: str, holder_person_id: uuid.UUID) -> AuthorityHolder:
    holder = AuthorityHolder(
        authority_identity=authority_identity,
        holder_person_id=holder_person_id,
        appointment_instrument_ref="TEST-FIXTURE",
        status=AuthorityHolderStatus.ACTIVE.value,
    )
    db_session.add(holder)
    await db_session.commit()
    await db_session.refresh(holder)
    return holder


async def _seed_organization(db_session: AsyncSession, code: str | None = None) -> Organization:
    org = Organization(
        organization_code=code or f"TEST-{uuid.uuid4().hex[:12]}",
        organization_name="Test Establishment Org",
        organization_type="CORPORATE",
    )
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org


@pytest.fixture
async def ai001_ai002(db_session: AsyncSession) -> tuple[uuid.UUID, uuid.UUID]:
    """Seeds ACTIVE test-only AI-001 and AI-002 holders; returns their person_ids."""
    ai001_person_id = uuid.uuid4()
    ai002_person_id = uuid.uuid4()
    await _seed_holder(db_session, "AI-001", ai001_person_id)
    await _seed_holder(db_session, "AI-002", ai002_person_id)
    return ai001_person_id, ai002_person_id


# ---------------------------------------------------------------------------
# A. successful Tenant Establishment
# ---------------------------------------------------------------------------

async def test_successful_tenant_establishment(
    client: TestClient, db_session: AsyncSession, ai001_ai002: tuple[uuid.UUID, uuid.UUID]
) -> None:
    ai001_person_id, ai002_person_id = ai001_ai002
    org = await _seed_organization(db_session)

    response = client.post(
        "/tenants",
        json={"organization_id": str(org.id)},
        headers=_auth_headers(person_id=str(ai002_person_id), identity_id=str(uuid.uuid4())),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["organization_id"] == str(org.id)
    assert body["tenant_code"] == org.organization_code
    assert body["approved_by_actor_id"] == str(ai001_person_id)
    assert body["allocated_by_actor_id"] == str(ai002_person_id)


# ---------------------------------------------------------------------------
# B. authorization failure — no Authorization header at all
# ---------------------------------------------------------------------------

def test_establishment_rejects_missing_authorization_header(client: TestClient) -> None:
    response = client.post("/tenants", json={"organization_id": str(uuid.uuid4())})
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# C. no one can silently supply Business Approval — AI-001 unpopulated
# ---------------------------------------------------------------------------

async def test_establishment_rejects_when_ai001_unpopulated(
    client: TestClient, db_session: AsyncSession
) -> None:
    ai002_person_id = uuid.uuid4()
    await _seed_holder(db_session, "AI-002", ai002_person_id)  # AI-001 deliberately NOT seeded
    org = await _seed_organization(db_session)

    response = client.post(
        "/tenants",
        json={"organization_id": str(org.id)},
        headers=_auth_headers(person_id=str(ai002_person_id), identity_id=str(uuid.uuid4())),
    )
    assert response.status_code == 409
    assert "AI-001" in response.json()["detail"]


# ---------------------------------------------------------------------------
# D / E. PLATFORM_ADMIN / AUREX_ADMIN cannot bypass the AI-002 requirement
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("role_code", ["PLATFORM_ADMIN", "AUREX_ADMIN"])
def test_role_claim_does_not_substitute_for_ai002_holder(client: TestClient, role_code: str) -> None:
    response = client.post(
        "/tenants",
        json={"organization_id": str(uuid.uuid4())},
        headers=_auth_headers(person_id=str(uuid.uuid4()), identity_id=str(uuid.uuid4()), role_code=role_code),
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# F. duplicate / replayed establishment
# ---------------------------------------------------------------------------

async def test_duplicate_establishment_rejected(
    client: TestClient, db_session: AsyncSession, ai001_ai002: tuple[uuid.UUID, uuid.UUID]
) -> None:
    _, ai002_person_id = ai001_ai002
    org = await _seed_organization(db_session)
    headers = _auth_headers(person_id=str(ai002_person_id), identity_id=str(uuid.uuid4()))

    first = client.post("/tenants", json={"organization_id": str(org.id)}, headers=headers)
    assert first.status_code == 201

    replay = client.post("/tenants", json={"organization_id": str(org.id)}, headers=headers)
    assert replay.status_code == 409


# ---------------------------------------------------------------------------
# G. atomic rollback — a rejected attempt leaves no orphaned tenant_registry row
# ---------------------------------------------------------------------------

async def test_rejected_establishment_leaves_no_orphaned_tenant_row(
    client: TestClient, db_session: AsyncSession
) -> None:
    ai002_person_id = uuid.uuid4()
    await _seed_holder(db_session, "AI-002", ai002_person_id)  # AI-001 NOT seeded -> must fail
    org = await _seed_organization(db_session)

    response = client.post(
        "/tenants",
        json={"organization_id": str(org.id)},
        headers=_auth_headers(person_id=str(ai002_person_id), identity_id=str(uuid.uuid4())),
    )
    assert response.status_code == 409

    rows = (await db_session.execute(select(TenantRegistry))).scalars().all()
    assert rows == []

    refreshed_org = await db_session.get(Organization, org.id)
    assert refreshed_org.tenant_id is None


# ---------------------------------------------------------------------------
# H. Tenant -> Organization invariant (1:1, no reuse across Organizations)
# ---------------------------------------------------------------------------

async def test_tenant_organization_invariant_distinct_tenants(
    client: TestClient, db_session: AsyncSession, ai001_ai002: tuple[uuid.UUID, uuid.UUID]
) -> None:
    _, ai002_person_id = ai001_ai002
    org_a = await _seed_organization(db_session)
    org_b = await _seed_organization(db_session)
    headers = _auth_headers(person_id=str(ai002_person_id), identity_id=str(uuid.uuid4()))

    response_a = client.post("/tenants", json={"organization_id": str(org_a.id)}, headers=headers)
    response_b = client.post("/tenants", json={"organization_id": str(org_b.id)}, headers=headers)
    assert response_a.status_code == 201
    assert response_b.status_code == 201
    assert response_a.json()["id"] != response_b.json()["id"]

    refreshed_a = await db_session.get(Organization, org_a.id)
    refreshed_b = await db_session.get(Organization, org_b.id)
    assert refreshed_a.tenant_id == uuid.UUID(response_a.json()["id"])
    assert refreshed_b.tenant_id == uuid.UUID(response_b.json()["id"])
    assert refreshed_a.tenant_id != refreshed_b.tenant_id


# ---------------------------------------------------------------------------
# I. lifecycle state correctness
# ---------------------------------------------------------------------------

async def test_established_tenant_starts_provisioned_version_one(
    client: TestClient, db_session: AsyncSession, ai001_ai002: tuple[uuid.UUID, uuid.UUID]
) -> None:
    _, ai002_person_id = ai001_ai002
    org = await _seed_organization(db_session)

    response = client.post(
        "/tenants",
        json={"organization_id": str(org.id)},
        headers=_auth_headers(person_id=str(ai002_person_id), identity_id=str(uuid.uuid4())),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["lifecycle_state"] == "PROVISIONED"
    assert body["version"] == 1


# ---------------------------------------------------------------------------
# J. missing runtime authority holder — AI-002 entirely unpopulated
# ---------------------------------------------------------------------------

async def test_establishment_rejected_when_ai002_unpopulated(
    client: TestClient, db_session: AsyncSession
) -> None:
    org = await _seed_organization(db_session)  # neither AI-001 nor AI-002 seeded
    response = client.post(
        "/tenants",
        json={"organization_id": str(org.id)},
        headers=_auth_headers(person_id=str(uuid.uuid4()), identity_id=str(uuid.uuid4())),
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# K. existing Organization-scoped APIs remain unaffected by the schema addition
# ---------------------------------------------------------------------------

async def test_existing_organization_read_path_unaffected(
    client: TestClient, db_session: AsyncSession
) -> None:
    org = await _seed_organization(db_session)
    response = client.get(
        f"/organizations/{org.id}",
        headers=_auth_headers(person_id=str(uuid.uuid4()), identity_id=str(uuid.uuid4()), role_code="PLATFORM_ADMIN"),
    )
    assert response.status_code == 200
    assert response.json()["id"] == str(org.id)
    assert "tenant_id" not in response.json()  # OrganizationResponse's own declared field list is unchanged


# ---------------------------------------------------------------------------
# L. existing X-Tenant-ID semantics remain unchanged for other endpoints
# ---------------------------------------------------------------------------

def test_other_endpoints_still_require_x_tenant_id(client: TestClient) -> None:
    response = client.get(
        "/configuration",
        headers=_auth_headers(person_id=str(uuid.uuid4()), identity_id=str(uuid.uuid4())),
    )
    assert response.status_code == 400
    assert "X-Tenant-ID" in response.json()["message"]


# ---------------------------------------------------------------------------
# Additional: organization not found
# ---------------------------------------------------------------------------

def test_establishment_rejects_unknown_organization(
    client: TestClient, ai001_ai002: tuple[uuid.UUID, uuid.UUID]
) -> None:
    _, ai002_person_id = ai001_ai002
    response = client.post(
        "/tenants",
        json={"organization_id": str(uuid.uuid4())},
        headers=_auth_headers(person_id=str(ai002_person_id), identity_id=str(uuid.uuid4())),
    )
    assert response.status_code == 404
