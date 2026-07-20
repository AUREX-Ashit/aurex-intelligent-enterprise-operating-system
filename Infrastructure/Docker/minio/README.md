# MinIO Object Storage Infrastructure

MinIO provides S3-compatible local object storage for CorpStage. This is primarily utilized by the IngestionService to store raw multi-tenant data, documents, and ESG evidence uploads.

## Ports and Connections
* **Object Store Endpoint (API):** `http://minio:9000` (Local Host: `http://localhost:9000`)
* **Admin Web UI Console:** `http://localhost:9001`

## Default Development Credentials
* **Access Key:** `corpstage_admin`
* **Secret Key:** `CorpStageAdminPass123!`

## Pre-provisioned Buckets
* `corpstage-ingestion-payloads` - Contains ingested source documents.
* `corpstage-esg-evidence` - Stores validated audit evidence artifacts.

## CLI Management (mc)
You can download the MinIO Client (`mc`) and configure it locally to manage file transfers:
```bash
# Configure local alias
mc alias set corpstage-local http://localhost:9000 corpstage_admin CorpStageAdminPass123!

# List objects inside ingestion bucket
mc ls corpstage-local/corpstage-ingestion-payloads
```
