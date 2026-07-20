import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class UploadInitiateRequest(BaseModel):
    """
    Validation schema to pre-allocate an upload tracking volume session.
    """
    total_files: int = Field(gt=0, description="Number of documents to be uploaded in this tracking stream session (MUST be > 0)")
    overall_size_bytes: int = Field(gt=0, description="Cumulative size of all documents combined")
    initiator_user_id: Optional[str] = Field(None, max_length=100, description="ID of the user who initiated this session")
    client_metadata: Optional[Dict[str, Any]] = Field(None, description="Custom dictionary elements capturing system variables")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "total_files": 2,
                "overall_size_bytes": 10485760,
                "initiator_user_id": "usr_9921_esg_analyst",
                "client_metadata": {"department": "Sustainability Reporting", "quarter": "Q2-2026"}
            }
        }
    )

class UploadTrackerSummary(BaseModel):
    """
    Direct model mapping representation.
    """
    id: uuid.UUID
    tenant_id: str
    initiator_user_id: Optional[str] = None
    session_status: str
    total_files: int
    overall_size_bytes: int
    client_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UploadInitiateResponse(BaseModel):
    """
    Structure returned to client upon session confirmation.
    """
    session_id: uuid.UUID = Field(..., description="UUID token to supply during individual file uploads")
    tenant_id: str
    status: str
    total_files_allowed: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
