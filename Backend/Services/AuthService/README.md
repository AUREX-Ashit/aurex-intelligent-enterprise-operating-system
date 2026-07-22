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
- **Idempotent Platform Bootstrap (WP-00)**: automated, re-runnable seeding of canonical Roles, Permissions, the demonstration Organization, and the Platform Administrator identity — see [Platform Bootstrap](#-platform-bootstrap-wp-00) below.
- **Feature Flags (WP-00)**: config-driven (YAML + environment override) rollout control, with fail-closed defaults for undeclared flags.
- **Liveness/Readiness Split (WP-00)**: `/health` reports process/database liveness; `/ready` additionally reports whether bootstrap has completed.
- **Correlation IDs (WP-00)**: every request is assigned or propagates an `X-Correlation-ID`, bound to audit/event/metric emissions for end-to-end tracing.
- **Organization Management (WP-01)**: Establish Organization Business Activity — see [Organization Management](#-organization-management-wp-01) below.

---

## 📂 Project Structure

```text
AuthService/
├── Config/               # platform-config.yaml (database, CORS, feature flags, bootstrap)
├── docs/                 # Operational documentation (WP-00)
│   ├── RUNBOOK_BOOTSTRAP.md
│   └── OPERATIONAL_OWNERSHIP.md
├── middleware/           # Interceptor layers (Multi-tenant extraction, Trace logs)
│   ├── __init__.py
│   ├── logging.py        # Request logging + correlation ID + duration metric (WP-00)
│   └── tenant.py         # ContextVar storage and headers sanitization
├── models/                # SQLAlchemy 2.x Declarative Models
│   ├── __init__.py
│   ├── database.py        # Async Engine manager and Async Session dependency
│   └── ...                # Organization, Person, Identity, Membership, Role, Permission
├── repositories/           # Decoupled database data-access-object layers
│   ├── __init__.py
│   ├── base_repository.py  # Generic async CRUD scaffold
│   └── organization_repository.py  # WP-01
├── routers/               # FastAPI Endpoint Controllers
│   ├── __init__.py
│   ├── auth.py             # /auth/login and /auth/refresh
│   ├── person.py           # /person/recognize and /person/establish
│   ├── organization.py     # POST /organizations (WP-01)
│   └── health.py           # /health (liveness) and /ready (readiness, WP-00)
├── schemas/                # Pydantic v2 validation DTOs
│   └── organization.py     # WP-01
├── scripts/                 # Seed data + bootstrap CLI entrypoint (WP-00)
│   ├── __init__.py
│   ├── bootstrap_data.py    # Canonical Role/Permission/Organization/Identity seed constants
│   └── run_bootstrap.py     # `python -m scripts.run_bootstrap` pipeline entrypoint
├── services/                 # Custom enterprise business logic orchestrators
│   ├── __init__.py
│   ├── auth_service.py       # Password hashing, JWT credentials creation, JWT decode (WP-01)
│   ├── bootstrap_service.py  # Idempotent platform bootstrap orchestration (WP-00)
│   ├── feature_flag_service.py  # Config-driven feature flag evaluation (WP-00)
│   └── organization_service.py  # Establish Organization Business Activity (WP-01)
├── tests/                  # Pytest testing suite
│   ├── __init__.py
│   ├── conftest.py         # SQLAlchemy DB overrides and TestClient fixture state
│   ├── test_auth.py        # Endpoint integration and validations checks
│   ├── test_bootstrap_service.py  # WP-00
│   ├── test_feature_flags.py      # WP-00
│   ├── test_health.py             # WP-00
│   ├── test_organization_service.py  # WP-01
│   └── test_organization_api.py      # WP-01
├── dependencies.py         # Shared auth dependencies (require_platform_admin) — WP-01
├── observability.py       # Local audit/event/metric/correlation substitute (WP-00; see module docstring)
├── organization-api.yaml   # Organization Management OpenAPI contract (WP-01)
├── Dockerfile              # Optimized multi-stage Docker environment build
├── README.md               # Service documentation
├── main.py                 # Application entrypoint
└── requirements.txt        # Python production-grade packages catalog
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

## 🌱 Platform Bootstrap (WP-00)

A freshly-provisioned environment has no Roles, Permissions, or Platform Administrator
until bootstrap runs. Bootstrap is idempotent — safe to run on every deployment,
unconditionally:

```bash
export DATABASE_URL="postgresql+asyncpg://..."
python -m scripts.run_bootstrap
```

Full procedure, credential reference, and rollback strategy: [`docs/RUNBOOK_BOOTSTRAP.md`](docs/RUNBOOK_BOOTSTRAP.md).
Operational ownership: [`docs/OPERATIONAL_OWNERSHIP.md`](docs/OPERATIONAL_OWNERSHIP.md).

**Production safeguard (IC-001 M1):** the built-in demo/Platform Administrator password
hashes are public (visible in source). When `ENVIRONMENT=production`, bootstrap refuses
to seed them and requires `BOOTSTRAP_ADMIN_PASSWORD_HASH` /
`BOOTSTRAP_PLATFORM_ADMIN_PASSWORD_HASH` overrides — see the runbook.

### Liveness vs. Readiness

- `GET /health` — is the process alive and can it reach its database? Used by
  orchestrators to decide whether to **restart** an instance.
- `GET /ready` — is the process alive, reachable, **and** has bootstrap completed? Used
  by orchestrators to decide whether to **route traffic** to an instance.

### Feature Flags

Declared in `Config/platform-config.yaml` under `feature_flags`, evaluated via
`services.feature_flag_service.feature_flags`. Undeclared flags fail closed (`False`).
Flags may be scoped to a list of organization IDs for staged rollout, and overridden per
environment via `FF_<FLAG_NAME>=true|false`.

```yaml
feature_flags:
  ff_platform_workspace_v1:
    enabled: false
    organizations: null   # null = platform-wide once enabled; or a list of org UUID strings
```

---

## 🏢 Organization Management (WP-01)

BA-01 (Establish Organization Identity), BA-02 (Resolve Organization Details), BA-03 (Search &
List Organizations), BA-04 (Steward Organization Identity), BA-05 (Reactivate Suspended
Organization), BA-06 (Suspend Organization), and BA-07 (Retire Organization & Preserve
Continuity) of C-004, per IRA-001 (as revised by its §15 WP-01 Scope Reconciliation against the
canonical `PE-001-C004` Capability Specification) and ADR-003/004/005. **BA-07 is WP-01's final
Business Activity.**

- `POST /organizations` — requires `Authorization: Bearer <access_token>` for a caller holding
  the `PLATFORM_ADMIN` role. Rejects a duplicate `organization_code` with `409`.
- `GET /organizations/{organization_id}` — same authorization; `404` if the id doesn't exist.
- `GET /organizations` — same authorization; `q` (name/code substring), `status`
  (`ACTIVE`/`SUSPENDED`/`RETIRED`), `skip`/`limit` (pagination, max 100/page), `sort_by`/`sort_order`
  query params.
- `PUT /organizations/{organization_id}` — same authorization; `404` if the id doesn't exist.
  Updates `organization_name`, `organization_type`, `description`. `organization_code` and
  lifecycle `status` are immutable through this endpoint (code is the natural key; status is
  owned by the Reactivate/Suspend/Retire Business Activities).
- `POST /organizations/{organization_id}/activate` — same authorization; `404` if the id doesn't
  exist; `409` if already `ACTIVE` or if `RETIRED` (terminal — never reactivatable). Transitions
  `status` from `SUSPENDED` to `ACTIVE` (and syncs the legacy `is_active` boolean to `True`).
- `POST /organizations/{organization_id}/suspend` — same authorization; `404` if the id doesn't
  exist; `409` if already `SUSPENDED` or if `RETIRED` (terminal — never reversible). Transitions
  `status` from `ACTIVE` to `SUSPENDED` (and syncs `is_active` to `False`).
- `POST /organizations/{organization_id}/retire` — same authorization; `404` if the id doesn't
  exist; `409` if already `RETIRED`. Transitions `status` to `RETIRED` from either `ACTIVE` or
  `SUSPENDED` (and syncs `is_active` to `False`). Terminal and irreversible — no endpoint
  transitions a `RETIRED` organization to any other status. Preserves continuity: no row is
  deleted; the organization's identity and full history remain queryable via `GET
  /organizations/{organization_id}`.

All seven are tenant-agnostic (no `X-Tenant-ID` required).

Full contract: [`organization-api.yaml`](organization-api.yaml).

WP-01's Business Activity scope is complete as of BA-07 — see the WP-01 Scope Reconciliation in
`IRA-001` §15 and `IMP-REPORT-WP-01`'s corresponding section for why "Configuration" and "Audit
History" (originally planned as BA-07/BA-08) were removed: neither is a canonical C-004 Business
Activity per `PE-001-C004`.

---

## 🔒 Security Design: Multi-Tenancy

Each incoming HTTP request (excluding `health` and `docs`) is intercept-checked via `TenantMiddleware`. 

If the user does not provide `X-Tenant-ID` in the request headers, or provides an invalid representation, the application declines routing with an `HTTP 400 Bad Request` payload. On valid requests, it sets a localized, async-safe `ContextVar` that is referenced globally across service layers to protect cross-tenant boundary queries automatically.
