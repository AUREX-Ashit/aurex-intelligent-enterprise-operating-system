# CorpStage ReportingService

Enterprise ESG (Environmental, Social, Governance), BRSR (India SEBI), GRI, and CSRD (European Union) disclosure reporting microservice built with **Python 3.14**, **FastAPI**, **Pydantic v2**, and **SQLAlchemy 2.0 Async** engines.

## 🏗️ Architecture Overview

The system utilizes the classic **Repository Pattern** paired with **Abstract Provider Contexts** to guarantee modularity and compliance validation.

```
CorpStage ReportingService/
├── main.py                     # Microservice entrypoint & lifespans
├── requirements.txt            # Dependency listings (SQLAlchemy 2.0, FastAPI, jose, structlog)
├── Dockerfile                  # Secure, multi-stage non-root container builder
├── README.md                   # System documentation
├── config/
│   ├── platform-config.yaml    # Raw declarative Azure/DB/Auth setup values
│   └── settings.py             # Config parser with automatic environment overloads
├── middleware/
│   └── tenant.py               # ContextVar isolators enforcing multi-tenant headers
├── models/
│   ├── database.py             # SQLAlchemy Async Engine, async sessions & audit mixins
│   └── report.py               # SQLAlchemy 2.0 models for reports, exports, and scorecards
├── repositories/
│   ├── base.py                 # Abstract Generic Repository scoping queries to Tenant ID
│   └── report_repository.py    # Specific repositories for Reports, Scorecards, & AuditLogs
├── routers/
│   └── reporting.py            # API routing with operational validators
├── schemas/
│   └── report.py               # Pydantic v2 schemas validating in/out schemas
├── services/
│   └── providers.py            # Implementations of ReportProvider, ExportProvider & DashboardProvider
└── tests/
    ├── __init__.py
    └── test_endpoints.py       # Integration & API endpoint test assertions
```

### 🔒 Core Design Principles

1. **Strict Multi-Tenancy**: The `TenantMiddleware` extracts the tenant context from the header defined in `platform-config.yaml` (`X-Tenant-ID`). This identity is preserved in an async-safe `contextvars.ContextVar` across the execution lifecycle. Every database select, insert, or delete query performed by the `BaseRepository` automatically appends filters on `tenant_id` to guarantee tenant isolation.
2. **Abstract Providers**: Abstractions like `ReportProvider`, `ExportProvider`, and `DashboardProvider` enforce decoupled design. For example:
   * `ReportProvider`: generates and scores standard reports (ESG, BRSR, GRI, CSRD).
   * `ExportProvider`: triggers cloud-backed exports (PDF, XLSX, PPTX, JSON) linked to Azure Blob.
   * `DashboardProvider`: gathers complex scorecard progress tracking.
3. **Pydantic v2 & SQLAlchemy 2.0 Async**: Employs async generators for database sessions (`get_db`) to utilize connection pools safely without clogging threads.
4. **Environment Variables Over YAML**: Sourced using `pydantic-settings`. High-security tokens such as `JWT_SECRET_KEY` are parsed **strictly** from the runtime environment and blocked from being loaded from YAML configuration files.

## 🚀 Running Locally

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Provide connection parameters overriding `platform-config.yaml`:
   ```bash
   export JWT_SECRET_KEY="YOUR_ENTERPRISE_SIGNING_KEY"
   export DATABASE_URL="postgresql+asyncpg://user:password@host:port/dbname"
   ```

3. **Launch the Service**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🐋 Docker Build & Deploy

This repository includes a multi-stage Dockerfile that builds a secure, non-root runner:

```bash
docker build -t corpstage-reporting-service .
docker run -p 8000:8000 -e JWT_SECRET_KEY="supersecret" corpstage-reporting-service
```
