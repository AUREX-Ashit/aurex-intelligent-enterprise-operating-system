# CorpStage Authentication Service (`AuthService`)

A production-grade, multi-tenant authentication microservice scaffold based on FastAPI, Python 3.14, and Pydantic v2. Designed with high-performance async pools using SQLAlchemy 2.0 and structural security configurations ready to be deployed on container architectures.

---

## 🛠 Features Included

- **Python 3.14 + FastAPI**: Fully asynchronous, type-annotated, and fast framework integration.
- **Pydantic v2 Schemas**: Request validation and response-serialization enforcement with highly optimized JSON compiling.
- **SQLAlchemy 2.0 async engine**: Modern mapping support (`Mapped` types) and connection pool sizing configured.
- **Strict Multi-Tenancy**: Tenant context automatic isolation middleware extracting compliant header parameters (`X-Tenant-ID` is required as a valid UUID).
- **Asynchronous Unit Testing**: Comprehensive test mocks using Pytest with SQLite in-memory overrides logic.
- **Enterprise Docker Blueprint**: Best-practice multi-stage compiler builds and non-root execution profiles.

---

## 📂 Project Structure

```text
AuthService/
├── middleware/          # Interceptor layers (Multi-tenant extraction, Trace logs)
│   ├── __init__.py
│   ├── logging.py
│   └── tenant.py        # ContextVar storage and headers sanitization
├── models/              # SQLAlchemy 2.x Declarative Models
│   ├── __init__.py
│   ├── database.py      # Async Engine manager and Async Session dependency
│   └── user.py          # TentantModel & UserModel schemas
├── repositories/        # Decoupled database data-access-object layers
│   ├── __init__.py
│   ├── base_repository.py  # Generic async CRUD scaffold
│   └── user_repository.py  # Specialized queries
├── routers/             # FastAPI Endpoint Controller stubs
│   ├── __init__.py
│   ├── auth.py          # /auth/login and /auth/refresh
│   └── health.py        # Microservice health probe
├── schemas/             # Pydantic v2 validation DTOs
│   ├── __init__.py
│   └── auth.py          # LoginRequest and TokenResponse schemas
├── services/            # Custom enterprise business logic orchestrators
│   ├── __init__.py
│   └── auth_service.py  # Password hashing, JWT credentials creation
├── tests/               # Pytest testing suite
│   ├── __init__.py
│   ├── conftest.py      # SQLAlchemy DB overrides and TestClient fixture state
│   └── test_auth.py     # Endpoint integration and validations checks
├── Dockerfile           # Optimized multi-stage Docker environment build
├── README.md            # Service documentation
├── main.py              # Application entrypoint
└── requirements.txt     # Python production-grade packages catalog
```

---

## 🚀 Running the Microservice

### 1. Requirements

Before building, ensure you have Python 3.12+ (Python 3.14 recommended) or Docker environment installed.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Standard Up Execution

Start the Uvicorn development server with files auto-reloader enabled:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive OpenAPI Swagger documentations will be available immediately at:
- **Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDocs**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🐳 Running with Docker

Build and run the release package safely inside modern sandboxed containers:

```bash
# Build the Docker image
docker build -t corpstage-auth-service:latest .

# Run the container specifying port mappings
docker run -p 8000:8000 --env DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/corpstage corpstage-auth-service:latest
```

---

## 🧪 Running Tests

Execute analytical test suites asserting compliance across routers and middlewares utilizing standard unit tests:

```bash
pytest -v
```

---

## 🔒 Security Design: Multi-Tenancy

Each incoming HTTP request (excluding `health` and `docs`) is intercept-checked via `TenantMiddleware`. 

If the user does not provide `X-Tenant-ID` in the request headers, or provides an invalid representation, the application declines routing with an `HTTP 400 Bad Request` payload. On valid requests, it sets a localized, async-safe `ContextVar` that is referenced globally across service layers to protect cross-tenant boundary queries automatically.
