"""unclassified_intelligence_registry

Revision ID: f3b8d5a2c7e1
Revises: e7a2c4f9b6d3
Create Date: 2026-08-15 15:00:00.000000

WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090 Enterprise
Discovery). Extends AIService's existing Alembic chain (WP-14 BA-01's own
`e7a2c4f9b6d3`) — does not bootstrap a second one. Introduces the single
canonical, LOCKED table `Master_Technical_Architecture.md` AMD-005
specifies for this Business Activity (`unclassified_intelligence_registry`,
line 5453) — no column added, removed, or retyped beyond that
specification.

Does not create `user_registry`, `metric_registry`, or
`customer_metric_registry` — none has a physical Backend model anywhere in
this repository (same disposition already established for BA-01's/BA-04's
own optional FKs); `resolved_by_user_id`/`resolved_metric_id`/
`resolved_customer_metric_id` are declared nullable, no FK.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f3b8d5a2c7e1'
down_revision: Union[str, Sequence[str], None] = 'e7a2c4f9b6d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'unclassified_intelligence_registry',
        sa.Column('unclassified_id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('raw_extracted_value', sa.Text(), nullable=False),
        sa.Column('source_document_reference', sa.Text(), nullable=False),
        sa.Column('source_page_section', sa.String(500), nullable=True),
        sa.Column('extraction_method', sa.String(100), nullable=False),
        sa.Column('llm_label_suggestion', sa.String(255), nullable=True),
        sa.Column('llm_confidence_score', sa.Numeric(4, 3), nullable=True),
        sa.Column('probable_domain', sa.String(100), nullable=True),
        sa.Column('probable_bq_id', sa.String(50), nullable=True),
        sa.Column('resolution_status', sa.String(30), nullable=False, server_default='PENDING'),
        sa.Column('resolved_by_user_id', sa.Uuid(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('resolved_metric_id', sa.Uuid(), nullable=True),
        sa.Column('resolved_customer_metric_id', sa.Uuid(), nullable=True),
        sa.Column('convergence_signal_raised_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('active_flag', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "extraction_method IN ("
            "'OCR', 'NLP_PARSE', 'TABLE_EXTRACT', 'ENTITY_EXTRACT', "
            "'SEMANTIC_PARSE', 'MANUAL_ENTRY', 'API_INGEST'"
            ")",
            name='ck_unclassified_intelligence_registry_extraction_method',
        ),
        sa.CheckConstraint(
            "resolution_status IN ("
            "'PENDING', 'MAPPED_TO_EXISTING', 'NEW_CDE_CREATED', "
            "'DISCARDED', 'PROMOTED_CONVERGENCE'"
            ")",
            name='ck_unclassified_intelligence_registry_resolution_status',
        ),
        sa.PrimaryKeyConstraint('unclassified_id'),
    )
    op.create_index(
        'ix_unclassified_intelligence_registry_organization_id',
        'unclassified_intelligence_registry',
        ['organization_id'],
    )


def downgrade() -> None:
    op.drop_index(
        'ix_unclassified_intelligence_registry_organization_id',
        table_name='unclassified_intelligence_registry',
    )
    op.drop_table('unclassified_intelligence_registry')
