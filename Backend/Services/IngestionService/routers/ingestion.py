import json
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_db_session
from schemas.document import DocumentStatusResponse, StartOCRRequest, StartOCRResponse, DocumentMetadataUpdate
from services.ingestion_service import IngestionService
from services.storage_provider import AzureBlobStorageStub
from services.ocr_provider import AzureDocumentIntelligenceStub
from services.event_publisher import AzureServiceBusStub
from config.settings import settings

ingestion_router = APIRouter(prefix="/ingestion", tags=["Ingestion Orchestrator"])

# Shared Dependency Provider mapping stubs
def get_ingestion_service(db: AsyncSession = Depends(get_db_session)) -> IngestionService:
    """
    Dependency injector assembling storage, OCR, and ServiceBus stubs with db session.
    """
    storage = AzureBlobStorageStub(container_name=settings.storage.azure_container)
    ocr = AzureDocumentIntelligenceStub(model_name=settings.ocr.azure_model)
    bus = AzureServiceBusStub()
    return IngestionService(
        db_session=db,
        storage_provider=storage,
        ocr_provider=ocr,
        event_publisher=bus
    )


@ingestion_router.post(
    "/upload",
    response_model=DocumentStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload and track ESG document",
    description="Accepts multipart upload, pushes to cloud containers, and initializes row tracking."
)
async def upload_esg_document(
    file: UploadFile = File(..., description="Document asset (PDF, XLSX, CSV, DOCX) under 200MB"),
    document_type: str = Form(..., description="E.g., 'esg_report', 'annual_report'"),
    metadata_str: Optional[str] = Form(None, description="Valid JSON string representing parsed metadata properties"),
    x_tenant_id: str = Header(..., alias=settings.auth.header_name, description="Organization isolation UUID context"),
    service: IngestionService = Depends(get_ingestion_service)
):
    # Parse metadata string if supplied
    custom_metadata = {}
    if metadata_str:
        try:
            custom_metadata = json.loads(metadata_str)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Form parameter 'metadata_str' must be a valid JSON representation."
            )

    try:
        # Read file contents
        content_bytes = await file.read()
        
        # Invoke orchestrator
        document_orm = await service.handle_document_upload(
            file_bytes=content_bytes,
            filename=file.filename or "unnamed_document",
            tenant_id=x_tenant_id,
            document_type=document_type,
            content_type=file.content_type or "application/octet-stream",
            custom_metadata=custom_metadata
        )
        return document_orm
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion transaction aborted: {str(exc)}"
        )


@ingestion_router.post(
    "/ocr/start",
    response_model=StartOCRResponse,
    status_code=status.HTTP_200_OK,
    summary="Initiate asynchronous OCR Layout execution",
    description="Pre-signs a SAS token, passes URL to Form Recognizer backend, and registers task tracking."
)
async def initiate_ocr_processing(
    payload: StartOCRRequest,
    x_tenant_id: str = Header(..., alias=settings.auth.header_name),
    service: IngestionService = Depends(get_ingestion_service)
):
    try:
        result = await service.initiate_ocr_processing(
            document_id=payload.document_id,
            tenant_id=x_tenant_id
        )
        return result
    except LookupError as lookup_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(lookup_err)
        )
    except PermissionError as perm_err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(perm_err)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OCR Dispatch system pipeline failure: {str(exc)}"
        )


@ingestion_router.get(
    "/document/{document_id}",
    response_model=DocumentStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch tenant document status"
)
async def get_document_by_id(
    document_id: uuid.UUID,
    x_tenant_id: str = Header(..., alias=settings.auth.header_name),
    service: IngestionService = Depends(get_ingestion_service)
):
    try:
        doc = await service.fetch_document_state(document_id, x_tenant_id)
        return doc
    except LookupError as lookup_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(lookup_err)
        )


@ingestion_router.patch(
    "/document/{document_id}/metadata",
    response_model=DocumentStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Update document verification tags"
)
async def update_document_metadata_fields(
    document_id: uuid.UUID,
    payload: DocumentMetadataUpdate,
    x_tenant_id: str = Header(..., alias=settings.auth.header_name),
    service: IngestionService = Depends(get_ingestion_service)
):
    try:
        doc = await service.update_custom_metadata(
            document_id=document_id,
            tenant_id=x_tenant_id,
            new_meta=payload.metadata_json
        )
        return doc
    except LookupError as lookup_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(lookup_err)
        )
