# CorpStage Enterprise Platform Docker Infrastructure

This repository encapsulates the standard local development, testing, and integration infrastructure for the CorpStage Multi-Tenant SaaS platform. It leverages **Docker Compose v3.9+** to orchestrate high-fidelity database structures, caching proxies, telemetry queues, object storage vaults, and core application services.

---

## 🏛️ System Architecture Layout

The CorpStage architecture runs inside a dedicated isolated bridge network (`corpstage-network`), restricting cross-service queries whilst providing granular pathways for microservice integrations:

```
  ◄── External client APIs port ingress ────────────────────────────────────►
                         │
         ┌───────────────┼───────────────┬────────────────┬──────────────┐
         ▼               ▼               ▼                ▼              ▼
   [AuthService]  [TenantService]  [IngestionSvc]   [AIService]    [ReportingSvc]
     (:8001)         (:8002)         (:8003)         (:8004)        (:8005)
         │               │               │                │              │
   ┌─────┴─────┐         │               ├──────────┐     ├────────┐     │
   ▼           ▼         ▼               ▼          ▼     ▼        ▼     ▼
 [Redis]   [Postgres] [Kafka]        [MinIO]     [Kafka][Redis]  [Postgres]
 (:6379)    (:5432)   (:9092)        (:9000)     (:9092)(:6379)  (:5432)
```

---

## 💾 Core Infrastructure Services

| Service Name | Technology | Internal Endpoint | External Endpoint | Role / Usage Scopes |
| :--- | :--- | :--- | :--- | :--- |
| **PostgreSQL 16** | Relational Database | `postgres:5432` | `localhost:5432` | Relational store, schema isolation (RLS) |
| **Redis Cache** | In-Memory Dictionary | `redis:6379` | `localhost:6379` | Token caching, session tracking, rate-limiting |
| **Zookeeper** | Consensus Service | `zookeeper:2181` | N/A | Kafka broker orchestration & heartbeat metadata |
| **Apache Kafka** | Streaming Platform | `kafka:9092` | `localhost:29092` | Message pipeline, domain event subscription |
| **MinIO** | S3 Object Engine | `minio:9000` | `localhost:9000` | S3-compliant store (ESG file ingestion payload) |

---

## 🔑 Service Connection Documentation

To preserve modularity and security, each microservice connects using specific database schemas and users rather than full database administrator privileges.

### 1. AuthService
* **PostgreSQL:** Injects user `auth_service_user` targeting schema `auth_schema`.
  ```ini
  DATABASE_URL=postgresql://auth_service_user:AuthServiceSecretPass123!@postgres:5432/corpstage?sslmode=disable
  ```
* **Redis:** Connects to cache pools on database `0`.
  ```ini
  REDIS_HOST=redis
  REDIS_PORT=6379
  ```

### 2. TenantService
* **PostgreSQL:** Injects user `tenant_service_user` targeting schema `tenant_schema`.
  ```ini
  DATABASE_URL=postgresql://tenant_service_user:TenantServiceSecretPass123!@postgres:5432/corpstage?sslmode=disable
  ```
* **Kafka:** Publishes tenant creation events `corpstage.tenant.provisioning` on topic stream.
  ```ini
  KAFKA_BOOTSTRAP_SERVERS=kafka:9092
  ```

### 3. IngestionService
* **PostgreSQL:** Injects user `ingestion_service_user` targeting schema `ingestion_schema`.
  ```ini
  DATABASE_URL=postgresql://ingestion_service_user:IngestionServiceSecretPass123!@postgres:5432/corpstage?sslmode=disable
  ```
* **Kafka:** Subscribes to ingestion topic schemas.
  ```ini
  KAFKA_BOOTSTRAP_SERVERS=kafka:9092
  ```
* **MinIO Object Vault:** Accesses `corpstage-ingestion-payloads` bucket over S3 API.
  ```ini
  MINIO_ENDPOINT=http://minio:9000
  MINIO_ACCESS_KEY=corpstage_admin
  MINIO_SECRET_KEY=CorpStageAdminPass123!
  ```

### 4. AIService
* **PostgreSQL:** Injects user `ai_service_user` targeting schema `ai_schema`.
  ```ini
  DATABASE_URL=postgresql://ai_service_user:AIServiceSecretPass123!@postgres:5432/corpstage?sslmode=disable
  ```
* **Redis:** Caches embedding patterns.
  ```ini
  REDIS_HOST=redis
  REDIS_PORT=6379
  ```
* **Kafka:** Outputs audit telemetry events to `corpstage.ai.inference.logs`.
  ```ini
  KAFKA_BOOTSTRAP_SERVERS=kafka:9092
  ```

### 5. ReportingService
* **PostgreSQL:** Injects user `reporting_service_user` targeting schema `reporting_schema`.
  ```ini
  DATABASE_URL=postgresql://reporting_service_user:ReportingServiceSecretPass123!@postgres:5432/corpstage?sslmode=disable
  ```
* **Kafka:** Reads cross-service events to build reports.
  ```ini
  KAFKA_BOOTSTRAP_SERVERS=kafka:9092
  ```

---

## ⚡ Setup and Operation Cycles

### Standard Prerequisites
Ensure you have the latest stable dependencies running locally:
* **Docker Engine:** `v20.10+`
* **Docker Compose:** `v2.20+`

### Step 1: Initialize System Environment Configuration
Copy the default parameters template to establish your local variable scope:
```bash
cp .env.example .env
```

### Step 2: Build and Bootstrap Infrastructure Services
To launch PostgreSQL, Redis, Kafka, and MinIO alongside auto-provisioning databases tables and storage buckets, run:
```bash
docker compose up -d postgres redis kafka minio kafka-init-topics minio-init-buckets
```

### Step 3: Run Full Suite Including Application Microservices
To compile and boot the entire platform including custom core application services, run:
```bash
docker compose up -d --build
```

### Step 4: Verify Containers Health States
Execute standard status checks to ensure any database or storage ready limits are satisfied:
```bash
docker compose ps
```

### Step 5: Tear Down Development Environments
To stop execution, preserve named storage volume states, and cleanly reclaim network interfaces:
```bash
docker compose down
```
To fully purge databases state and storage cache directories:
```bash
docker compose down -v
```
