from abc import ABC, abstractmethod
import os
from typing import BinaryIO, Dict, Any, Tuple
from config.settings import settings

class StorageProvider(ABC):
    """
    Abstract Base Class contract guiding asset uploads to object storage.
    Enforces clean dependency injection across environments.
    """
    
    @abstractmethod
    async def upload_file(self, file_object: BinaryIO, filename: str, tenant_id: str, content_type: str) -> str:
        """
        Uploads and saves a stream, returning the complete, addressable URI/filepath.
        """
        pass

    @abstractmethod
    async def get_download_url(self, storage_path: str, tenant_id: str, expiry_seconds: int = 3600) -> str:
        """
        Generates a secure, temporary pre-signed URL for dowloading and ingestion by extraction models.
        """
        pass

    @abstractmethod
    async def delete_file(self, storage_path: str, tenant_id: str) -> bool:
        """
        Deletes stored resource if exists, returning boolean confirmation.
        """
        pass


class AzureBlobStorageStub(StorageProvider):
    """
    Mock/Stub production compliant implementation mapping to Azure Blob Storage configurations.
    Avoids SDK bloat during bootstrapping, allowing seamless local development, testing, and CI.
    """
    def __init__(self, container_name: str = "aurex-evidence"):
        self.container_name = container_name
        self.mock_db: Dict[str, Dict[str, Any]] = {}

    async def upload_file(self, file_object: BinaryIO, filename: str, tenant_id: str, content_type: str) -> str:
        # Create a unique virtual location mirroring tenant-isolated Azure containers
        virtual_path = f"https://staurex{settings.region}.blob.core.windows.net/{self.container_name}/{tenant_id}/{filename}"
        
        # Read the file to register metadata size in stub database
        content = file_object.read()
        file_size = len(content)
        
        self.mock_db[virtual_path] = {
            "size": file_size,
            "tenant_id": tenant_id,
            "content_type": content_type
        }
        
        # In a real environment, you would use:
        # from azure.storage.blob.aio import BlobServiceClient
        # blob_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
        # ...
        
        return virtual_path

    async def get_download_url(self, storage_path: str, tenant_id: str, expiry_seconds: int = 3600) -> str:
        # Appends a secure, mock SAS (Shared Access Signature) token ensuring tenant scope validation
        if "staurex" in storage_path and f"/{tenant_id}/" not in storage_path:
            raise PermissionError(f"Cross-tenant storage access denied. Tenant {tenant_id} is forbidden from accessing {storage_path}.")
            
        return f"{storage_path}?sv=2023-11-03&sr=b&sig=MOCK_SAS_SIG_EXPIRING_IN_{expiry_seconds}_SECONDS_TENANT_{tenant_id}"

    async def delete_file(self, storage_path: str, tenant_id: str) -> bool:
        if storage_path in self.mock_db:
            if self.mock_db[storage_path]["tenant_id"] != tenant_id:
                raise PermissionError("Access restricted. Cannot delete cross-tenant resources.")
            del self.mock_db[storage_path]
            return True
        return False
