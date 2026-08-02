"""
WP-10 BA-01 — Resolve Enterprise Configuration (EX-C041-01).
Service-layer tests for ConfigurationResolutionService.resolve().
"""
import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.configuration_entry import ConfigurationFacet
from models.organization import Organization
from models.person import Person
from repositories.configuration_entry_repository import ConfigurationEntryRepository
from schemas.configuration import ConfigurationSource, EstablishConfigurationEntryRequest
from services.configuration_management_service import ConfigurationManagementService
from services.configuration_resolution_service import ConfigurationResolutionService


@pytest.fixture
async def seeded_organization_person(db_session: AsyncSession) -> tuple[Organization, Person]:
    organization = Organization(
        organization_code="CFG_RESOLVE_TEST_ORG", organization_name="Configuration Resolve Test Org", organization_type="CORPORATE",
    )
    person = Person(first_name="Nadia", last_name="Torres", display_name="Nadia Torres")
    db_session.add_all([organization, person])
    await db_session.flush()
    return organization, person


def _resolution_service(session: AsyncSession) -> ConfigurationResolutionService:
    return ConfigurationResolutionService(ConfigurationEntryRepository(session))


def _management_service(session: AsyncSession) -> ConfigurationManagementService:
    return ConfigurationManagementService(ConfigurationEntryRepository(session))


async def test_resolve_returns_platform_defaults_when_no_overrides_exist(
    db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person

    bundle = await _resolution_service(db_session).resolve(organization.id, person.id, facets=None)

    theme_values = {v.key: v for v in bundle.facets[ConfigurationFacet.THEME.value]}
    assert theme_values["theme_class"].value == "LIGHT"
    assert theme_values["theme_class"].source == ConfigurationSource.PLATFORM_DEFAULT
    assert theme_values["theme_class"].version is None

    localization_values = {v.key: v for v in bundle.facets[ConfigurationFacet.LOCALIZATION.value]}
    assert localization_values["default_language"].value == "en"

    # Terminology has an open-ended key space and no platform default keys —
    # empty until an enterprise establishes at least one term override.
    assert bundle.facets[ConfigurationFacet.TERMINOLOGY.value] == []


async def test_resolve_prefers_tenant_override_over_platform_default(
    db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person
    await _management_service(db_session).establish(
        organization.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.THEME, key="theme_class", value="DARK"),
        established_by_person_id=person.id,
    )
    await db_session.commit()

    bundle = await _resolution_service(db_session).resolve(organization.id, person.id, facets=[ConfigurationFacet.THEME.value])

    theme_class = bundle.facets[ConfigurationFacet.THEME.value][0]
    assert theme_class.value == "DARK"
    assert theme_class.source == ConfigurationSource.TENANT
    assert theme_class.version == 1


async def test_resolve_restricts_to_requested_facets(
    db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person

    bundle = await _resolution_service(db_session).resolve(
        organization.id, person.id, facets=[ConfigurationFacet.THEME.value]
    )

    assert list(bundle.facets.keys()) == [ConfigurationFacet.THEME.value]


async def test_resolve_returns_established_terminology_override(
    db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person
    await _management_service(db_session).establish(
        organization.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.TERMINOLOGY, key="role.ceo", value="Managing Director"),
        established_by_person_id=person.id,
    )
    await db_session.commit()

    bundle = await _resolution_service(db_session).resolve(
        organization.id, person.id, facets=[ConfigurationFacet.TERMINOLOGY.value]
    )

    term = bundle.facets[ConfigurationFacet.TERMINOLOGY.value][0]
    assert term.key == "role.ceo"
    assert term.value == "Managing Director"
    assert term.source == ConfigurationSource.TENANT


async def test_resolve_never_leaks_a_different_organizations_override(
    db_session: AsyncSession, seeded_organization_person
) -> None:
    """
    Mandatory Tenant-Isolation checklist (CLAUDE.md §21.4) — the same
    negative-control shape as test_configuration_api.py's own API-level
    version, at the service layer: establishing an override for one
    Organization must never be visible when resolving a different
    Organization's own Configuration.
    """
    organization_a, person = seeded_organization_person
    organization_b = Organization(
        organization_code="CFG_RESOLVE_TEST_ORG_B", organization_name="Configuration Resolve Test Org B", organization_type="CORPORATE",
    )
    db_session.add(organization_b)
    await db_session.flush()

    await _management_service(db_session).establish(
        organization_a.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.THEME, key="theme_class", value="BOARDROOM"),
        established_by_person_id=person.id,
    )
    await db_session.commit()

    bundle_b = await _resolution_service(db_session).resolve(
        organization_b.id, uuid.uuid4(), facets=[ConfigurationFacet.THEME.value]
    )

    theme_class_b = bundle_b.facets[ConfigurationFacet.THEME.value][0]
    assert theme_class_b.value == "LIGHT"
    assert theme_class_b.source == ConfigurationSource.PLATFORM_DEFAULT
