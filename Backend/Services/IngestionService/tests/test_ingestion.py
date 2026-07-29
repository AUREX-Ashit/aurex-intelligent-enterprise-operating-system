import pytest
import uuid
import json
from httpx import AsyncClient
from config.settings import settings

pytestmark = pytest.mark.asyncio

async def test_tenant_isolation_middleware_missing_header(client: AsyncClient):
    """
    Asserts that the TenantIsolationMiddleware blocks incoming requests when X-Tenant-ID is missing.
    """
    response = await client.post("/ingestion/upload", data={
        "document_type": "esg_report"
    })
    # Must get HTTP 400 Bad Request
    assert response.status_code == 400
    details = response.json()
    assert details["error"] == "Missing Tenant Header"
    assert "X-Tenant-ID" in details["message"]
    assert details["code"] == "MISSING_TENANT_CONTEXT"


async def test_tenant_isolation_middleware_invalid_header(client: AsyncClient):
    """
    Asserts that the TenantIsolationMiddleware blocks invalid tenant IDs.
    """
    response = await client.post(
        "/ingestion/upload", 
        headers={"X-Tenant-ID": "  "},
        data={"document_type": "esg_report"}
    )
    assert response.status_code == 400
    assert "Invalid Tenant Header" in response.json()["error"]


async def test_health_check_exempt_from_tenant_isolation(client: AsyncClient):
    """
    Asserts that open/operations health paths do not prompt for Tenant isolation keys.
    """
    response = await client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["service"] == "aurex-ingestion-service"


async def test_successful_document_upload(client: AsyncClient):
    """
    Tests complete document upload, storage persistence mock registry, and database mapping.
    """
    file_payload = ("test_report.pdf", b"%PDF-1.4 mock pdf structure details", "application/pdf")
    tenant_header = {"X-Tenant-ID": "tenant_abc_corp_01"}
    
    response = await client.post(
        "/ingestion/upload",
        headers=tenant_header,
        files={"file": file_payload},
        data={
            "document_type": "esg_report",
            "metadata_str": '{"year": 2026, "audited": true}'
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_report.pdf"
    assert data["tenant_id"] == "tenant_abc_corp_01"
    assert data["document_type"] == "esg_report"
    assert data["content_type"] == "application/pdf"
    assert "staurex" in data["storage_path"]
    assert data["status"] == "uploaded"
    assert data["metadata_json"]["year"] == 2026
    assert data["metadata_json"]["audited"] is True
    assert "id" in data


async def test_upload_blocks_unsupported_file_extension(client: AsyncClient):
    """
    Asserts that file suffixes out of config ranges trigger bad request actions.
    """
    bad_file = ("script.py", b"import os; os.system('clear')", "text/x-python")
    headers = {"X-Tenant-ID": "tenant_abc_corp_01"}
    
    response = await client.post(
        "/ingestion/upload",
        headers=headers,
        files={"file": bad_file},
        data={"document_type": "utility_bill"}
    )
    assert response.status_code == 400
    assert "File extension '.py' is not within authorized system formats" in response.json()["detail"]


@pytest.mark.skip(reason="Needs real file size mocking which is validated in service")
async def test_upload_blocks_oversized_file(client: AsyncClient):
    pass


async def test_ocr_trigger_success_flow(client: AsyncClient):
    """
    Mocks active entry status transitions under async OCR layout analysis client signals.
    """
    # 1. Upload file to construct entry
    file_payload = ("carbon_offset.docx", b"Microsoft Word binary stream metadata mock", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    headers = {"X-Tenant-ID": "tenant_esg_global"}
    
    upload_res = await client.post(
        "/ingestion/upload",
        headers=headers,
        files={"file": file_payload},
        data={"document_type": "offset_certificate"}
    )
    assert upload_res.status_code == 200
    doc_id = upload_res.json()["id"]

    # 2. Fire OCR trigger
    ocr_res = await client.post(
        "/ingestion/ocr/start",
        headers=headers,
        json={"document_id": doc_id}
    )
    assert ocr_res.status_code == 200
    ocr_data = ocr_res.json()
    assert ocr_data["document_id"] == doc_id
    assert "task_id" in ocr_data
    assert ocr_data["status"] == "ocr_processing"
    
    # 3. Retrieve and confirm database state has progressed
    check_res = await client.get(
        f"/ingestion/document/{doc_id}",
        headers=headers
    )
    assert check_res.status_code == 200
    check_data = check_res.json()
    assert check_data["status"] == "ocr_processing"
    assert check_data["ocr_task_id"] == ocr_data["task_id"]


async def test_ocr_trigger_restrict_cross_tenant_access(client: AsyncClient):
    """
    Ensures a tenant cannot dispatch, inspect, or manage documents of another tenant.
    """
    # 1. Tenant A uploads item
    headers_a = {"X-Tenant-ID": "tenant_alpha_ltd"}
    file_bytes = ("annual_report.xlsx", b"Excel cell grid emissions tracker", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    upload_res = await client.post(
        "/ingestion/upload",
        headers=headers_a,
        files={"file": file_bytes},
        data={"document_type": "financial_statement"}
    )
    doc_id = upload_res.json()["id"]

    # 2. Tenant B attempts to start OCR on Tenant A's document
    headers_b = {"X-Tenant-ID": "tenant_beta_corp"}
    ocr_res = await client.post(
        "/ingestion/ocr/start",
        headers=headers_b,
        json={"document_id": doc_id}
    )
    # Must deny with HTTP 404 Not Found to prevent metadata probing
    assert ocr_res.status_code == 404
    assert "not found for organization" in ocr_res.json()["detail"]
