# CorpStage AIService Scaffolding

An enterprise-grade, multi-tenant AI Orchestration and ESG compliance validation microservice engineered in FastAPI and Python 3.14.

## Key Features

- **Multi-Tenant Architecture**: Complete tenant isolation from requests down to the database connection levels, controlled by custom tracking headers (`X-Tenant-ID`).
- **Clean Architecture Principles**: Layered decoupling using the Repository pattern and Service Contract models.
- **Provider Abstractions**: Decoupled third-party interfaces for LLM execution (`LLMProvider`), embedders (`EmbeddingProvider`), and semantic indices (`VectorProvider`).
- **Pydantic v2 & SQLAlchemy 2.x Async**: Leverages asynchronous SQLite/Postgres connectivities and ultra-safe type schemas.
- **Testing suite**: Embedded pytest structures including async fixtures and endpoint validations.

## Service Registry Overview

```
AIService/
├── main.py                     # Entry point, lifespan managers, and router bindings
├── requirements.txt            # Package lock-file
├── Dockerfile                  # Container configurations
├── README.md                   # System documentation
├── config/                     # Platform and YAML parser utilities
├── middleware/                 # Tenancy checks and structured JSON log managers
├── models/                     # SQLAlchemy declaration base and multi-entity models
├── repositories/               # Decoupled DB queries with transactional context
├── routers/                    # Clean endpoints exposing api-contract schemas
├── schemas/                    # Pydantic-validations for IO payloads
├── services/                   # Intelligent engines (Orchestrator, RAG, Extraction)
└── tests/                      # Conftest files and simulation suites
```

## Setup & Running Locally

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Service**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 3000 --reload
   ```

3. **Verify API Documentation**:
   - Swagger endpoints: `http://localhost:3000/docs`
   - Redoc documentation: `http://localhost:3000/redoc`
