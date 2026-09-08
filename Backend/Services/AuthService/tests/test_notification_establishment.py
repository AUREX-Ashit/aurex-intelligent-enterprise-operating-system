"""
C-132 Enterprise Notifications — WP-19 BA-01 ("Establish / Manage Enterprise
Notification Context") implementation tests.

Covers the WP-19 charter §18 test obligations and the CLAUDE.md §21.4
Mandatory Tenant-Isolation Test Checklist:

  * establish happy path + persistence + resulting UNREAD status
  * list — the caller's own notifications only, newest first
  * read — one by id, and the tenant-isolated / other-recipient 404
    (anti-enumeration, never 403)
  * acknowledge — UNREAD -> ACKNOWLEDGED, acknowledged_at set, idempotent
    re-acknowledge
  * lifecycle — no third state; acknowledge is one-directional
  * tenant isolation — two distinct, unrelated Organizations with no
    shared row:
      - a caller in Org A cannot establish a Notification against an
        Org B Membership (explicit foreign-identifier probe, §21.4(c))
      - a caller in Org A cannot read an Org B Notification (404)
      - a caller in Org A cannot acknowledge an Org B Notification (404)
      - list for an Org A caller never returns an Org B row
  * recipient/Membership integrity — establish against a nonexistent
    Membership -> 404
  * authorization — unauthenticated establish/list/read/acknowledge -> 400;
    PLATFORM_ADMIN may read/acknowledge any in-tenant notification
  * invalid input — bad severity / empty what_happened / empty source_type
    -> 422
  * audit — a SUCCESS record is emitted on establish and on acknowledge;
    Notification is never treated as an Audit Event
"""

import uuid
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.c132_notification import C132Notification
from models.membership import LicenseType, Membership
from models.organization import Organization
from models.person import Person
from models.role import Role


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
    def __init__(self, org: Organization, person: Person, membership: Membership) -> None:
        self.org = org
        self.person = person
        self.membership = membership


async def _seed_org_with_member(db_session: AsyncSession, *, code: str) -> _Seed:
    role = Role(role_code=f"ROLE_{code}", role_name=f"Role {code}")
    org = Organization(organization_code=code, organization_name=code, organization_type="CORPORATE")
    person = Person(first_name=code, last_name="Recipient", display_name=f"{code} Recipient")
    db_session.add_all([role, org, person])
    await db_session.flush()

    membership = Membership(
        person_id=person.id, organization_id=org.id, role_id=role.id,
        membership_status="ACTIVE", license_type=LicenseType.FULL.value,
    )
    db_session.add(membership)
    await db_session.flush()
    await db_session.commit()
    return _Seed(org, person, membership)


def _establish_body(membership_id: str, **extra) -> dict:
    body = {
        "membership_id": membership_id,
        "severity": "info",
        "what_happened": "Something happened.",
        "source_type": "TEST_SOURCE",
    }
    body.update(extra)
    return body


def _establish(client: TestClient, seed: _Seed, **extra):
    return client.post(
        "/notifications",
        json=_establish_body(str(seed.membership.id), **extra),
        headers=_headers(str(seed.org.id), person_id=str(seed.person.id), membership_id=str(seed.membership.id)),
    )


# ---------------------------------------------------------------------------
# A. establish — happy path + persistence
# ---------------------------------------------------------------------------

async def test_establish_happy_path(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-A")

    resp = _establish(
        client, s,
        severity="warning",
        what_happened="Your license was established.",
        why_it_matters="You now have access.",
        what_happens_next="No action required.",
        source_type="C023_LICENSE_CONTEXT",
        source_id=str(uuid.uuid4()),
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["membership_id"] == str(s.membership.id)
    assert body["severity"] == "warning"
    assert body["what_happened"] == "Your license was established."
    assert body["why_it_matters"] == "You now have access."
    assert body["what_happens_next"] == "No action required."
    assert body["source_type"] == "C023_LICENSE_CONTEXT"
    assert body["status"] == "UNREAD"
    assert body["acknowledged_at"] is None
    assert body["created_at"] is not None

    row = (await db_session.execute(select(C132Notification))).scalars().one()
    assert row.membership_id == s.membership.id
    assert row.status == "UNREAD"
    assert row.acknowledged_at is None


async def test_establish_optional_composition_elements_may_be_omitted(
    client: TestClient, db_session: AsyncSession
) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-OPT")
    resp = _establish(client, s)
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["why_it_matters"] is None
    assert body["what_happens_next"] is None
    assert body["source_id"] is None


# ---------------------------------------------------------------------------
# B. list — caller's own, newest first
# ---------------------------------------------------------------------------

async def test_list_returns_callers_own_newest_first(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-LIST")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))

    first = _establish(client, s, what_happened="first")
    second = _establish(client, s, what_happened="second")
    assert first.status_code == 201 and second.status_code == 201

    resp = client.get("/notifications", headers=h)
    assert resp.status_code == 200, resp.text
    items = resp.json()
    assert len(items) == 2
    assert items[0]["what_happened"] == "second"
    assert items[1]["what_happened"] == "first"


async def test_list_empty_when_caller_has_no_membership_in_tenant(
    client: TestClient, db_session: AsyncSession
) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-LE")
    _establish(client, s)

    # A caller with no Membership in this Organization.
    stranger_id = str(uuid.uuid4())
    resp = client.get(
        "/notifications",
        headers=_headers(str(s.org.id), person_id=stranger_id, membership_id=None),
    )
    assert resp.status_code == 200
    assert resp.json() == []


# ---------------------------------------------------------------------------
# C. read — one by id + anti-enumeration 404
# ---------------------------------------------------------------------------

async def test_read_by_id(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-R")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))
    nid = _establish(client, s).json()["id"]

    resp = client.get(f"/notifications/{nid}", headers=h)
    assert resp.status_code == 200
    assert resp.json()["id"] == nid


async def test_read_unknown_id_returns_404(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-R404")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))
    resp = client.get(f"/notifications/{uuid.uuid4()}", headers=h)
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# D. acknowledge — lifecycle + idempotency
# ---------------------------------------------------------------------------

async def test_acknowledge_transitions_unread_to_acknowledged(
    client: TestClient, db_session: AsyncSession
) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-ACK")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))
    nid = _establish(client, s).json()["id"]

    resp = client.post(f"/notifications/{nid}/acknowledge", headers=h)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "ACKNOWLEDGED"
    assert body["acknowledged_at"] is not None

    row = await db_session.get(C132Notification, uuid.UUID(nid))
    await db_session.refresh(row)
    assert row.status == "ACKNOWLEDGED"
    assert row.acknowledged_at is not None


async def test_acknowledge_is_idempotent(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-IDEM")
    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))
    nid = _establish(client, s).json()["id"]

    first = client.post(f"/notifications/{nid}/acknowledge", headers=h)
    assert first.status_code == 200 and first.json()["status"] == "ACKNOWLEDGED"
    row = (await db_session.execute(select(C132Notification))).scalars().one()
    await db_session.refresh(row)
    first_ack_at = row.acknowledged_at
    assert first_ack_at is not None

    second = client.post(f"/notifications/{nid}/acknowledge", headers=h)
    assert second.status_code == 200 and second.json()["status"] == "ACKNOWLEDGED"

    # Idempotent: still one row, still ACKNOWLEDGED, acknowledged_at untouched.
    rows = (await db_session.execute(select(C132Notification))).scalars().all()
    assert len(rows) == 1
    await db_session.refresh(rows[0])
    assert rows[0].status == "ACKNOWLEDGED"
    assert rows[0].acknowledged_at == first_ack_at


# ---------------------------------------------------------------------------
# E. tenant isolation — two unrelated Organizations, no shared row
# ---------------------------------------------------------------------------

async def test_establish_against_foreign_tenant_membership_is_rejected(
    client: TestClient, db_session: AsyncSession
) -> None:
    a = await _seed_org_with_member(db_session, code="NTF-ISO-A")
    b = await _seed_org_with_member(db_session, code="NTF-ISO-B")

    # Caller in Org A, X-Tenant-ID = Org A, but recipient membership is Org B's.
    resp = client.post(
        "/notifications",
        json=_establish_body(str(b.membership.id)),
        headers=_headers(str(a.org.id), person_id=str(a.person.id), membership_id=str(a.membership.id)),
    )
    assert resp.status_code == 403, resp.text
    assert (await db_session.execute(select(C132Notification))).scalars().first() is None


async def test_establish_with_forged_foreign_tenant_header_is_denied_and_writes_no_row(
    client: TestClient, db_session: AsyncSession
) -> None:
    """
    Gate 1 finding F-1 regression. The exact pre-fix attack: an
    authenticated caller whose OWN Organization is Org A forges
    `X-Tenant-ID = Org B` and supplies Org B's `membership_id`. Before the
    fix this returned 201 and persisted a row visible to Org B. After
    gating `POST /notifications` with
    `require_matching_tenant_or_platform_admin` (the WP-10 / `CERT-WP-10`
    Finding B-1 precedent), the caller's own `organization_id` claim (Org A)
    no longer matches `X-Tenant-ID` (Org B), so the request is denied at
    the dependency, before the route body runs — no row is created.
    """
    a = await _seed_org_with_member(db_session, code="NTF-F1-A")
    b = await _seed_org_with_member(db_session, code="NTF-F1-B")

    resp = client.post(
        "/notifications",
        json=_establish_body(str(b.membership.id)),
        headers=_headers(
            str(b.org.id),                 # forged X-Tenant-ID = Org B
            person_id=str(a.person.id),    # caller is Org A's person
            membership_id=str(a.membership.id),
            caller_org_id=str(a.org.id),   # caller's JWT organization_id = Org A
        ),
    )
    assert resp.status_code == 403, resp.text

    # No row anywhere — not for Org B, not for anyone.
    assert (await db_session.execute(select(C132Notification))).scalars().first() is None
    # And Org B's own recipient sees nothing.
    b_list = client.get(
        "/notifications",
        headers=_headers(str(b.org.id), person_id=str(b.person.id), membership_id=str(b.membership.id)),
    )
    assert b_list.status_code == 200 and b_list.json() == []


async def test_establish_denied_on_caller_tenant_mismatch_before_recipient_lookup(
    client: TestClient, db_session: AsyncSession
) -> None:
    """
    Demonstrates the binding is caller-vs-header, not merely
    membership-vs-header: an Org A caller forging `X-Tenant-ID = Org B` is
    denied even when `membership_id` is a random UUID that is never looked
    up (the 403 comes from the tenant-authority dependency, not the service
    layer's recipient validation).
    """
    a = await _seed_org_with_member(db_session, code="NTF-F1-MM-A")
    b = await _seed_org_with_member(db_session, code="NTF-F1-MM-B")

    resp = client.post(
        "/notifications",
        json=_establish_body(str(uuid.uuid4())),  # never resolved
        headers=_headers(
            str(b.org.id),
            person_id=str(a.person.id),
            membership_id=str(a.membership.id),
            caller_org_id=str(a.org.id),
        ),
    )
    assert resp.status_code == 403, resp.text
    assert (await db_session.execute(select(C132Notification))).scalars().first() is None


async def test_platform_admin_may_establish_across_tenants_but_recipient_must_match_header(
    client: TestClient, db_session: AsyncSession
) -> None:
    """
    PLATFORM_ADMIN behaviour stays consistent with the WP-10 tenant-authority
    precedent: a PLATFORM_ADMIN whose own `organization_id` claim does not
    match `X-Tenant-ID` may still establish — but the recipient Membership
    must still belong to `X-Tenant-ID` (the service-layer check is
    unchanged).
    """
    admin_home = await _seed_org_with_member(db_session, code="NTF-PA-HOME")
    target = await _seed_org_with_member(db_session, code="NTF-PA-TGT")
    other = await _seed_org_with_member(db_session, code="NTF-PA-OTH")

    admin_h = _headers(
        str(target.org.id),                    # X-Tenant-ID = target org
        person_id=str(uuid.uuid4()),
        membership_id=None,
        caller_org_id=str(admin_home.org.id),  # admin's own org is a different one
        role_code="PLATFORM_ADMIN",
    )

    ok = client.post("/notifications", json=_establish_body(str(target.membership.id)), headers=admin_h)
    assert ok.status_code == 201, ok.text
    assert ok.json()["membership_id"] == str(target.membership.id)

    # Recipient in a third org, while X-Tenant-ID is the target org -> still 403.
    bad = client.post("/notifications", json=_establish_body(str(other.membership.id)), headers=admin_h)
    assert bad.status_code == 403, bad.text


async def test_read_other_tenant_notification_returns_404(
    client: TestClient, db_session: AsyncSession
) -> None:
    a = await _seed_org_with_member(db_session, code="NTF-ISO-RA")
    b = await _seed_org_with_member(db_session, code="NTF-ISO-RB")

    b_nid = client.post(
        "/notifications",
        json=_establish_body(str(b.membership.id)),
        headers=_headers(str(b.org.id), person_id=str(b.person.id), membership_id=str(b.membership.id)),
    ).json()["id"]

    # Org A caller tries to read Org B's notification id.
    resp = client.get(
        f"/notifications/{b_nid}",
        headers=_headers(str(a.org.id), person_id=str(a.person.id), membership_id=str(a.membership.id)),
    )
    assert resp.status_code == 404


async def test_acknowledge_other_tenant_notification_returns_404(
    client: TestClient, db_session: AsyncSession
) -> None:
    a = await _seed_org_with_member(db_session, code="NTF-ISO-AA")
    b = await _seed_org_with_member(db_session, code="NTF-ISO-AB")

    b_nid = client.post(
        "/notifications",
        json=_establish_body(str(b.membership.id)),
        headers=_headers(str(b.org.id), person_id=str(b.person.id), membership_id=str(b.membership.id)),
    ).json()["id"]

    resp = client.post(
        f"/notifications/{b_nid}/acknowledge",
        headers=_headers(str(a.org.id), person_id=str(a.person.id), membership_id=str(a.membership.id)),
    )
    assert resp.status_code == 404

    row = await db_session.get(C132Notification, uuid.UUID(b_nid))
    await db_session.refresh(row)
    assert row.status == "UNREAD"


async def test_list_never_returns_another_tenants_row(client: TestClient, db_session: AsyncSession) -> None:
    a = await _seed_org_with_member(db_session, code="NTF-ISO-LA")
    b = await _seed_org_with_member(db_session, code="NTF-ISO-LB")

    client.post(
        "/notifications",
        json=_establish_body(str(b.membership.id), what_happened="b-only"),
        headers=_headers(str(b.org.id), person_id=str(b.person.id), membership_id=str(b.membership.id)),
    )

    resp = client.get(
        "/notifications",
        headers=_headers(str(a.org.id), person_id=str(a.person.id), membership_id=str(a.membership.id)),
    )
    assert resp.status_code == 200
    assert resp.json() == []


async def test_other_recipient_same_tenant_cannot_read_or_acknowledge(
    client: TestClient, db_session: AsyncSession
) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-OR")
    # A second person + membership in the SAME organization.
    other_person = Person(first_name="Other", last_name="Member", display_name="Other Member")
    db_session.add(other_person)
    await db_session.flush()
    other_membership = Membership(
        person_id=other_person.id, organization_id=s.org.id, role_id=s.membership.role_id,
        membership_status="ACTIVE", license_type=LicenseType.FULL.value,
    )
    db_session.add(other_membership)
    await db_session.flush()
    await db_session.commit()

    nid = _establish(client, s).json()["id"]

    other_h = _headers(str(s.org.id), person_id=str(other_person.id), membership_id=str(other_membership.id))
    assert client.get(f"/notifications/{nid}", headers=other_h).status_code == 404
    assert client.post(f"/notifications/{nid}/acknowledge", headers=other_h).status_code == 404


# ---------------------------------------------------------------------------
# F. recipient / Membership integrity
# ---------------------------------------------------------------------------

async def test_establish_against_unknown_membership_returns_404(
    client: TestClient, db_session: AsyncSession
) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-NOMEM")
    resp = client.post(
        "/notifications",
        json=_establish_body(str(uuid.uuid4())),
        headers=_headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id)),
    )
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# G. authorization
# ---------------------------------------------------------------------------

async def test_unauthenticated_requests_are_rejected(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-NOAUTH")
    only_tenant = {"X-Tenant-ID": str(s.org.id)}
    assert client.post("/notifications", json=_establish_body(str(s.membership.id)), headers=only_tenant).status_code == 400
    assert client.get("/notifications", headers=only_tenant).status_code == 400
    assert client.get(f"/notifications/{uuid.uuid4()}", headers=only_tenant).status_code == 400
    assert client.post(f"/notifications/{uuid.uuid4()}/acknowledge", headers=only_tenant).status_code == 400


async def test_missing_tenant_header_is_rejected(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-NOTEN")
    only_auth = {"Authorization": f"Bearer {_access_token(str(s.person.id), str(s.org.id), str(s.membership.id))}"}
    assert client.get("/notifications", headers=only_auth).status_code == 400


async def test_platform_admin_may_read_and_acknowledge_any_in_tenant_notification(
    client: TestClient, db_session: AsyncSession
) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-PA")
    nid = _establish(client, s).json()["id"]

    admin_h = _headers(
        str(s.org.id), person_id=str(uuid.uuid4()), membership_id=None, role_code="PLATFORM_ADMIN",
    )
    assert client.get(f"/notifications/{nid}", headers=admin_h).status_code == 200
    ack = client.post(f"/notifications/{nid}/acknowledge", headers=admin_h)
    assert ack.status_code == 200
    assert ack.json()["status"] == "ACKNOWLEDGED"


async def test_platform_admin_cannot_reach_across_tenants(client: TestClient, db_session: AsyncSession) -> None:
    a = await _seed_org_with_member(db_session, code="NTF-PA-A")
    b = await _seed_org_with_member(db_session, code="NTF-PA-B")
    b_nid = client.post(
        "/notifications",
        json=_establish_body(str(b.membership.id)),
        headers=_headers(str(b.org.id), person_id=str(b.person.id), membership_id=str(b.membership.id)),
    ).json()["id"]

    # PLATFORM_ADMIN acting with X-Tenant-ID = Org A must still not see Org B's row.
    admin_h = _headers(str(a.org.id), person_id=str(uuid.uuid4()), membership_id=None, role_code="PLATFORM_ADMIN")
    assert client.get(f"/notifications/{b_nid}", headers=admin_h).status_code == 404


# ---------------------------------------------------------------------------
# H. invalid input
# ---------------------------------------------------------------------------

async def test_invalid_severity_is_rejected(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-BADSEV")
    resp = _establish(client, s, severity="critical")
    assert resp.status_code == 422


async def test_empty_what_happened_is_rejected(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-EMPTY")
    resp = _establish(client, s, what_happened="")
    assert resp.status_code == 422


async def test_empty_source_type_is_rejected(client: TestClient, db_session: AsyncSession) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-NOSRC")
    resp = _establish(client, s, source_type="")
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# I. audit
# ---------------------------------------------------------------------------

async def test_establish_and_acknowledge_emit_success_audit(
    client: TestClient, db_session: AsyncSession, monkeypatch
) -> None:
    s = await _seed_org_with_member(db_session, code="NTF-AUD")
    captured: list[dict] = []

    import services.notification_establishment_service as svc

    real = svc.record_audit

    def _spy(**kwargs):
        captured.append(kwargs)
        return real(**kwargs)

    monkeypatch.setattr(svc, "record_audit", _spy)

    h = _headers(str(s.org.id), person_id=str(s.person.id), membership_id=str(s.membership.id))
    nid = client.post("/notifications", json=_establish_body(str(s.membership.id)), headers=h).json()["id"]
    client.post(f"/notifications/{nid}/acknowledge", headers=h)

    actions = {
        c["action"]
        for c in captured
        if getattr(c.get("status"), "value", None) == "SUCCESS"
    }
    assert "ESTABLISH_NOTIFICATION" in actions, captured
    assert "ACKNOWLEDGE_NOTIFICATION" in actions, captured
    est = next(c for c in captured if c["action"] == "ESTABLISH_NOTIFICATION")
    assert est["actor_id"] == str(s.person.id)
    assert est["tenant_id"] == str(s.org.id)
    assert est["metadata"]["membership_id"] == str(s.membership.id)
