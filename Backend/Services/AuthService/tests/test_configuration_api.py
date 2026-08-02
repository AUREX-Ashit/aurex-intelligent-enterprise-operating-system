"""
WP-10 BA-01/BA-02 — Resolve / Establish Enterprise Configuration
(EX-C041-01/02). API-level tests, including the Mandatory
Tenant-Isolation Test Checklist (CLAUDE.md §21.4) — a submission gate
for every endpoint carrying an organization/tenant boundary, not a
reactive finding (directly evidenced by VV-AUDIT-WP-05's F-02 and
VV-AUDIT-WP-09's Finding 2 both independently finding the same root
cause when this checklist was absent).
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.organization import Organization
from models.person import Person


def _access_token(person_id: str, organization_id: str, role_code: str = "ESG_MANAGER") -> str:
    """Mirrors test_workspace_api.py's own _access_token() convention."""
    claims = {
        "person_id": person_id,
        "identity_id": str(uuid.uuid4()),
        "organization_id": organization_id,
        "membership_id": str(uuid.uuid4()),
        "role_code": role_code,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _headers(
    person_id: str,
    organization_id: str | None,
    role_code: str = "ESG_MANAGER",
    claims_organization_id: str | None = None,
) -> dict[str, str]:
    """
    By default, the caller's own JWT `organization_id` claim matches the
    `X-Tenant-ID` header sent — the realistic case (a caller resolving
    their own tenant). Pass `claims_organization_id` explicitly to
    construct a genuine mismatch (a caller asserting a different tenant
    than their own JWT claims), exercising
    `require_matching_tenant_or_platform_admin` (`CERT-WP-10` Finding
    B-1 — the cross-tenant disclosure this dependency closes).
    """
    token_organization_id = claims_organization_id if claims_organization_id is not None else (organization_id or str(uuid.uuid4()))
    headers = {"Authorization": f"Bearer {_access_token(person_id, token_organization_id, role_code)}"}
    if organization_id is not None:
        headers["X-Tenant-ID"] = organization_id
    return headers


@pytest.fixture
async def seeded_organization_person(db_session: AsyncSession) -> tuple[Organization, Person]:
    organization = Organization(
        organization_code="CFG_API_TEST_ORG", organization_name="Configuration API Test Org", organization_type="CORPORATE",
    )
    person = Person(first_name="Rio", last_name="Bianchi", display_name="Rio Bianchi")
    db_session.add_all([organization, person])
    await db_session.flush()
    await db_session.commit()
    return organization, person


# ---------------------------------------------------------------------------
# BA-01 — GET /configuration (EX-C041-01)
# ---------------------------------------------------------------------------

def test_resolve_requires_authentication(client: TestClient) -> None:
    response = client.get("/configuration")
    assert response.status_code == 400


def test_resolve_requires_tenant_header(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    """
    Unlike /workspaces (deliberately exempted), /configuration is NOT
    exempted from TenantMiddleware — the inverse of
    test_workspace_api.py's own test_get_candidates_does_not_require_
    tenant_header, proving the deliberate design difference documented in
    middleware/tenant.py's own new /configuration comment block.
    """
    _organization, person = seeded_organization_person

    response = client.get("/configuration", headers=_headers(str(person.id), organization_id=None))

    assert response.status_code == 400
    assert response.json().get("message", "").startswith("Header 'X-Tenant-ID'")


def test_resolve_is_open_to_any_authenticated_caller_not_only_platform_admin(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person

    response = client.get("/configuration", headers=_headers(str(person.id), str(organization.id), role_code="ESG_MANAGER"))

    assert response.status_code == 200


def test_resolve_rejects_mismatched_tenant_for_non_admin(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    """
    CERT-WP-10 Finding B-1 (blocking): without
    require_matching_tenant_or_platform_admin, a non-admin caller could
    read an arbitrary Organization's Configuration simply by naming its
    UUID in X-Tenant-ID, regardless of their own JWT organization_id
    claim. A caller whose own claims name a different Organization than
    the one they assert via X-Tenant-ID must be rejected.
    """
    organization, person = seeded_organization_person
    own_organization_id = str(uuid.uuid4())

    response = client.get(
        "/configuration",
        headers=_headers(str(person.id), str(organization.id), claims_organization_id=own_organization_id),
    )

    assert response.status_code == 403


def test_resolve_allows_platform_admin_to_view_a_different_tenant(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person
    own_organization_id = str(uuid.uuid4())

    response = client.get(
        "/configuration",
        headers=_headers(
            str(person.id), str(organization.id), role_code="PLATFORM_ADMIN", claims_organization_id=own_organization_id
        ),
    )

    assert response.status_code == 200


def test_resolve_returns_platform_defaults_when_no_overrides_established(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person

    response = client.get("/configuration", headers=_headers(str(person.id), str(organization.id)))

    assert response.status_code == 200
    body = response.json()
    theme_values = {v["key"]: v for v in body["facets"]["THEME"]}
    assert theme_values["theme_class"]["value"] == "LIGHT"
    assert theme_values["theme_class"]["source"] == "PLATFORM_DEFAULT"


def test_resolve_accepts_facet_filter(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person

    response = client.get(
        "/configuration?facet=THEME", headers=_headers(str(person.id), str(organization.id))
    )

    assert response.status_code == 200
    assert list(response.json()["facets"].keys()) == ["THEME"]


# ---------------------------------------------------------------------------
# BA-02 — POST /configuration (EX-C041-02)
# ---------------------------------------------------------------------------

def test_establish_requires_platform_admin(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person

    response = client.post(
        "/configuration",
        headers=_headers(str(person.id), str(organization.id), role_code="ESG_MANAGER"),
        json={"facet": "THEME", "key": "theme_class", "value": "DARK"},
    )

    assert response.status_code == 403


def test_establish_creates_active_tenant_override(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person

    response = client.post(
        "/configuration",
        headers=_headers(str(person.id), str(organization.id), role_code="PLATFORM_ADMIN"),
        json={"facet": "THEME", "key": "theme_class", "value": "DARK"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["version"] == 1
    assert body["lifecycle_state"] == "ACTIVE"
    assert body["organization_id"] == str(organization.id)


def test_resolve_reflects_established_override(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person
    client.post(
        "/configuration",
        headers=_headers(str(person.id), str(organization.id), role_code="PLATFORM_ADMIN"),
        json={"facet": "THEME", "key": "theme_class", "value": "DARK"},
    )

    response = client.get("/configuration?facet=THEME", headers=_headers(str(person.id), str(organization.id)))

    theme_class = response.json()["facets"]["THEME"][0]
    assert theme_class["value"] == "DARK"
    assert theme_class["source"] == "TENANT"
    assert theme_class["version"] == 1


def test_list_entries_requires_platform_admin(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person

    response = client.get(
        "/configuration/entries", headers=_headers(str(person.id), str(organization.id), role_code="ESG_MANAGER")
    )

    assert response.status_code == 403


def test_list_entries_returns_established_overrides(
    client: TestClient, db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person
    admin_headers = _headers(str(person.id), str(organization.id), role_code="PLATFORM_ADMIN")
    client.post("/configuration", headers=admin_headers, json={"facet": "THEME", "key": "theme_class", "value": "DARK"})
    client.post("/configuration", headers=admin_headers, json={"facet": "LOCALIZATION", "key": "default_language", "value": "fr"})

    response = client.get("/configuration/entries", headers=admin_headers)

    assert response.status_code == 200
    entries = response.json()["entries"]
    assert len(entries) == 2
    assert {e["key"] for e in entries} == {"theme_class", "default_language"}


# ---------------------------------------------------------------------------
# Mandatory Tenant-Isolation Test Checklist (CLAUDE.md §21.4)
# ---------------------------------------------------------------------------

class TestConfigurationTenantIsolation:
    """
    Two-tenant negative control: establishing a Configuration override for
    one Organization must never be visible to a different Organization,
    at either the resolve (BA-01) or establish/list (BA-02) endpoints —
    the exact defect class VV-AUDIT-WP-05 F-02 and VV-AUDIT-WP-09 Finding
    2 each independently found, now a submission gate rather than a
    reactive finding.
    """

    @pytest.fixture
    async def seeded_two_organizations(self, db_session: AsyncSession) -> tuple[Organization, Organization, Person]:
        organization_a = Organization(
            organization_code="CFG_TENANT_ISO_ORG_A", organization_name="Tenant Isolation Org A", organization_type="CORPORATE",
        )
        organization_b = Organization(
            organization_code="CFG_TENANT_ISO_ORG_B", organization_name="Tenant Isolation Org B", organization_type="CORPORATE",
        )
        person = Person(first_name="Isla", last_name="Kowalski", display_name="Isla Kowalski")
        db_session.add_all([organization_a, organization_b, person])
        await db_session.flush()
        await db_session.commit()
        return organization_a, organization_b, person

    def test_established_override_is_not_visible_when_resolving_a_different_tenant(
        self, client: TestClient, db_session: AsyncSession, seeded_two_organizations
    ) -> None:
        organization_a, organization_b, person = seeded_two_organizations
        client.post(
            "/configuration",
            headers=_headers(str(person.id), str(organization_a.id), role_code="PLATFORM_ADMIN"),
            json={"facet": "THEME", "key": "theme_class", "value": "BOARDROOM"},
        )

        response_b = client.get(
            "/configuration?facet=THEME", headers=_headers(str(person.id), str(organization_b.id))
        )

        theme_class_b = response_b.json()["facets"]["THEME"][0]
        assert theme_class_b["value"] == "LIGHT"
        assert theme_class_b["source"] == "PLATFORM_DEFAULT"

    def test_outsider_with_no_relationship_to_org_cannot_resolve_its_configuration(
        self, client: TestClient, db_session: AsyncSession, seeded_two_organizations
    ) -> None:
        """
        CERT-WP-10 Finding B-1's own direct reproduction: an authenticated
        Person whose own JWT organization_id claim names neither
        Organization must not be able to read Organization A's
        Configuration merely by naming its UUID in X-Tenant-ID — the exact
        probe the Independent Certification agent used to confirm the
        original defect (a bare UUID header, unconnected to the caller's
        own claims, previously granted a 200).
        """
        organization_a, _organization_b, person = seeded_two_organizations
        client.post(
            "/configuration",
            headers=_headers(str(person.id), str(organization_a.id), role_code="PLATFORM_ADMIN"),
            json={"facet": "THEME", "key": "theme_class", "value": "BOARDROOM"},
        )

        outsider_id = str(uuid.uuid4())
        outsider_own_org = str(uuid.uuid4())
        response = client.get(
            "/configuration?facet=THEME",
            headers=_headers(outsider_id, str(organization_a.id), claims_organization_id=outsider_own_org),
        )

        assert response.status_code == 403

    def test_established_override_is_not_listed_under_a_different_tenant(
        self, client: TestClient, db_session: AsyncSession, seeded_two_organizations
    ) -> None:
        organization_a, organization_b, person = seeded_two_organizations
        client.post(
            "/configuration",
            headers=_headers(str(person.id), str(organization_a.id), role_code="PLATFORM_ADMIN"),
            json={"facet": "BRANDING", "key": "logo_url", "value": "https://a.example.com/logo.png"},
        )

        response_b = client.get(
            "/configuration/entries", headers=_headers(str(person.id), str(organization_b.id), role_code="PLATFORM_ADMIN")
        )

        assert response_b.json()["entries"] == []

    def test_each_tenant_can_independently_establish_the_same_key(
        self, client: TestClient, db_session: AsyncSession, seeded_two_organizations
    ) -> None:
        organization_a, organization_b, person = seeded_two_organizations
        client.post(
            "/configuration",
            headers=_headers(str(person.id), str(organization_a.id), role_code="PLATFORM_ADMIN"),
            json={"facet": "THEME", "key": "theme_class", "value": "DARK"},
        )
        client.post(
            "/configuration",
            headers=_headers(str(person.id), str(organization_b.id), role_code="PLATFORM_ADMIN"),
            json={"facet": "THEME", "key": "theme_class", "value": "HIGH_CONTRAST"},
        )

        response_a = client.get("/configuration?facet=THEME", headers=_headers(str(person.id), str(organization_a.id)))
        response_b = client.get("/configuration?facet=THEME", headers=_headers(str(person.id), str(organization_b.id)))

        assert response_a.json()["facets"]["THEME"][0]["value"] == "DARK"
        assert response_b.json()["facets"]["THEME"][0]["value"] == "HIGH_CONTRAST"
