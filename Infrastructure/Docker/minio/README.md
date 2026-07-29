# MinIO Object Storage Infrastructure

MinIO provides S3-compatible local object storage for Aurex. This is primarily utilized by the IngestionService to store raw multi-tenant data, documents, and ESG evidence uploads.

## Ports and Connections
* **Object Store Endpoint (API):** `http://minio:9000` (Local Host: `http://localhost:9000`)
* **Admin Web UI Console:** `http://localhost:9001`

## Default Development Credentials
* **Access Key:** `aurex_admin`
* **Secret Key:** `AurexAdminPass123!`

## Pre-provisioned Buckets
* `aurex-ingestion-payloads` - Contains ingested source documents.
* `aurex-esg-evidence` - Stores validated audit evidence artifacts.

## CLI Management (mc)
You can download the MinIO Client (`mc`) and configure it locally to manage file transfers:
```bash
# Configure local alias
mc alias set aurex-local http://localhost:9000 aurex_admin AurexAdminPass123!

# List objects inside ingestion bucket
mc ls aurex-local/aurex-ingestion-payloads
```
