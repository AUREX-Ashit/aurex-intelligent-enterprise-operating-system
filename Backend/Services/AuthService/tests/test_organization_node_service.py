import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.organization_node import EstablishOrganizationNodeRequest
from services.organization_node_service import OrganizationNodeService


def _service(session: AsyncSession) -> OrganizationNodeService:
    return OrganizationNodeService(OrganizationNodeRepository(session))


async def test_establish_creates_organization_node_with_structural_identity_fields(
    db_session: AsyncSession,
) -> None:
    """
    Business Activity Contract (WP-04 BA-01, IRA-004 §9/§11): a first-time
    Establish Organization Node call creates exactly one row, persisting
    only the Structural Identity column subset scoped for BA-01.
    """
    service = _service(db_session)
    request = EstablishOrganizationNodeRequest(
        node_code="APAC-HOLD-001",
        node_name="APAC Holding",
        node_type="HOLDING",
        legal_entity_name="Acme APAC Holdings Pte Ltd",
        business_unit="APAC Operations",
        sector="Manufacturing",
        operational_status="ACTIVE",
    )

    node = await service.establish(request, actor_id="platform-admin-1")

    assert node.node_code == "APAC-HOLD-001"
    assert node.node_name == "APAC Holding"
    assert node.node_type == "HOLDING"
    assert node.legal_entity_name == "Acme APAC Holdings Pte Ltd"
    assert node.business_unit == "APAC Operations"
    assert node.sector == "Manufacturing"
    assert node.operational_status == "ACTIVE"
    assert node.active_flag is True
    assert node.id is not None


async def test_establish_allows_optional_structural_identity_fields_to_be_omitted(
    db_session: AsyncSession,
) -> None:
    """Only node_code/node_name/node_type are required — the remaining Structural Identity fields are optional."""
    service = _service(db_session)
    request = EstablishOrganizationNodeRequest(
        node_code="APAC-HOLD-002",
        node_name="APAC Subsidiary",
        node_type="ENTITY",
    )

    node = await service.establish(request)

    assert node.legal_entity_name is None
    assert node.business_unit is None
    assert node.sector is None
    assert node.operational_status is None
    assert node.effective_from is None
    assert node.effective_to is None


async def test_establish_rejects_duplicate_node_code(db_session: AsyncSession) -> None:
    """
    Business Rule (ERG-001-02): node_code is unique platform-wide. A
    second Establish Organization Node call for the same code is
    rejected (409), not silently deduplicated and not permitted to
    create a second row.
    """
    service = _service(db_session)
    request = EstablishOrganizationNodeRequest(
        node_code="APAC-HOLD-003",
        node_name="APAC Holding",
        node_type="HOLDING",
    )
    await service.establish(request)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 409


async def test_establish_organization_node_output_is_a_valid_membership_home_node(
    db_session: AsyncSession,
) -> None:
    """
    TD-032's own resolution criterion (IRA-004 §16): a Membership's
    home_node_id can now reference a real, governed Establish Organization
    Node output — not only a node created directly in a test fixture, as
    every WP-03 membership test did before this Business Activity existed.
    """
    from models.membership import Membership
    from models.organization import Organization
    from models.person import Person
    from models.role import Role

    node_service = _service(db_session)
    node = await node_service.establish(
        EstablishOrganizationNodeRequest(
            node_code="APAC-HOLD-004",
            node_name="APAC Holding",
            node_type="HOLDING",
        )
    )

    person = Person(first_name="Ada", last_name="Lovelace", display_name="Ada Lovelace")
    organization = Organization(
        organization_code="WP04_TEST_ORG", organization_name="WP-04 Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="WP04_TEST_ROLE", role_name="WP-04 Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(
        person_id=person.id, organization_id=organization.id, role_id=role.id, home_node_id=node.id,
    )
    db_session.add(membership)
    await db_session.flush()

    assert membership.home_node_id == node.id


# ---------------------------------------------------------------------------
# BA-02 — Understand Structural Position
# ---------------------------------------------------------------------------

async def test_get_details_returns_the_established_organization_node(db_session: AsyncSession) -> None:
    """BA-02: fetching by id returns exactly the node created by BA-01's establish()."""
    service = _service(db_session)
    created = await service.establish(
        EstablishOrganizationNodeRequest(
            node_code="APAC-HOLD-005",
            node_name="APAC Holding Fifth",
            node_type="HOLDING",
            legal_entity_name="Acme APAC Fifth Pte Ltd",
        )
    )

    fetched = await service.get_details(created.id)

    assert fetched.id == created.id
    assert fetched.node_code == "APAC-HOLD-005"
    assert fetched.node_name == "APAC Holding Fifth"
    assert fetched.legal_entity_name == "Acme APAC Fifth Pte Ltd"


async def test_get_details_raises_404_for_unknown_id(db_session: AsyncSession) -> None:
    """BA-02: a well-formed but non-existent id is a 404, not a 500 or an empty success."""
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_details(uuid.uuid4())

    assert exc_info.value.status_code == 404
