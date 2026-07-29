# tests/test_ai.py
import pytest
from httpx import AsyncClient

# Test headers
MOCK_TENANT_HEADERS = {
    "X-Tenant-ID": "test-corporate-tenant-42"
}

@pytest.mark.asyncio
async def test_health_check_endpoint(client: AsyncClient):
    """Verifies service health check operates perfectly in isolation."""
    response = await client.get("/ai/health")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Aurex"
    assert "database" in data["components"]

@pytest.mark.asyncio
async def test_tenancy_requirement_checking(client: AsyncClient):
    """Confirms request rejections when header tracking parameters are empty."""
    # Posting without Tenant-ID header
    response = await client.post(
        "/ai/extract",
        json={"document_name": "Annual_Report_2025.pdf"}
    )
    assert response.status_code == 400
    assert "Tenancy isolation error" in response.json()["error"]

@pytest.mark.asyncio
async def test_extract_and_comply_workflow(client: AsyncClient):
    """Simulates multi-stage processing covering Extraction, Validation and Scoring."""
    # 1. Trigger extraction with verified header
    extract_resp = await client.post(
        "/ai/extract",
        json={
            "document_name": "ESG_Target_Report.pdf",
            "file_uri": "https://storage.corpstage.internal/evidence/report.pdf"
        },
        headers=MOCK_TENANT_HEADERS
    )
    assert extract_resp.status_code == 200
    extract_data = extract_resp.json()
    assert extract_data["document_name"] == "ESG_Target_Report.pdf"
    assert extract_data["status"] == "completed"
    
    extraction_id = extract_data["id"]

    # 2. Trigger rule validations over previous entry
    valid_resp = await client.post(
        "/ai/validate",
        json={
            "extraction_id": extraction_id
        },
        headers=MOCK_TENANT_HEADERS
    )
    assert valid_resp.status_code == 200
    valid_data = valid_resp.json()
    assert valid_data["extraction_id"] == extraction_id
    assert valid_data["governance_verified"] is True  # Based on stub values
    assert len(valid_data["rules_run"]) > 0

    validation_id = valid_data["id"]

    # 3. Simulate human audit action marking record as reviewed
    review_resp = await client.post(
        "/ai/review",
        json={
            "validation_id": validation_id,
            "reviewer_email": "auditor@corpstage.com",
            "is_approved": True,
            "comments": "Auditing results match declared carbon assets perfectly."
        },
        headers=MOCK_TENANT_HEADERS
    )
    assert review_resp.status_code == 200
    review_data = review_resp.json()
    assert review_data["is_reviewed"] is True
    assert review_data["reviewed_by"] == "auditor@corpstage.com"

    # 4. Trigger ESG criteria rating algorithm calculation
    score_resp = await client.post(
        "/ai/scoring",
        json={
            "extraction_id": extraction_id
        },
        headers=MOCK_TENANT_HEADERS
    )
    assert score_resp.status_code == 200
    score_data = score_resp.json()
    assert score_data["composite_esg_score"] > 0
    assert len(score_data["sdg_mapping"]) > 0
    # Map to SDG climate Action indicator
    assert any(mapping["sdg_id"] == 13 for mapping in score_data["sdg_mapping"])
