# CorpStage Enterprise SaaS - Relational Database Platform

This directory contains the core physical data architectures and schema controls required for the Core CorpStage Plattform. It provides a highly partitionable, audit-tracked relational core modeling tenant directories, access frameworks, file metadata structures, UN Sustainable Development Goals (SDGs), and ESG metrics compliance pipelines.

---

## 📂 Database Workspace Directory Structure

```
Database/
├── ERD/
│   └── README.md              # Logical/Physical Entity-Relationship Model (Mermaid.js)
├── DDL/
│   └── schema.sql             # Raw DDL layout including triggers, RLS and policies
├── Migrations/
│   ├── env.py                 # Core Alembic setup script mapping connection configurations
│   └── versions/
│       └── 001_initial_schema.py   # Initial Alembic execution history migration
└── Seeds/
    └── seed_data.sql          # Standard master parameters (17 UN SDGs, ESG taxonomies, RBAC mapping)
```

---

## 🏛️ Tenant-Isolation Model & RLS Architecture

CorpStage utilizes a **shared-database, isolated-schema** multi-tenant paradigm. This model enforces logical isolation of sensitive tenant details using **PostgreSQL Row-Level Security (RLS) policies** combined with foreign key indices.

### How Row-Level Security (RLS) Works
Every tenant-scoped table features a non-nullable `tenant_id` field. Rather than adding tedious `WHERE tenant_id = ?` bounds manually inside each CRUD database query, PostgreSQL filters rows automatically at the engine layer based on a session context token.

The policy verifies ownership by comparing the row's `tenant_id` with the current session variable value:
```sql
CREATE POLICY tenant_isolation_documents_policy ON documents
    FOR ALL USING (tenant_id = current_setting('app.current_tenant_id', true));
```

### Simulating/Verifying the Isolation Policies in SQL Client
Developers or background service workers activate specific tenant filters by declaring the session variables inside a transactional block scope:

```sql
BEGIN;

-- 1. Initialize session to "Tenant Alpha"
SET LOCAL app.current_tenant_id = 'tenant_alpha_uuid';

-- 2. Query documents - only documents owning tenant_id = 'tenant_alpha_uuid' return
SELECT id, title, tenant_id FROM documents;

-- 3. Switch session to "Tenant Beta"
SET LOCAL app.current_tenant_id = 'tenant_beta_uuid';

-- 4. Query again - database strictly returns beta's documentation
SELECT id, title, tenant_id FROM documents;

COMMIT;
```

---

## 🛠️ Schema Migrations Strategy (Alembic)

The platform implements **Alembic** as a declarative migration engine.

### Run Online Migration (Database Upgrades)
Ensure you set the target `DATABASE_URL` context variable and carry out the standard upgrade cmd:

```bash
# Export the matching environment connection parameters
export DATABASE_URL="postgresql://postgres:CorpStageMasterDatabasePass123!@localhost:5432/corpstage?sslmode=disable"

# Run alembic upgrade to the head revision
alembic upgrade head
```

### Run Downward Migration (Database Rollbacks)
To safety back out the entire initial database schema sequence:

```bash
alembic downgrade base
```

---

## 🧬 Taxonomy & Metric Standards (Master Seeds)

CorpStage incorporates standard corporate governance taxonomies out-of-the-box. Running `/corpstage/database/seeds/seed_data.sql` populates:

1. **UN Sustainable Development Goals (SDGs):** Immutable database representation of Goals 1 through 17 which can be linked to metrics profiles via the `sdg_mappings` join table.
2. **ESG Metric Rules Catalog:** Predefined taxonomy indexes mapped directly to standard disclosure standards such as the **GRI (Global Reporting Initiative)** index and **SASB (Sustainability Accounting Standards Board)** codes, including:
   * **Scope 1, 2, and 3 Greenhouse Gas (GHG) emissions** (MT CO2e)
   * **Total Energy Consumption** (MWh)
   * **Water withdrawal volumes** (m³)
   * **Gender representation ratios** and general workforce turnovers (%)
   * **TRIR Injury ratios** and safety metrics
   * **Board council independence ratios** (%)
3. **Role-Based Access Control (RBAC) Mapping:** Provisions system roles (`TenantAdmin`, `DataIngester`, `ESGEditor`, `Auditor`, `SystemAdmin`) and maps them to standard operational permissions (`tenant:read`, `document:write`, `metric:edit`, `ai:extract`, `report:review`).
