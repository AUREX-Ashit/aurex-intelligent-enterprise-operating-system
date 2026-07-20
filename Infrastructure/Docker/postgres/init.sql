-- CorpStage Enterprise Platform - PostgreSQL Initialization Script
-- Bootstraps microservice-specific schemas, execution users, and security isolation layers.

SELECT 'Bootstrapping CorpStage PostgreSQL Instance...' AS progress_marker;

-- 1. Create Core Database and Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Configure Microservice-Specific Execution Roles (RBAC)
-- These separate users prevent any single service compromise from gaining complete database ownership.
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'auth_service_user') THEN
        CREATE ROLE auth_service_user WITH LOGIN PASSWORD 'AuthServiceSecretPass123!';
    END IF;

    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'tenant_service_user') THEN
        CREATE ROLE tenant_service_user WITH LOGIN PASSWORD 'TenantServiceSecretPass123!';
    END IF;

    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'ingestion_service_user') THEN
        CREATE ROLE ingestion_service_user WITH LOGIN PASSWORD 'IngestionServiceSecretPass123!';
    END IF;

    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'ai_service_user') THEN
        CREATE ROLE ai_service_user WITH LOGIN PASSWORD 'AIServiceSecretPass123!';
    END IF;

    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'reporting_service_user') THEN
        CREATE ROLE reporting_service_user WITH LOGIN PASSWORD 'ReportingServiceSecretPass123!';
    END IF;
END
$$;

-- 3. Provision Microservice Schemas
CREATE SCHEMA IF NOT EXISTS auth_schema AUTHORIZATION auth_service_user;
CREATE SCHEMA IF NOT EXISTS tenant_schema AUTHORIZATION tenant_service_user;
CREATE SCHEMA IF NOT EXISTS ingestion_schema AUTHORIZATION ingestion_service_user;
CREATE SCHEMA IF NOT EXISTS ai_schema AUTHORIZATION ai_service_user;
CREATE SCHEMA IF NOT EXISTS reporting_schema AUTHORIZATION reporting_service_user;

-- 4. Set Schema Default Privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA auth_schema GRANT ALL ON TABLES TO auth_service_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA tenant_schema GRANT ALL ON TABLES TO tenant_service_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ingestion_schema GRANT ALL ON TABLES TO ingestion_service_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ai_schema GRANT ALL ON TABLES TO ai_service_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA reporting_schema GRANT ALL ON TABLES TO reporting_service_user;

-- 5. Build Shared Tenant Routing Registry
-- Used by TenantService to manage global multitenant mappings
CREATE TABLE IF NOT EXISTS tenant_schema.tenants (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(64) UNIQUE NOT NULL,
    database_url VARCHAR(512) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Grant Read-Only permissions on Tenant Mapping registry to cross-cutting services for RLS
GRANT USAGE ON SCHEMA tenant_schema TO auth_service_user, ingestion_service_user, ai_service_user, reporting_service_user;
GRANT SELECT ON tenant_schema.tenants TO auth_service_user, ingestion_service_user, ai_service_user, reporting_service_user;

SELECT 'PostgreSQL bootstrapping completed successfully.' AS progress_marker;
