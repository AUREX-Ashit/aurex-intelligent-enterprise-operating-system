# tests/test_search_unit.py
"""WP-11 — Enterprise Search (C-093) unit tests, BA-01/02/03 (`IRA-011 §5`/§10) — service/repository layer, direct DB session, no HTTP."""
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.search_repository import (
    DocumentChunkRegistryRepository,
    EvidenceRegistryRepository,
    VectorIndexRegistryRepository,
)
from schemas.search import EstablishIndexConfigurationRequest, RegisterContentRequest
from services.content_registration_service import ContentRegistrationService, _fixed_size_chunks
from services.search_index_service import SearchIndexConfigurationService


def test_fixed_size_chunks_splits_and_strips():
    assert _fixed_size_chunks("   ") == []
    chunks = _fixed_size_chunks("a" * 2500, chunk_size=1000)
    assert len(chunks) == 3
    assert len(chunks[0]) == 1000
    assert len(chunks[-1]) == 500


@pytest.mark.asyncio
async def test_establish_writes_tenant_scoped_row_by_default(db_session: AsyncSession):
    org = uuid4()
    service = SearchIndexConfigurationService(VectorIndexRegistryRepository(db_session))
    response = await service.establish(
        org,
        EstablishIndexConfigurationRequest(
            index_name="unit-test-index", embedding_model="text-embedding-3-large", embedding_dimension=1536
        ),
    )
    assert response.organization_id == org
    assert response.active_flag is True
    assert response.retrieval_mode == "HYBRID"


@pytest.mark.asyncio
async def test_establish_platform_wide_writes_null_organization_id(db_session: AsyncSession):
    org = uuid4()
    service = SearchIndexConfigurationService(VectorIndexRegistryRepository(db_session))
    response = await service.establish(
        org,
        EstablishIndexConfigurationRequest(
            index_name="unit-test-platform-index",
            embedding_model="text-embedding-3-large",
            embedding_dimension=1536,
            platform_wide=True,
        ),
    )
    assert response.organization_id is None


@pytest.mark.asyncio
async def test_get_by_name_for_caller_never_returns_another_tenants_row(db_session: AsyncSession):
    """Direct repository-level tenant-isolation unit test, complementing the API-level checklist tests."""
    org_a, org_b = uuid4(), uuid4()
    repo = VectorIndexRegistryRepository(db_session)
    await repo.create(
        organization_id=org_a,
        index_name="unit-isolation-index",
        embedding_model="m",
        embedding_dimension=8,
        retrieval_mode="HYBRID",
        refresh_cadence=None,
    )

    resolved_for_b = await repo.get_by_name_for_caller(org_b, "unit-isolation-index")
    assert resolved_for_b is None

    resolved_for_a = await repo.get_by_name_for_caller(org_a, "unit-isolation-index")
    assert resolved_for_a is not None
    assert resolved_for_a.organization_id == org_a


@pytest.mark.asyncio
async def test_content_registration_produces_correctly_linked_evidence_and_chunks(db_session: AsyncSession):
    org = uuid4()
    index_repo = VectorIndexRegistryRepository(db_session)
    index = await index_repo.create(
        organization_id=org,
        index_name="unit-content-index",
        embedding_model="text-embedding-3-large",
        embedding_dimension=1536,
        retrieval_mode="HYBRID",
        refresh_cadence=None,
    )

    service = ContentRegistrationService(
        db_session=db_session,
        index_repo=index_repo,
        evidence_repo=EvidenceRegistryRepository(db_session),
        chunk_repo=DocumentChunkRegistryRepository(db_session),
    )

    result = await service.register(
        org,
        RegisterContentRequest(index_name="unit-content-index", text="A short evidence passage.", evidence_source="Unit Test"),
    )
    assert result.vector_index_id == index.vector_index_id
    assert result.chunk_count == 1

    chunk_repo = DocumentChunkRegistryRepository(db_session)
    rows = await chunk_repo.list_for_index(vector_index_id=index.vector_index_id, organization_id=org, top_k=10)
    assert len(rows) == 1
    chunk, evidence = rows[0]
    assert chunk.evidence_id == evidence.evidence_id
    assert chunk.organization_id == org
    assert evidence.organization_id == org
