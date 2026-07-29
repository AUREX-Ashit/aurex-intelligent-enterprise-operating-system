import io
import uuid
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.document_repository import DocumentRepository
from services.storage_provider import StorageProvider
from services.ocr_provider import OCRProvider
from services.event_publisher import EventPublisher
from models.document import Document
from config.settings import settings

class IngestionService:
    """
    Central Coordinator service encapsulating business rules, binding persistence,
    storage routing, and asynchronous ocr scheduling pipelines under tenant security gates.
    """
    def __init__(
        self, 
        db_session: AsyncSession,
        storage_provider: StorageProvider,
        ocr_provider: OCRProvider,
        event_publisher: EventPublisher
    ):
        self.db = db_session
        self.doc_repo = DocumentRepository(db_session)
        self.storage = storage_provider
        self.ocr = ocr_provider
        self.publisher = event_publisher

    async def handle_document_upload(
        self, 
        file_bytes: bytes, 
        filename: str, 
        tenant_id: str, 
        document_type: str, 
        content_type: str,
        custom_metadata: Optional[Dict[str, Any]] = None
    ) -> Document:
        """
        Ingests document:
        1. Employs StorageProvider to persist the raw binary file in the cloud.
        2. Allocates tracking database entries via repositories under explicit Tenant confinement.
        3. Fires external Event Bus signaling file completion ready for indexing systems.
        """
        # Validate file size limitations configured in platform rules
        size_limit_bytes = settings.ingestion.max_file_size_mb * 1024 * 1024
        file_size = len(file_bytes)
        if file_size > size_limit_bytes:
            raise ValueError(f"File size {file_size / (1024*1024):.2f}MB exceeds allowed threshold of {settings.ingestion.max_file_size_mb}MB.")
            
        # Validate extensions allowed
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        if ext not in settings.ingestion.allowed_extensions:
            raise ValueError(f"File extension '.{ext}' is not within authorized system formats: {settings.ingestion.allowed_extensions}.")

        # Step 1: Upload raw file stream to storage
        file_stream = io.BytesIO(file_bytes)
        storage_uri = await self.storage.upload_file(
            file_object=file_stream,
            filename=filename,
            tenant_id=tenant_id,
            content_type=content_type
        )
        
        # Step 2: Establish SQLAlchemy tracking model payload
        doc_fields = {
            "id": uuid.uuid4(),
            "filename": filename,
            "file_size": file_size,
            "content_type": content_type,
            "storage_path": storage_uri,
            "document_type": document_type,
            "status": "uploaded",
            "metadata_json": custom_metadata or {}
        }
        
        # Insert inside transactions
        document_orm = await self.doc_repo.create(doc_fields, tenant_id)
        
        # Step 3: Broadcast file ingress transaction event to Service Bus
        await self.publisher.publish_event(
            topic_or_queue="aurex-document-ingress",
            event_type="document.uploaded",
            payload={
                "document_id": str(document_orm.id),
                "filename": document_orm.filename,
                "storage_path": document_orm.storage_path,
                "tenant_id": document_orm.tenant_id,
                "file_size": document_orm.file_size
            },
            tenant_id=tenant_id
        )
        
        return document_orm

    async def initiate_ocr_processing(self, document_id: uuid.UUID, tenant_id: str) -> Dict[str, Any]:
        """
        Unfolds layout analysis pipeline:
        1. Ensures document belongs securely to tenant.
        2. Obtains temporary pre-signed direct access storage path.
        3. Schedules background transaction task inside target OCRProvider.
        4. Transistions database metadata.
        5. Emits scheduling event.
        """
        # Step 1: Verify Ownership
        doc = await self.doc_repo.get_by_id(document_id, tenant_id)
        if not doc:
            raise LookupError(f"Document with reference '{document_id}' not found for organization '{tenant_id}'.")
            
        if doc.status == "ocr_processing":
            return {
                "task_id": doc.ocr_task_id or "local_task_active",
                "document_id": doc.id,
                "status": doc.status,
                "message": "OCR process is already active for this document."
            }

        # Step 2: Generate SAS locator token URI
        secure_uri = await self.storage.get_download_url(doc.storage_path, tenant_id)
        
        # Step 3 & 4: Dispatch processing requests & write tracking tags
        ocr_task_id = await self.ocr.submittal_ocr_analysis(secure_uri, tenant_id)
        
        # Move document state to active
        updated_doc = await self.doc_repo.update_ocr_status(
            doc_id=doc.id,
            tenant_id=tenant_id,
            status="ocr_processing",
            ocr_task_id=ocr_task_id
        )
        
        # Step 5: Post Event Outflow
        await self.publisher.publish_event(
            topic_or_queue="aurex-ocr-pipelines",
            event_type="ocr.started",
            payload={
                "document_id": str(doc.id),
                "ocr_task_id": ocr_task_id,
                "tenant_id": tenant_id,
                "model": settings.ocr.azure_model
            },
            tenant_id=tenant_id
        )
        
        return {
            "task_id": ocr_task_id,
            "document_id": str(updated_doc.id),
            "status": updated_doc.status,
            "dispatched_at": updated_doc.updated_at
        }

    async def fetch_document_state(self, document_id: uuid.UUID, tenant_id: str) -> Document:
        """
        Secured fetch returning active states.
        """
        doc = await self.doc_repo.get_by_id(document_id, tenant_id)
        if not doc:
            raise LookupError(f"Document with ID '{document_id}' is not registerd.")
        return doc

    async def update_custom_metadata(self, document_id: uuid.UUID, tenant_id: str, new_meta: Dict[str, Any]) -> Document:
        """
        Allows auditing metadata patching.
        """
        doc = await self.doc_repo.get_by_id(document_id, tenant_id)
        if not doc:
            raise LookupError(f"Document and scope mismatch.")
            
        merged_metadata = {**(doc.metadata_json or {}), **new_meta}
        updated_doc = await self.doc_repo.update(
            item_id=document_id,
            update_data={"metadata_json": merged_metadata},
            tenant_id=tenant_id
        )
        return updated_doc
