"""
WP-10 BA-02 — Establish/Update Enterprise Configuration (EX-C041-02).
Service-layer tests for ConfigurationManagementService.establish().
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.configuration_entry import ConfigurationFacet, ConfigurationLifecycleState
from models.organization import Organization
from models.person import Person
from repositories.configuration_entry_repository import ConfigurationEntryRepository
from schemas.configuration import EstablishConfigurationEntryRequest
from services.configuration_management_service import ConfigurationManagementService


@pytest.fixture
async def seeded_organization_person(db_session: AsyncSession) -> tuple[Organization, Person]:
    organization = Organization(
        organization_code="CFG_MGMT_TEST_ORG", organization_name="Configuration Management Test Org", organization_type="CORPORATE",
    )
    person = Person(first_name="Ola", last_name="Fischer", display_name="Ola Fischer")
    db_session.add_all([organization, person])
    await db_session.flush()
    return organization, person


def _management_service(session: AsyncSession) -> ConfigurationManagementService:
    return ConfigurationManagementService(ConfigurationEntryRepository(session))


async def test_establish_creates_active_version_one(db_session: AsyncSession, seeded_organization_person) -> None:
    organization, person = seeded_organization_person

    result = await _management_service(db_session).establish(
        organization.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.BRANDING, key="logo_url", value="https://example.com/logo.png"),
        established_by_person_id=person.id,
    )

    assert result.version == 1
    assert result.lifecycle_state == ConfigurationLifecycleState.ACTIVE.value
    assert result.scope_level == "TENANT"
    assert result.organization_id == organization.id
    assert result.value == "https://example.com/logo.png"
    assert result.established_by_person_id == person.id


async def test_establish_again_supersedes_prior_active_version(
    db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person
    repo = ConfigurationEntryRepository(db_session)
    service = _management_service(db_session)

    first = await service.establish(
        organization.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.THEME, key="theme_class", value="DARK"),
        established_by_person_id=person.id,
    )
    await db_session.commit()

    second = await service.establish(
        organization.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.THEME, key="theme_class", value="HIGH_CONTRAST"),
        established_by_person_id=person.id,
    )
    await db_session.commit()

    assert second.version == 2
    assert second.value == "HIGH_CONTRAST"

    superseded = await repo.get_by_id(first.id)
    assert superseded is not None
    assert superseded.lifecycle_state == ConfigurationLifecycleState.SUPERSEDED.value
    assert superseded.effective_to is not None

    active = await repo.get_active_tenant_override(organization.id, ConfigurationFacet.THEME.value, "theme_class")
    assert active is not None
    assert active.id == second.id


async def test_establish_different_keys_do_not_interfere(
    db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person
    service = _management_service(db_session)

    await service.establish(
        organization.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.TERMINOLOGY, key="role.ceo", value="Managing Director"),
        established_by_person_id=person.id,
    )
    await db_session.commit()
    result = await service.establish(
        organization.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.TERMINOLOGY, key="role.cfo", value="Finance Director"),
        established_by_person_id=person.id,
    )

    assert result.version == 1

    entries = await service.list_established(organization.id)
    assert len(entries) == 2
    assert {e.key for e in entries} == {"role.ceo", "role.cfo"}


async def test_list_established_only_returns_active_entries(
    db_session: AsyncSession, seeded_organization_person
) -> None:
    organization, person = seeded_organization_person
    service = _management_service(db_session)

    await service.establish(
        organization.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.LOCALIZATION, key="default_language", value="fr"),
        established_by_person_id=person.id,
    )
    await db_session.commit()
    await service.establish(
        organization.id,
        EstablishConfigurationEntryRequest(facet=ConfigurationFacet.LOCALIZATION, key="default_language", value="de"),
        established_by_person_id=person.id,
    )
    await db_session.commit()

    entries = await service.list_established(organization.id)

    assert len(entries) == 1
    assert entries[0].value == "de"
    assert entries[0].version == 2
