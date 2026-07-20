import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class DocumentStatusResponse(BaseModel):
    """
    Response schema representing the ingestion status of a single ESG document.
    """
    id: uuid.UUID
    tenant_id: str
    filename: str
    file_size: int
    content_type: str
    storage_path: str
    document_type: str
    status: str
    ocr_task_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    metadata_json: Optional[Dict[str, Any]] = None
    extracted_data_json: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class DocumentMetadataUpdate(BaseModel):
    """
    Payload for patching custom extracted metadata fields.
    """
    metadata_json: Dict[str, Any] = Field(..., description="Key-value dictionary representing audited ESG metadata updates")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "metadata_json": {
                    "audit_status": "verified",
                    "co2_reduction_metric_tons": 450.5,
                    "target_year": 2030
                }
            }
        }
    )

class StartOCRRequest(BaseModel):
    """
    Payload for triggering async OCR layout processing.
    """
    document_id: uuid.UUID = Field(..., description="Unique track ID of the uploaded document to process")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "document_id": "89b53f66-3d44-4284-8ee1-f9ebdb314db0"
            }
        }
    )

class StartOCRResponse(BaseModel):
    """
    System response indicating OCR dispatch task details.
    """
    task_id: str = Field(..., description="Unique service broker tracker token for checking execution status")
    document_id: uuid.UUID = Field(..., description="Referred document tracking reference")
    status: str = Field(..., description="The state of execution scheduling dispatch (e.g., dispatched)")
    dispatched_at: datetime = Field(default_factory=datetime.utcnow, description="Log timestamp of task release")

    model_config = ConfigDict(from_attributes=True)
