# CorpStage TenantService

Production-grade, asynchronous SaaS Tenant, Organization, and Workspace provisioning microservice.

Designed for high durability, strict isolation, and robust configurations matching the **CorpStage Enterprise Platform**.

---

## 🛠 Tech Stack

- **Runtime**: Python 3.14
- **Framework**: FastAPI (Asynchronous engine)
- **Validation**: Pydantic v2
- **ORM/Engine**: SQLAlchemy 2.x Async + Postgres Asyncpg
- **Database Migrations**: Alembic
- **Ecosystem**: Multi-tenant database schema architecture, Docker orchestration

---

## 📂 Directories Layout

```text
TenantService/
├── main.py                    # Root bootstrapping and FastAPI lifespan
├── requirements.txt           # Standard Python packages specification
├── Dockerfile                 # Production multi-stage Docker deployment
├── README.md                  # Microservice system handbook
├── config/
│   ├── settings.py            # Pydantic Settings class parsing platform-config.yaml
│   ├── platform-config.yaml   # Original Corpstage Enterprise platform parameters
│   └── tenant-api.yaml        # Original Corpstage Tenant OpenAPI specification
├── models/
│   ├── base.py                # DeclarativeBase foundation with general UUID keys
│   └── tenant.py              # Tenant, TenantConfig, and TenantUser database schemas
├── repositories/
│   ├── base.py                # Abstract generic CRUD Repository base
│   └── tenant_repo.py         # Specialized repositories for tenants and users
├── routers/
│   └── tenant.py              # REST routing endpoints including onboarding
├── services/
│   └── tenant_service.py      # Business process orchestrator (scaffolded)
└── middleware/
    ├── tenant.py              # Multi-tenant header extraction and ContextVar storage
    └── logging.py             # Highly trace-friendly structured JSON request logs
```

---

## ⚙ Configurations and Environment Precedence

The service loads all presets from `config/platform-config.yaml`. However, any configuration item can be dynamically overridden using standard environment variables prefixed with `CORPSTAGE_` and utilizing double underscores (`__`) to delimit nested JSON blocks:

| Pydantic Parameter | Equivalent Env Variable | Default Value | Description |
|---|---|---|---|
| `platform.environment` | `CORPSTAGE_PLATFORM__ENVIRONMENT` | `development` | Active build profile |
| `database.postgresql.host` | `CORPSTAGE_DATABASE__POSTGRESQL__HOST` | `localhost`| Database IP / hostname |
| `database.postgresql.password` | `CORPSTAGE_DATABASE__POSTGRESQL__PASSWORD` | `CHANGE_IN_ENVIRONMENT` | Postgres authentications |
| `authentication.tenant.header_name` | `CORPSTAGE_AUTHENTICATION__TENANT__HEADER_NAME` | `X-Tenant-ID` | Incoming Tenant HTTP Header |

---

## 🧭 REST APIs

All routes return high-fidelity, strictly typed JSON matching the OpenAPI spec.

### 🌐 Global / Platform Standard

#### 1. Index Specification
- **Method / Path**: `GET /`
- **Response**: Details active system capabilities, workspace features, and OpenAPI links.

#### 2. Service health
- **Method / Path**: `GET /health`
- **Response**: Deep connectivity statuses for dependencies (Database, AI gateway, Storage).

---

### 🏢 Tenant Management APIs (Namespace `/tenant`)

#### 1. Tenant Creation
- **Method / Path**: `POST /tenant/create`
- **Header Required**: None
- **Body**: `TenantCreate`
- **Response**: Configured Tenant metadata matching Swagger spec.

#### 2. Advanced Onboarding Orchestration
- **Method / Path**: `POST /tenant/onboard`
- **Header Required**: None
- **Body**: `TenantOnboardRequest`
- **Description**: Atomically provisions standard tenant accounts, configures default themes / security policies, and maps primary administrators in single lifecycle events.

#### 3. Contextual Tenant Users
- **Method / Path**: `GET /tenant/users`
- **Header Required**: `X-Tenant-ID: <UUID_V4>`
- **Description**: Fully context-bound query extracting user arrays registered inside the tenant partition specified in the header.

#### 4. Active Configuration GET
- **Method / Path**: `GET /tenant/config`
- **Header Required**: `X-Tenant-ID: <UUID_V4>`
- **Response**: Active theme configurations, custom CORS origins, security policies, and AI preferences.

#### 5. Active Configuration PUT
- **Method / Path**: `PUT /tenant/config`
- **Header Required**: `X-Tenant-ID: <UUID_V4>`
- **Body**: `TenantConfigBase`
- **Response**: Reflects and updates global parameters contextually.

---

## 🚀 Running Locally

Ensure Python 3.14 is installed.

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Run server locally
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

## 🐳 Running Under Docker

To verify the Docker container build:

```bash
docker build -t corpstage-tenant-service .
docker run -p 3000:3000 corpstage-tenant-service
```
