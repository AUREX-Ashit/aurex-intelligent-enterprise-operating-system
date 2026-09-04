"""
C-023 Licensing & Entitlement — WP-17 BA-01 ("Establish Entitlement/License
Context (Administrative)") implementation tests.

Covers the WP-17 §18 / TDS-C023 §21 test obligations and the CLAUDE.md
§21.4 Mandatory Tenant-Isolation Test Checklist:

  * the License establish happy path + the resulting-outcome GET
  * INV-C023-10 duplicate rejection (pre-check) and the DB-level partial
    unique index race backstop (`ux_c023_license_context_current`)
  * negative control — the Approval Authority contract denies by default:
    no authority row, no binding, unsupported (MAJORITY) strategy, and
    PLATFORM_ADMIN / AUREX_ADMIN claims do NOT bypass (mirrors
    `test_role_claim_does_not_substitute_for_ai002_holder`)
  * tenant isolation — two distinct, unrelated Organizations with no
    shared row; a caller in Org A cannot establish or read Org B's
    context; an explicit probe of a foreign `membership_id` not derived
    from the caller's own claims
  * Decision 6 — `memberships.license_type` is untouched and no C-023 row
    stores a FULL/LIGHT value
  * the Entitlement half is vacuously blocked (Decision 3 deferred) — a
    clean 422, no row written
  * audit — a SUCCESS record is emitted on establish

The certified WP-18 infrastructure (`membership_approval_authority`,
`resolve_approval_authority()`, `require_approval_authority()`) is consumed
as-is and never modified.
"""

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.approval_authority import ApprovalAuthority
from models.c023_entitlement_context import C023EntitlementContext
from models.c023_license_context import C023LicenseContext
from models.membership import LicenseType, Membership
from models.membership_approval_authority import MembershipApprovalAuthority
from models.organization import Organization
from models.person import Person
from models.role import Role

COMMIT_AUTHORITY_NAME = "Entitlement/License Commit Authority"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _access_token(person_id: str, organization_id: str | None, membership_id: str | None,
                  role_code: str | None = None) -> str:
    claims = {
        "person_id": person_id,
        "identity_id": str(uuid.uuid4()),
        "organization_id": organization_id,
        "membership_id": membership_id,
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _headers(org_id: str, *, person_id: str, membership_id: str | None,
             caller_org_id: str | None = None, role_code: str | None = None) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_access_token(person_id, caller_org_id or org_id, membership_id, role_code)}",
        "X-Tenant-ID": org_id,
    }


class _Seed:
    def __init__(self, org: Organization, person: Person, membership: Membership,
                 authority: ApprovalAuthority) -> None:
        self.org = org
        self.person = person
        self.membership = membership
        self.authority = authority


async def _seed_org_with_bound_caller(
    db_session: AsyncSession,
    *,
    code: str,
    approval_strategy: str = "ANY_ONE",
    majority_threshold_pct: int | None = None,
    authority_status: str = "ACTIVE",
    bind_caller: bool = True,
    with_authority: bool = True,
) -> _Seed:
    role = Role(role_code=f"ROLE_{code}", role_name=f"Role {code}")
    org = Organization(organization_code=code, organization_name=code, organization_type="CORPORATE")
    person = Person(first_name=code, last_name="Caller", display_name=f"{code} Caller")
    db_session.add_all([role, org, person])
    await db_session.flush()

    membership = Membership(
        person_id=person.id, organization_id=org.id, role_id=role.id,
        membership_status="ACTIVE", license_type=LicenseType.FULL.value,
    )
    db_session.add(membership)
    await db_session.flush()

    authority = None
    if with_authority:
        authority = ApprovalAuthority(
            organization_id=org.id,
            authority_name=COMMIT_AUTHORITY_NAME,
            approval_strategy=approval_strategy,
            majority_threshold_pct=majority_threshold_pct,
            scope_type="COMPANY",
            status=authority_status,
        )
        db_session.add(authority)
        await db_session.flush()
        if bind_caller:
            db_session.add(MembershipApprovalAuthority(
                membership_id=membership.id, approval_authority_id=authority.id, effective_to=None,
            ))
            await db_session.flush()

    await db_session.commit()
    return _Seed(org, person, membership, authority)


def _establish_license_body(membership_id: str, **extra) -> dict:
    body = {"membership_id": membership_id}
    body.update(extra)
    return body


# ---------------------------------------------------------------------------
# A. License establish — happy path
# ---------------------------------------------------------------------------

async def test_establish_license_happy_path(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-A")

    resp = client.post(
        "/entitlement-license-contexts",
        json=_establish_license_body(str(s.membership.id), c023_license_type="SUPPLIER"),
        headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)),
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["entitlement"] is None
    lic = body["license"]
    assert lic["membership_id"] == str(s.membership.id)
    assert lic["status"] == "ACTIVE"
    assert lic["c023_license_type"] == "SUPPLIER"
    assert lic["effective_to"] is None
    assert lic["entitlement_source_reference"] == "ADMINISTRATIVE"
    assert lic["approval_authority_id"] == str(s.authority.id)
    assert lic["committed_by_actor_id"] == str(s.person.id)

    row = (await db_session.execute(select(C023LicenseContext))).scalars().one()
    assert row.membership_id == s.membership.id
    assert row.status == "ACTIVE"
    assert row.effective_to is None


async def test_get_resulting_outcome(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-GET")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))
    created = client.post("/entitlement-license-contexts",
                          json=_establish_license_body(str(s.membership.id)), headers=h)
    assert created.status_code == 201
    ctx_id = created.json()["license"]["id"]

    got = client.get(f"/entitlement-license-contexts/{ctx_id}", headers=h)
    assert got.status_code == 200
    assert got.json()["kind"] == "LICENSE"
    assert got.json()["license"]["id"] == ctx_id
    assert got.json()["entitlement"] is None


async def test_get_unknown_context_is_404(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-404")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))
    got = client.get(f"/entitlement-license-contexts/{uuid.uuid4()}", headers=h)
    assert got.status_code == 404


async def test_default_effective_from_and_open_ended(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-DATES")
    resp = client.post("/entitlement-license-contexts",
                       json=_establish_license_body(str(s.membership.id)),
                       headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)))
    assert resp.status_code == 201
    assert resp.json()["license"]["effective_from"] is not None
    assert resp.json()["license"]["effective_to"] is None


# ---------------------------------------------------------------------------
# B. INV-C023-10 — one current License Context per Membership
# ---------------------------------------------------------------------------

async def test_duplicate_current_license_rejected(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-DUP")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))
    first = client.post("/entitlement-license-contexts",
                        json=_establish_license_body(str(s.membership.id)), headers=h)
    assert first.status_code == 201
    second = client.post("/entitlement-license-contexts",
                         json=_establish_license_body(str(s.membership.id)), headers=h)
    assert second.status_code == 409
    assert "INV-C023-10" in second.json()["detail"]
    rows = (await db_session.execute(select(C023LicenseContext))).scalars().all()
    assert len(rows) == 1


async def test_partial_unique_index_is_the_race_backstop(client: TestClient, db_session: AsyncSession, monkeypatch) -> None:
    """
    If two concurrent establishes both pass the pre-check, the partial
    unique index `ux_c023_license_context_current` must reject the second —
    surfacing as a 409, never a duplicate current context, with the raced
    insert rolled back. Simulated by committing a current row first, then
    forcing the pre-check to see nothing (the race window), then
    establishing again through the real API.
    """
    s = await _seed_org_with_bound_caller(db_session, code="ELC-RACE")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))

    # A pre-existing, committed current License Context for this Membership.
    db_session.add(C023LicenseContext(
        membership_id=s.membership.id, status="ACTIVE",
        effective_from=datetime.now(timezone.utc), effective_to=None,
        entitlement_source_reference="ADMINISTRATIVE",
        approval_authority_id=s.authority.id, committed_by_actor_id=s.person.id,
        committed_at=datetime.now(timezone.utc), created_at=datetime.now(timezone.utc),
    ))
    await db_session.commit()

    from repositories.c023_license_context_repository import C023LicenseContextRepository

    async def _blind(self, membership_id):  # noqa: ANN001 — the race window: pre-check sees nothing
        return None

    monkeypatch.setattr(C023LicenseContextRepository, "get_current_for_membership", _blind)

    raced = client.post("/entitlement-license-contexts",
                        json=_establish_license_body(str(s.membership.id)), headers=h)
    assert raced.status_code == 409
    rows = (await db_session.execute(select(C023LicenseContext))).scalars().all()
    assert len(rows) == 1  # only the pre-existing row; the raced insert was rolled back


# ---------------------------------------------------------------------------
# C. Negative control — Approval Authority denies by default
# ---------------------------------------------------------------------------

async def test_denied_when_no_authority_configured(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-NOAUTH", with_authority=False)
    resp = client.post("/entitlement-license-contexts",
                       json=_establish_license_body(str(s.membership.id)),
                       headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)))
    assert resp.status_code == 403
    assert (await db_session.execute(select(C023LicenseContext))).scalars().all() == []


async def test_denied_when_caller_has_no_binding(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-NOBIND", bind_caller=False)
    resp = client.post("/entitlement-license-contexts",
                       json=_establish_license_body(str(s.membership.id)),
                       headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)))
    assert resp.status_code == 403
    assert (await db_session.execute(select(C023LicenseContext))).scalars().all() == []


async def test_denied_for_unsupported_majority_strategy(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(
        db_session, code="ELC-MAJ", approval_strategy="MAJORITY", majority_threshold_pct=51,
    )
    resp = client.post("/entitlement-license-contexts",
                       json=_establish_license_body(str(s.membership.id)),
                       headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)))
    assert resp.status_code == 403
    assert "UNSUPPORTED_STRATEGY" in resp.json()["detail"]


@pytest.mark.parametrize("role_code", ["PLATFORM_ADMIN", "AUREX_ADMIN"])
async def test_admin_role_claim_does_not_bypass(client: TestClient, db_session: AsyncSession, role_code: str) -> None:
    """No admin bypass exists for this gate (TDS-018 §11/§18)."""
    s = await _seed_org_with_bound_caller(db_session, code=f"ELC-{role_code[:4]}", with_authority=False)
    resp = client.post(
        "/entitlement-license-contexts",
        json=_establish_license_body(str(s.membership.id)),
        headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id), role_code=role_code),
    )
    assert resp.status_code == 403


async def test_missing_authorization_header_is_400(client: TestClient) -> None:
    resp = client.post("/entitlement-license-contexts",
                       json={"membership_id": str(uuid.uuid4())},
                       headers={"X-Tenant-ID": str(uuid.uuid4())})
    assert resp.status_code == 400


async def test_missing_tenant_header_is_400(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-NOTEN")
    resp = client.post(
        "/entitlement-license-contexts",
        json=_establish_license_body(str(s.membership.id)),
        headers={"Authorization": f"Bearer {_access_token(str(s.person.id), str(s.org.id), str(s.membership.id))}"},
    )
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# D. Tenant isolation (CLAUDE.md §21.4)
# ---------------------------------------------------------------------------

async def test_two_unrelated_orgs_have_no_shared_row(client: TestClient, db_session: AsyncSession) -> None:
    a = await _seed_org_with_bound_caller(db_session, code="ELC-ISO-A")
    b = await _seed_org_with_bound_caller(db_session, code="ELC-ISO-B")

    ra = client.post("/entitlement-license-contexts", json=_establish_license_body(str(a.membership.id)),
                     headers=_headers(str(a.org.id), person_id=str(a.person.id), membership_id=str(a.membership.id)))
    rb = client.post("/entitlement-license-contexts", json=_establish_license_body(str(b.membership.id)),
                     headers=_headers(str(b.org.id), person_id=str(b.person.id), membership_id=str(b.membership.id)))
    assert ra.status_code == 201 and rb.status_code == 201

    rows = (await db_session.execute(select(C023LicenseContext))).scalars().all()
    assert len(rows) == 2
    by_membership = {r.membership_id for r in rows}
    assert by_membership == {a.membership.id, b.membership.id}
    assert ra.json()["license"]["id"] != rb.json()["license"]["id"]
    assert ra.json()["license"]["approval_authority_id"] != rb.json()["license"]["approval_authority_id"]


async def test_caller_cannot_establish_license_for_foreign_membership(client: TestClient, db_session: AsyncSession) -> None:
    """
    Explicit foreign-identifier probe (§21.4 (c)): the caller is bound in
    Org A; they supply Org B's `membership_id` with X-Tenant-ID = Org A.
    The Commit Authority resolves for Org A (the caller IS bound there),
    so the request clears the dependency — then the service rejects the
    cross-Organization anchor (403). No row is written in either Org.
    """
    a = await _seed_org_with_bound_caller(db_session, code="ELC-XORG-A")
    b = await _seed_org_with_bound_caller(db_session, code="ELC-XORG-B")

    resp = client.post(
        "/entitlement-license-contexts",
        json=_establish_license_body(str(b.membership.id)),  # foreign membership
        headers=_headers(str(a.org.id), person_id=str(a.person.id), membership_id=str(a.membership.id)),
    )
    assert resp.status_code == 403
    assert (await db_session.execute(select(C023LicenseContext))).scalars().all() == []


async def test_caller_cannot_read_foreign_org_context(client: TestClient, db_session: AsyncSession) -> None:
    a = await _seed_org_with_bound_caller(db_session, code="ELC-RD-A")
    b = await _seed_org_with_bound_caller(db_session, code="ELC-RD-B")
    hb = _headers(str(b.org.id), person_id=str(b.person.id), membership_id=str(b.membership.id))
    created = client.post("/entitlement-license-contexts", json=_establish_license_body(str(b.membership.id)), headers=hb)
    assert created.status_code == 201
    ctx_id = created.json()["license"]["id"]

    # Caller A, scoped to Org A, asks for Org B's context id -> 404 (not 403).
    ha = _headers(str(a.org.id), person_id=str(a.person.id), membership_id=str(a.membership.id))
    got = client.get(f"/entitlement-license-contexts/{ctx_id}", headers=ha)
    assert got.status_code == 404


# ---------------------------------------------------------------------------
# E. Anchor validation
# ---------------------------------------------------------------------------

async def test_unknown_membership_is_404(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-UNK")
    resp = client.post(
        "/entitlement-license-contexts",
        json=_establish_license_body(str(uuid.uuid4())),
        headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)),
    )
    assert resp.status_code == 404


async def test_effective_to_must_be_after_effective_from(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-BADDATE")
    now = datetime.now(timezone.utc)
    resp = client.post(
        "/entitlement-license-contexts",
        json=_establish_license_body(
            str(s.membership.id),
            effective_from=now.isoformat(),
            effective_to=(now - timedelta(days=1)).isoformat(),
        ),
        headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)),
    )
    assert resp.status_code == 422


async def test_c023_license_type_rejects_full_light_and_junk(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-LT")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))
    for bad in ("FULL", "LIGHT", "NONSENSE"):
        resp = client.post("/entitlement-license-contexts",
                           json=_establish_license_body(str(s.membership.id), c023_license_type=bad), headers=h)
        assert resp.status_code == 422, bad
    assert (await db_session.execute(select(C023LicenseContext))).scalars().all() == []


# ---------------------------------------------------------------------------
# F. Decision 6 — membership.license_type untouched, never duplicated
# ---------------------------------------------------------------------------

async def test_decision_6_membership_license_type_untouched(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-D6")
    resp = client.post("/entitlement-license-contexts",
                       json=_establish_license_body(str(s.membership.id), c023_license_type="AUDITOR"),
                       headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)))
    assert resp.status_code == 201

    membership = await db_session.get(Membership, s.membership.id)
    assert membership.license_type == LicenseType.FULL.value  # unchanged by C-023

    row = (await db_session.execute(select(C023LicenseContext))).scalars().one()
    # No column anywhere stores a FULL/LIGHT value.
    stored = {v for v in row.__dict__.values() if isinstance(v, str)}
    assert "FULL" not in stored and "LIGHT" not in stored
    assert row.c023_license_type == "AUDITOR"


# ---------------------------------------------------------------------------
# G. Entitlement half — vacuously blocked (Decision 3 deferred)
# ---------------------------------------------------------------------------

async def test_entitlement_establish_is_vacuously_blocked(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-ENT")
    resp = client.post(
        "/entitlement-license-contexts",
        json={"organization_id": str(s.org.id), "entitlement_type_ref": "IFRS_ENABLED"},
        headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)),
    )
    assert resp.status_code == 422
    assert "Decision 3" in resp.json()["detail"]
    assert (await db_session.execute(select(C023EntitlementContext))).scalars().all() == []


async def test_entitlement_organization_id_must_match_tenant(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-ENT-X")
    resp = client.post(
        "/entitlement-license-contexts",
        json={"organization_id": str(uuid.uuid4()), "entitlement_type_ref": "IFRS_ENABLED"},
        headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)),
    )
    assert resp.status_code in (403, 422)


# ---------------------------------------------------------------------------
# H. audit
# ---------------------------------------------------------------------------

async def test_establish_emits_success_audit(client: TestClient, db_session: AsyncSession, monkeypatch) -> None:
    s = await _seed_org_with_bound_caller(db_session, code="ELC-AUD")
    captured: list[dict] = []

    import services.entitlement_license_establishment_service as svc

    real = svc.record_audit

    def _spy(**kwargs):
        captured.append(kwargs)
        return real(**kwargs)

    monkeypatch.setattr(svc, "record_audit", _spy)

    resp = client.post("/entitlement-license-contexts",
                       json=_establish_license_body(str(s.membership.id)),
                       headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)))
    assert resp.status_code == 201
    success = [c for c in captured if getattr(c.get("status"), "value", None) == "SUCCESS"]
    assert success, captured
    md = success[0]["metadata"]
    assert md["kind"] == "LICENSE"
    assert md["approval_authority_id"] == str(s.authority.id)
    assert success[0]["actor_id"] == str(s.person.id)
