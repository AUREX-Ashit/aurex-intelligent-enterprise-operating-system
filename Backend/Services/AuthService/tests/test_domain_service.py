import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.domain_repository import DomainRepository
from services.domain_service import DomainService


def _service(session: AsyncSession) -> DomainService:
    return DomainService(DomainRepository(session))


async def _seed_domain(repo: DomainRepository, **kwargs):
    domain = await repo.create(kwargs)
    await repo.session.flush()
    return domain


async def test_list_domains_returns_platform_defaults_only_with_no_org_filter(
    db_session: AsyncSession,
) -> None:
    """
    With no organization_id supplied, list_domains() returns only the
    platform-default catalog (organization_id IS NULL, URA-001-43) — a
    tenant-added domain from a different organization must not leak in.
    """
    repo = DomainRepository(db_session)
    await _seed_domain(repo, domain_name="Finance")
    await _seed_domain(
        repo,
        domain_name="Tenant Custom Domain",
        organization_id=uuid.uuid4(),
    )
    service = DomainService(repo)

    domains = await service.list_domains(organization_id=None)

    names = {d.domain_name for d in domains}
    assert "Finance" in names
    assert "Tenant Custom Domain" not in names


async def test_list_domains_includes_tenant_added_domains_when_org_supplied(
    db_session: AsyncSession,
) -> None:
    """
    Supplying organization_id returns the platform defaults plus that
    tenant's own added domains (URA-001-43), mirroring
    business_role_registry's NULL-is-global visibility rule.
    """
    repo = DomainRepository(db_session)
    org_id = uuid.uuid4()
    await _seed_domain(repo, domain_name="Finance")
    await _seed_domain(repo, domain_name="Tenant Custom Domain", organization_id=org_id)
    service = DomainService(repo)

    domains = await service.list_domains(organization_id=org_id)

    names = {d.domain_name for d in domains}
    assert "Finance" in names
    assert "Tenant Custom Domain" in names


async def test_get_details_resolves_an_existing_domain(db_session: AsyncSession) -> None:
    """Realizes PE-001-C003 EX-C003-02's Entry Context: the target Domain, already established."""
    repo = DomainRepository(db_session)
    domain = await _seed_domain(repo, domain_name="Risk")
    service = DomainService(repo)

    resolved = await service.get_details(domain.id)

    assert resolved.id == domain.id
    assert resolved.domain_name == "Risk"


async def test_get_details_raises_404_for_unknown_domain(db_session: AsyncSession) -> None:
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_details(uuid.uuid4())

    assert exc_info.value.status_code == 404


async def test_domain_hierarchy_self_reference(db_session: AsyncSession) -> None:
    """URA-001-44: sub-domains reference their parent via parent_domain_id."""
    repo = DomainRepository(db_session)
    finance = await _seed_domain(repo, domain_name="Finance")
    await db_session.flush()
    accounting = await _seed_domain(
        repo, domain_name="Accounting", parent_domain_id=finance.id
    )

    assert accounting.parent_domain_id == finance.id
