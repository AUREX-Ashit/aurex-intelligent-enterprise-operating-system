"""
Initial Schema Core Migration.

Revision ID: 001_initial_schema
Revises: None
Create Date: 2026-05-29 09:14:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers, used by Alembic.
revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Performs database upgrade cycles creating all schemas, indexes, and tables programmatically."""
    
    # 1. Tenant Management Registry
    op.create_table(
        "tenants",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("subdomain", sa.String(length=64), nullable=False),
        sa.Column("database_url", sa.String(length=512), nullable=True),
        sa.Column("status", sa.String(length=32), server_default="ACTIVE", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("subdomain")
    )

    # 2. IAM Core permissions and roles
    op.create_table(
        "permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code")
    )

    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name")
    )

    op.create_table(
        "role_permissions",
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("permission_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "permission_id")
    )

    # Users Registry
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=128), nullable=True),
        sa.Column("last_name", sa.String(length=128), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("updated_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "email", name="unique_tenant_email")
    )
    op.create_index("idx_users_tenant_id", "users", ["tenant_id"])
    op.create_index("idx_users_email", "users", ["email"])

    op.create_table(
        "user_roles",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id")
    )
    op.create_index("idx_user_roles_tenant_id", "user_roles", ["tenant_id"])

    # 3. Document Management File Vault
    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("file_type", sa.String(length=64), nullable=False),
        sa.Column("total_size", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(length=64), server_default="UPLOADED", nullable=False),
        sa.Column("created_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("updated_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("idx_documents_tenant_id", "documents", ["tenant_id"])
    op.create_index("idx_documents_status", "documents", ["status"])

    op.create_table(
        "document_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("document_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("s3_uri", sa.String(length=512), nullable=False),
        sa.Column("checksum", sa.String(length=256), nullable=False),
        sa.Column("created_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("document_id", "version_number", name="unique_document_version")
    )
    op.create_index("idx_document_versions_tenant_id", "document_versions", ["tenant_id"])
    op.create_index("idx_document_versions_doc_id", "document_versions", ["document_id"])

    op.create_table(
        "document_metadata",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("document_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("meta_key", sa.String(length=128), nullable=False),
        sa.Column("meta_value", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("document_id", "meta_key", name="unique_document_metadata_key")
    )
    op.create_index("idx_document_metadata_tenant_id", "document_metadata", ["tenant_id"])

    # 4. ESG Metric Streams
    op.create_table(
        "esg_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("unit", sa.String(length=32), nullable=False),
        sa.Column("gri_index", sa.String(length=64), nullable=True),
        sa.Column("sasb_code", sa.String(length=64), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code")
    )

    op.create_table(
        "esg_metric_values",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("metric_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("value", sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("source_type", sa.String(length=64), server_default="MANUAL", nullable=False),
        sa.Column("created_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("updated_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["metric_id"], ["esg_metrics.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("idx_esg_metric_values_tenant_id", "esg_metric_values", ["tenant_id"])
    op.create_index("idx_esg_metric_values_metric_id", "esg_metric_values", ["metric_id"])
    op.create_index("idx_esg_metric_values_periods", "esg_metric_values", ["period_start", "period_end"])

    # 5. SDG catalog and mappings
    op.create_table(
        "sdg_goals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("icon_url", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code")
    )

    op.create_table(
        "sdg_mappings",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("esg_metric_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sdg_id", sa.Integer(), nullable=False),
        sa.Column("mapping_weight", sa.Numeric(precision=3, scale=2), server_default="1.00", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["esg_metric_id"], ["esg_metrics.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sdg_id"], ["sdg_goals.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("idx_sdg_mappings_tenant_id", "sdg_mappings", ["tenant_id"])
    op.create_index("idx_sdg_mappings_metric_id", "sdg_mappings", ["esg_metric_id"])

    # 6. AI Inferences/Extractions & Scores
    op.create_table(
        "extractions",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("esg_metric_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("extracted_value", sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column("confidence_score", sa.Numeric(precision=5, scale=4), nullable=False),
        sa.Column("context_chunk", sa.Text(), nullable=False),
        sa.Column("ai_model", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=64), server_default="PENDING", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["esg_metric_id"], ["esg_metrics.id"], ondelete="SET_NULL"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("idx_extractions_tenant_id", "extractions", ["tenant_id"])
    op.create_index("idx_extractions_document_id", "extractions", ["document_id"])
    op.create_index("idx_extractions_status", "extractions", ["status"])

    op.create_table(
        "validations",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("extraction_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("validated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("original_value", sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column("validated_value", sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column("status", sa.String(length=64), server_default="APPROVED", nullable=False),
        sa.Column("user_feedback", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["extraction_id"], ["extractions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["validated_by"], ["users.id"], ondelete="SET_NULL"),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("idx_validations_tenant_id", "validations", ["tenant_id"])
    op.create_index("idx_validations_extraction_id", "validations", ["extraction_id"])

    op.create_table(
        "scores",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("category", sa.String(length=62), nullable=False),
        sa.Column("score_value", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("calculation_date", sa.Date(), nullable=False),
        sa.Column("methodology_version", sa.String(length=32), server_default="v1.0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("idx_scores_tenant_id", "scores", ["tenant_id"])

    # 7. Reporting & Disclosures
    op.create_table(
        "reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("standard", sa.String(length=64), nullable=False),
        sa.Column("period_year", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=64), server_default="DRAFT", nullable=False),
        sa.Column("created_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("updated_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "standard", "period_year", name="unique_tenant_report")
    )
    op.create_index("idx_reports_tenant_id", "reports", ["tenant_id"])

    op.create_table(
        "report_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("report_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("compiled_body", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("output_s3_uri", sa.String(length=512), nullable=True),
        sa.Column("created_by", sa.String(length=255), server_default="SYSTEM", nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["report_id"], ["reports.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("report_id", "revision", name="unique_report_revision")
    )
    op.create_index("idx_report_versions_tenant_id", "report_versions", ["tenant_id"])

    # 8. Immutable audits
    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("user_id", sa.String(length=255), server_default="ANONYMOUS", nullable=False),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), server_default="SUCCESS", nullable=False),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="SET_NULL"),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("idx_audit_logs_tenant_id", "audit_logs", ["tenant_id"])
    op.create_index("idx_audit_logs_action", "audit_logs", ["action", "created_at"])


def downgrade() -> None:
    """Safely tears down the schema in precise reverse-dependency order."""
    op.drop_table("audit_logs")
    op.drop_table("report_versions")
    op.drop_table("reports")
    op.drop_table("scores")
    op.drop_table("validations")
    op.drop_table("extractions")
    op.drop_table("sdg_mappings")
    op.drop_table("sdg_goals")
    op.drop_table("esg_metric_values")
    op.drop_table("esg_metrics")
    op.drop_table("document_metadata")
    op.drop_table("document_versions")
    op.drop_table("documents")
    op.drop_table("user_roles")
    op.drop_table("users")
    op.drop_table("role_permissions")
    op.drop_table("roles")
    op.drop_table("permissions")
    op.drop_table("tenants")
