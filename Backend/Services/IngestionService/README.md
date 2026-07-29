# Aurex Ingestion Service

An enterprise-grade, high-performance, multi-tenant document ingestion and OCR scheduling service built with Python 3.14 and FastAPI.

## Architectural Design Highlights

This microservice is structured for strict enterprise environments utilizing multi-tenancy, clean abstraction boundaries, and async-first database/event execution:

1. **Multi-Tenant Isolation**: Imbedded tenant middleware enforces isolation, validating incoming headers/credentials, setting contextual boundaries, and preparing database schemas or Azure search filters.
2. **Abstract Service Providers**: Implements independent abstract base interfaces (ABIs) for Storage Providers, OCR Analyzers, and Event Publishers under standard python dependency injection protocols. Zero tight coupling to Azure or AWS at the base core level.
3. **Async-First Execution**: Leveraging SQL Alchemy 2.0 Async engine coupled with explicit repositories and unit of works for high-density performance without connection holding.
4. **Structured JSON Logging**: Implements standard structured JSON logging via customized middleware and Python standard handlers.

---

## Technical Stack & Dependencies

- **Runtime**: Python 3.14-slim (optimized build runner)
- **API Engine**: FastAPI / Pydantic V2
- **Persistent Storage Model**: SQLAlchemy 2.x ORM Core / PostgreSQL (Schema Isolated or Row-Level Isolation ready)
- **Testing Engine**: PyTest with Async API fixtures

---

## Directory Structure

```text
IngestionService/
├── main.py                             # Microservice entrypoint & app bootstrapping
├── requirements.txt                    # Project libraries & dependencies
├── Dockerfile                          # Optimized multi-stage runner docker image
├── README.md                           # Documentation & execution instructions
├── auth-api.yaml                       # JWT Validation & Security boundaries
├── config/
│   ├── __init__.py
│   └── settings.py                     # Config parser reading platform-config.yaml & Environment variables
├── middleware/
│   ├── __init__.py
│   ├── logging.py                      # Request tracking and structured JSON Logger
│   └── tenant.py                       # Tenant context verification and extraction
├── models/
│   ├── __init__.py
│   ├── database.py                     # Async Database sessions and lifecycle engine
│   ├── document.py                     # SQLAlchemy Database model representing ingested items
│   └── upload.py                       # SQLAlchemy Database model representing upload sessions
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py              # Base Async repository logic
│   └── document_repository.py          # Domain-specific Async operations for Documents
├── routers/
│   ├── __init__.py
│   ├── ingestion.py                    # Multi-tenant ingestion routing protocols
│   └── health.py                       # High-reliability kubernetes/ingress health probes
├── schemas/
│   ├── __init__.py
│   ├── upload.py                       # Pydantic v2 schemas for document uploads
│   └── document.py                     # Pydantic v2 schemas for document statuses
├── services/
│   ├── __init__.py
│   ├── ingestion_service.py            # Orchestrator combining Storage, Database, OCR and dispatch
│   ├── storage_provider.py             # Storage Interface contract & dry-run stub
│   ├── ocr_provider.py                 # OCR Interface contract & dry-run stub
│   └── event_publisher.py              # Messages & Events Publisher contract & dry-run stub
└── tests/
    ├── __init__.py
    ├── conftest.py                     # PyTest database dynamic mock state engine
    └── test_ingestion.py               # Functional validation suites
```

---

## Setup & Running Locally

### 1. Prerequisites
- Python 3.14
- Docker & Docker Compose (optional)

### 2. Configure Environment Variables
Create a local `.env` overriding platform-config.yaml:
```bash
ENVIRONMENT=development
DATABASE_URL=postgresql+asyncpg://aurex:localpassword@localhost:5432/aurex
JWT_SECRET_KEY=super-secured-64-bit-production-secret-key-do-not-reveal
PORT=3000
```

### 3. Run with Uvicorn
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

### 4. Direct Docker Execution
```bash
docker build -t aurex-ingestion-service .
docker run -p 3000:3000 --env-file=.env aurex-ingestion-service
```
