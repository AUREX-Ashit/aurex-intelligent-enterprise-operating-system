# schemas/search.py
"""WP-11 — Enterprise Search (C-093). Request/response contracts for BA-01/02/03 (`IRA-011 §5`)."""
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# BA-01 — Establish Enterprise Search Index Configuration
# ---------------------------------------------------------------------------

class EstablishIndexConfigurationRequest(BaseModel):
    """Request body for BA-01's own establish path. `platform_wide=True` requires PLATFORM_ADMIN and produces `organization_id IS NULL` (AMD-012)."""
    index_name: str = Field(..., min_length=1, max_length=255)
    embedding_model: str = Field(..., min_length=1, max_length=255)
    embedding_dimension: int = Field(..., gt=0)
    retrieval_mode: str = Field("HYBRID", pattern="^(SEMANTIC|LEXICAL|HYBRID)$")
    refresh_cadence: str | None = Field(None, max_length=255)
    platform_wide: bool = Field(False, description="PLATFORM_ADMIN only — establishes a platform-wide shared index (organization_id NULL) rather than the caller's own tenant-dedicated index.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "index_name": "enterprise-knowledge-v1",
                "embedding_model": "text-embedding-3-large",
                "embedding_dimension": 1536,
                "retrieval_mode": "HYBRID",
                "refresh_cadence": "DAILY",
                "platform_wide": False,
            }
        }
    }


class IndexConfigurationResponse(BaseModel):
    """Result of BA-01's own establish path, and each row in its list path."""
    vector_index_id: UUID
    index_name: str
    embedding_model: str
    embedding_dimension: int
    retrieval_mode: str
    refresh_cadence: str | None
    active_flag: bool
    organization_id: UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}


class IndexConfigurationListResponse(BaseModel):
    """BA-01's own list path — every ACTIVE index configuration visible to the caller (their own tenant-dedicated rows plus platform-wide rows)."""
    index_configurations: list[IndexConfigurationResponse]


# ---------------------------------------------------------------------------
# BA-03 — Register Enterprise Search Content
# ---------------------------------------------------------------------------

class RegisterContentRequest(BaseModel):
    """
    Request body for BA-03. Accepts pre-extracted text only — no file
    upload, no Discovery Provider connection, no configurable chunking
    strategy (`IRA-011 §4.2`/§5, deliberately narrow).
    """
    index_name: str = Field(..., min_length=1, max_length=255, description="The vector_index_registry row (by index_name, resolved within the caller's own tenant/platform-wide scope) this content becomes searchable under.")
    text: str = Field(..., min_length=1, description="Pre-extracted text passage to register as searchable content.")
    evidence_type: str | None = Field(None, max_length=255)
    evidence_source: str | None = Field(None, max_length=255)
    file_reference: str | None = Field(None, max_length=255, description="A locator string for the source this text was extracted from — not a file upload.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "index_name": "enterprise-knowledge-v1",
                "text": "The Board maintains 11 permanent directors with 8 independent seats.",
                "evidence_type": "report",
                "evidence_source": "Annual Governance Report FY25",
                "file_reference": "governance-report-fy25.pdf#p12",
            }
        }
    }


class RegisteredContentResponse(BaseModel):
    """Result of BA-03 — the created Evidence record and the chunk(s) registered against it."""
    evidence_id: UUID
    vector_index_id: UUID
    chunk_count: int
    document_chunk_ids: list[UUID]
    created_at: datetime


# ---------------------------------------------------------------------------
# BA-02 — Execute Enterprise Search
# ---------------------------------------------------------------------------

class ExecuteSearchRequest(BaseModel):
    """Request body for BA-02. `index_name` is resolved within the caller's own tenant/platform-wide scope only — never an arbitrary caller-supplied index identifier (`CLAUDE.md §21.4`)."""
    query: str = Field(..., min_length=1)
    index_name: str | None = Field(None, max_length=255, description="Omit to use the caller's own default tenant-dedicated index, if exactly one exists.")
    top_k: int = Field(3, gt=0, le=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "What is our current board independence ratio?",
                "index_name": "enterprise-knowledge-v1",
                "top_k": 3,
            }
        }
    }


class SearchResultItem(BaseModel):
    """One evidence-cited search result (BA-02). `score` is a disclosed placeholder — no real embedding model is configured (`IRA-011 §4.6`); ranking is by registration recency, not semantic relevance, until a real provider is connected."""
    document_chunk_id: UUID
    evidence_id: UUID
    score: float
    citation: str
    metadata: dict[str, Any]


class SearchResponse(BaseModel):
    """Result of BA-02. `results` is empty, with `message` set, when no content has been registered under the resolved index — an honest empty state (`CLAUDE.md §20.6`), never a fabricated result."""
    vector_index_id: UUID
    results: list[SearchResultItem]
    message: str | None = None
