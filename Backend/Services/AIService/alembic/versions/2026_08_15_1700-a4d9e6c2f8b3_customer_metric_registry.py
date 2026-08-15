"""customer_metric_registry

Revision ID: a4d9e6c2f8b3
Revises: f3b8d5a2c7e1
Create Date: 2026-08-15 17:00:00.000000

WP-14 BA-03 — Resolve Enterprise Intelligence Candidate (Convergence
Decision). Extends AIService's existing Alembic chain (WP-14 BA-02's own
`f3b8d5a2c7e1`) — does not bootstrap a second one. Introduces
`customer_metric_registry`, combining its base `CREATE TABLE`
(`Master_Technical_Architecture.md:4263`), its own later Binding-3 rework
`ALTER TABLE` (`Master_Technical_Architecture.md:5410`), AND its own
AMD-007 Hide/Purge governance `ALTER TABLE` (`Master_Technical_Architecture.md:5541`)
into a single `CREATE TABLE` here — no column added, removed, or retyped
beyond what those three LOCKED DDL blocks together specify (corrected
per the Gate 1 independent certification's own Finding 4, which found
this migration, as originally written, had combined only the first two
blocks). `purge_audit_log` — the separate table AMD-007 also introduces
— is not created here; Hide/Purge are unchartered actions no WP-14
Business Activity performs.

Does not create `metric_registry`, `customer_domain_registry`, or
`user_registry` — none has a physical Backend model anywhere in this
repository; `semantic_match_result_metric_id`/`customer_domain_id`/
`requested_by_user_id` (etc.) are declared with no FK, logical only, the
same disposition already established for BA-01's/BA-02's/BA-04's own
optional cross-registry references.

`ck_customer_metric_registry_semantic_match_score` (`CHECK
(semantic_match_score BETWEEN 0 AND 1)`,
`Master_Technical_Architecture.md:5418-5419`) added in Gate 2 V&V
remediation (Finding 3) — the Binding-3 rework block's own `semantic_
match_score` `CHECK` was previously omitted despite the column's own
correct type/precision (`NUMERIC(4,3)`) already being present.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a4d9e6c2f8b3'
down_revision: Union[str, Sequence[str], None] = 'f3b8d5a2c7e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'customer_metric_registry',
        sa.Column('customer_metric_id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('customer_domain_id', sa.Uuid(), nullable=True),
        sa.Column('metric_name', sa.String(255), nullable=False),
        sa.Column('metric_code', sa.String(100), nullable=False),
        sa.Column('metric_description', sa.Text(), nullable=True),
        sa.Column('unit_of_measure', sa.String(50), nullable=True),
        sa.Column('formula_logic', sa.Text(), nullable=True),
        sa.Column('source_type', sa.String(50), nullable=True),
        sa.Column('requested_by_user_id', sa.Uuid(), nullable=False),
        sa.Column('approval_status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('approved_by_user_id', sa.Uuid(), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('evidence_required_flag', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('ai_extractable_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('active_flag', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('cde_tier', sa.String(20), nullable=False, server_default='TENANT'),
        sa.Column('semantic_match_attempted_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('semantic_match_result_metric_id', sa.Uuid(), nullable=True),
        sa.Column('semantic_match_score', sa.Numeric(4, 3), nullable=True),
        sa.Column('semantic_match_rejected_reason', sa.Text(), nullable=True),
        sa.Column('convergence_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('promotion_requested_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('promotion_requested_by', sa.Uuid(), nullable=True),
        sa.Column('promotion_requested_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('promotion_decision', sa.String(20), nullable=True),
        sa.Column('promotion_decided_by', sa.Uuid(), nullable=True),
        sa.Column('promotion_decided_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_hidden_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('hidden_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_purged_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('purge_requested_by', sa.Uuid(), nullable=True),
        sa.Column('purge_requested_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('purge_approved_by', sa.Uuid(), nullable=True),
        sa.Column('purge_approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('purge_reason', sa.Text(), nullable=True),
        sa.CheckConstraint(
            "approval_status IN ('pending', 'approved', 'rejected')",
            name='ck_customer_metric_registry_approval_status',
        ),
        sa.CheckConstraint(
            "cde_tier IN ('TENANT', 'TEMPORARY')",
            name='ck_customer_metric_registry_cde_tier',
        ),
        sa.CheckConstraint(
            "promotion_decision IS NULL OR promotion_decision IN ('PENDING', 'APPROVED', 'REJECTED')",
            name='ck_customer_metric_registry_promotion_decision',
        ),
        sa.CheckConstraint(
            "semantic_match_score BETWEEN 0 AND 1",
            name='ck_customer_metric_registry_semantic_match_score',
        ),
        sa.PrimaryKeyConstraint('customer_metric_id'),
        sa.UniqueConstraint('organization_id', 'metric_code', name='uq_customer_metric_registry_org_code'),
    )
    op.create_index(
        'ix_customer_metric_registry_organization_id',
        'customer_metric_registry',
        ['organization_id'],
    )


def downgrade() -> None:
    op.drop_index('ix_customer_metric_registry_organization_id', table_name='customer_metric_registry')
    op.drop_table('customer_metric_registry')
