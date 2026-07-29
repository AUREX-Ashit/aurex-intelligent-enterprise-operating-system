-- ==============================================================================
-- Aurex Enterprise SaaS Platform - Core Database Physical Schema (DDL)
-- Target Platform: PostgreSQL 16+
-- Robust design featuring UUID Primary Keys, Audit Columns, Triggers,
-- Foreign Key Indexes, and Tenant Row-Level Security (RLS) Configuration.
-- ==============================================================================

-- Create system extensions standard boundaries
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==============================================================================
-- 0. Shared Helper Routines & Triggers
-- ==============================================================================

-- Common trigger function to automatically update 'updated_at' timestamp on modification.
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Helper to track current tenant context securely bypassing standard variables
CREATE OR REPLACE FUNCTION get_current_tenant_id()
RETURNS VARCHAR AS $$
BEGIN
    -- Pulls current_setting from session context; returns NULL instead of raising an error if unbound
    RETURN NULLIF(current_setting('app.current_tenant_id', true), '');
END;
$$ LANGUAGE plpgsql;

-- ==============================================================================
-- 1. Tenant Management Schema
-- ==============================================================================

CREATE TABLE tenants (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(64) UNIQUE NOT NULL,
    database_url VARCHAR(512),
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'SUSPENDED', 'TERMINATED', 'PROVISIONING')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trigger_tenants_updated_at
    BEFORE UPDATE ON tenants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================================================
-- 2. Identity & Access Management (IAM)
-- ==============================================================================

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(64) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trigger_roles_updated_at
    BEFORE UPDATE ON roles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE role_permissions (
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by VARCHAR(255) DEFAULT 'SYSTEM',
    updated_by VARCHAR(255) DEFAULT 'SYSTEM',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_tenant_email UNIQUE (tenant_id, email)
);

CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);

CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE user_roles (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);

CREATE INDEX idx_user_roles_tenant_id ON user_roles(tenant_id);

-- ==============================================================================
-- 3. Document Management File Vault
-- ==============================================================================

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    title VARCHAR(255) NOT NULL,
    file_type VARCHAR(64) NOT NULL, -- e.g., 'PDF', 'XLSX', 'CSV', 'DOCX'
    total_size BIGINT NOT NULL CHECK (total_size > 0),
    status VARCHAR(64) NOT NULL DEFAULT 'UPLOADED' CHECK (status IN ('UPLOADED', 'PARSING', 'PARSED', 'ANALYZING', 'ANALYZED', 'FAILED')),
    created_by VARCHAR(255) DEFAULT 'SYSTEM',
    updated_by VARCHAR(255) DEFAULT 'SYSTEM',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_tenant_id ON documents(tenant_id);
CREATE INDEX idx_documents_status ON documents(status);

CREATE TRIGGER trigger_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE document_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    version_number INT NOT NULL,
    s3_uri VARCHAR(512) NOT NULL, -- Location inside MinIO (e.g. s3://aurex-payloads/tenant-1/file.pdf)
    checksum VARCHAR(256) NOT NULL,
    created_by VARCHAR(255) DEFAULT 'SYSTEM',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_document_version UNIQUE (document_id, version_number)
);

CREATE INDEX idx_document_versions_tenant_id ON document_versions(tenant_id);
CREATE INDEX idx_document_versions_doc_id ON document_versions(document_id);

CREATE TABLE document_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    meta_key VARCHAR(128) NOT NULL,
    meta_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_document_metadata_key UNIQUE (document_id, meta_key)
);

CREATE INDEX idx_document_metadata_tenant_id ON document_metadata(tenant_id);

-- ==============================================================================
-- 4. ESG Metric Streams
-- ==============================================================================

CREATE TABLE esg_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(64) UNIQUE NOT NULL, -- e.g., 'GHG_SCOPE_1_EMISSIONS', 'WATER_CONSUMPTION_TOTAL'
    name VARCHAR(255) NOT NULL,
    category VARCHAR(64) NOT NULL CHECK (category IN ('ENVIRONMENTAL', 'SOCIAL', 'GOVERNANCE')),
    unit VARCHAR(32) NOT NULL, -- e.g., 'MT CO2e', 'm3', 'MWh'
    gri_index VARCHAR(64), -- Global Reporting Initiative standard code mapping
    sasb_code VARCHAR(64), -- Sustainability Accounting Standards Board mapping
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trigger_esg_metrics_updated_at
    BEFORE UPDATE ON esg_metrics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE esg_metric_values (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    metric_id UUID NOT NULL REFERENCES esg_metrics(id) ON DELETE RESTRICT,
    value DECIMAL(18, 4) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    source_type VARCHAR(64) NOT NULL DEFAULT 'MANUAL' CHECK (source_type IN ('MANUAL', 'AI_INTEGRATION', 'SYSTEM_ESTIMATE')),
    created_by VARCHAR(255) DEFAULT 'SYSTEM',
    updated_by VARCHAR(255) DEFAULT 'SYSTEM',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_duration CHECK (period_end >= period_start)
);

CREATE INDEX idx_esg_metric_values_tenant_id ON esg_metric_values(tenant_id);
CREATE INDEX idx_esg_metric_values_metric_id ON esg_metric_values(metric_id);
CREATE INDEX idx_esg_metric_values_periods ON esg_metric_values(period_start, period_end);

CREATE TRIGGER trigger_esg_metric_values_updated_at
    BEFORE UPDATE ON esg_metric_values
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================================================
-- 5. Sustainable Development Goals (SDG) Alignment
-- ==============================================================================

CREATE TABLE sdg_goals (
    id INT PRIMARY KEY, -- 1 to 17 standard identifiers
    code VARCHAR(32) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    icon_url VARCHAR(255)
);

CREATE TABLE sdg_mappings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    esg_metric_id UUID NOT NULL REFERENCES esg_metrics(id) ON DELETE CASCADE,
    sdg_id INT NOT NULL REFERENCES sdg_goals(id) ON DELETE RESTRICT,
    mapping_weight DECIMAL(3, 2) NOT NULL DEFAULT 1.00 CHECK (mapping_weight >= 0.00 AND mapping_weight <= 1.00),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sdg_mappings_tenant_id ON sdg_mappings(tenant_id);
CREATE INDEX idx_sdg_mappings_metric_id ON sdg_mappings(esg_metric_id);

-- ==============================================================================
-- 6. AI Extraction Framework
-- ==============================================================================

CREATE TABLE extractions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    esg_metric_id UUID REFERENCES esg_metrics(id) ON DELETE SET NULL,
    extracted_value DECIMAL(18, 4),
    confidence_score DECIMAL(5, 4) NOT NULL CHECK (confidence_score >= 0.0000 AND confidence_score <= 1.0000),
    context_chunk TEXT NOT NULL, -- Exact text or snippet proving the value derivation
    ai_model VARCHAR(128) NOT NULL, -- e.g., 'gemini-1.5-pro'
    status VARCHAR(64) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'VALIDATED', 'OVERRIDDEN', 'REJECTED')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_extractions_tenant_id ON extractions(tenant_id);
CREATE INDEX idx_extractions_document_id ON extractions(document_id);
CREATE INDEX idx_extractions_status ON extractions(status);

CREATE TRIGGER trigger_extractions_updated_at
    BEFORE UPDATE ON extractions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE validations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    extraction_id UUID NOT NULL REFERENCES extractions(id) ON DELETE CASCADE,
    validated_by UUID REFERENCES users(id) ON DELETE SET NULL,
    original_value DECIMAL(18, 4),
    validated_value DECIMAL(18, 4) NOT NULL,
    status VARCHAR(64) NOT NULL DEFAULT 'APPROVED' CHECK (status IN ('APPROVED', 'MODIFIED', 'FLAGGED')),
    user_feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_validations_tenant_id ON validations(tenant_id);
CREATE INDEX idx_validations_extraction_id ON validations(extraction_id);

CREATE TABLE scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    category VARCHAR(62) NOT NULL CHECK (category IN ('ENVIRONMENTAL', 'SOCIAL', 'GOVERNANCE', 'COMPOSITE')),
    score_value DECIMAL(5, 2) NOT NULL CHECK (score_value >= 0.00 AND score_value <= 100.00),
    calculation_date DATE NOT NULL,
    methodology_version VARCHAR(32) NOT NULL DEFAULT 'v1.0',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scores_tenant_id ON scores(tenant_id);
CREATE INDEX idx_scores_category_date ON scores(tenant_id, category, calculation_date DESC);

-- ==============================================================================
-- 7. Reporting & Analytics
-- ==============================================================================

CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    title VARCHAR(255) NOT NULL,
    standard VARCHAR(64) NOT NULL CHECK (standard IN ('GRI', 'SASB', 'TCFD', 'CSRD', 'INTERNAL')),
    period_year INT NOT NULL CHECK (period_year >= 2000 AND period_year <= 2100),
    status VARCHAR(64) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'UNDER_REVIEW', 'APPROVED', 'ARCHIVED')),
    created_by VARCHAR(255) DEFAULT 'SYSTEM',
    updated_by VARCHAR(255) DEFAULT 'SYSTEM',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_tenant_report UNIQUE (tenant_id, standard, period_year)
);

CREATE INDEX idx_reports_tenant_id ON reports(tenant_id);

CREATE TRIGGER trigger_reports_updated_at
    BEFORE UPDATE ON reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE report_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    tenant_id VARCHAR(64) NOT NULL REFERENCES tenants(id) ON DELETE RESTRICT,
    revision INT NOT NULL,
    compiled_body JSONB NOT NULL, -- Full dump of parameters structured inside document version
    output_s3_uri VARCHAR(512), -- Compiled physical PDF snapshot path in S3
    created_by VARCHAR(255) DEFAULT 'SYSTEM',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_report_revision UNIQUE (report_id, revision)
);

CREATE INDEX idx_report_versions_tenant_id ON report_versions(tenant_id);

-- ==============================================================================
-- 8. Immutable Enterprise Audits
-- ==============================================================================

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(64) REFERENCES tenants(id) ON DELETE SET NULL,
    user_id VARCHAR(255) NOT NULL DEFAULT 'ANONYMOUS',
    action VARCHAR(128) NOT NULL, -- e.g., 'security.login_failed', 'document.delete'
    status VARCHAR(32) NOT NULL DEFAULT 'SUCCESS' CHECK (status IN ('SUCCESS', 'FAILURE', 'DENIED')),
    ip_address VARCHAR(45),
    correlation_id VARCHAR(64),
    payload JSONB, -- Context variables snapshot (e.g. mutated fields)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_tenant_id ON audit_logs(tenant_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action, created_at DESC);

-- ==============================================================================
-- 9. Row-Level Security (RLS) Configuration
-- ==============================================================================

-- Enable Row-Level Security explicitly on ALL multi-tenant entities
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_metadata ENABLE ROW LEVEL SECURITY;
ALTER TABLE esg_metric_values ENABLE ROW LEVEL SECURITY;
ALTER TABLE sdg_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE extractions ENABLE ROW LEVEL SECURITY;
ALTER TABLE validations ENABLE ROW LEVEL SECURITY;
ALTER TABLE scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE report_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Construct Global isolation rules. These rules check if the row's 'tenant_id' matches
-- the session-scoped tenant identification token 'app.current_tenant_id'.

CREATE POLICY tenant_isolation_users_policy ON users
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_user_roles_policy ON user_roles
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_documents_policy ON documents
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_document_versions_policy ON document_versions
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_document_metadata_policy ON document_metadata
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_esg_metric_values_policy ON esg_metric_values
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_sdg_mappings_policy ON sdg_mappings
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_extractions_policy ON extractions
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_validations_policy ON validations
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_scores_policy ON scores
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_reports_policy ON reports
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_report_versions_policy ON report_versions
    FOR ALL USING (tenant_id = get_current_tenant_id());

CREATE POLICY tenant_isolation_audit_logs_policy ON audit_logs
    FOR ALL USING (tenant_id = get_current_tenant_id() OR tenant_id IS NULL);
