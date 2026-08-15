"""knowledge_asset_registry

Revision ID: c3f8e1a9d2b6
Revises: b7f2a9c4e8d1
Create Date: 2026-08-10 14:00:00.000000

WP-14 BA-04 — Establish Knowledge Asset (C-091 Knowledge Management).
Extends AIService's existing Alembic chain (WP-12's `b7f2a9c4e8d1`) — does
not bootstrap a second one. Introduces the single canonical, LOCKED table
`Master_Technical_Architecture.md` AMD-012 specifies for this Business
Activity (`knowledge_asset_registry`, line 3226) — no column added,
removed, or retyped beyond that specification.

Per `WP-14_BA-04_Establish_Knowledge_Asset_Business_Activity_Charter.md`
§8 (corrected update): hosting-service placement in `AIService` is
evidenced by repository precedent (this table's own AMD-012 siblings,
`vector_index_registry`/`document_chunk_registry`, already live here using
the identical logical-FK `organization_id` pattern applied below) and is
not a prerequisite gated by the separate, still-open WP-14-wide hosting
determination (BA-05's own architectural matter).

Does not create `data_ingestion_registry` or `confidence_scoring_registry`
— both remain unimplemented anywhere in this repository (charter §15/§16);
`source_ingestion_id`/`confidence_rule_id` are declared nullable, no FK,
mirroring the identical precedent `d4a9c1e7f3b5` already established for
`evidence_registry.confidence_rule_id`.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c3f8e1a9d2b6'
down_revision: Union[str, Sequence[str], None] = 'b7f2a9c4e8d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'knowledge_asset_registry',
        sa.Column('knowledge_asset_id', sa.Uuid(), nullable=False),
        sa.Column('knowledge_asset_name', sa.String(255), nullable=True),
        sa.Column('knowledge_asset_type', sa.String(255), nullable=True),
        sa.Column('source_ingestion_id', sa.Uuid(), nullable=True),
        sa.Column('curation_status', sa.String(50), nullable=False, server_default='PROPOSED'),
        sa.Column('provenance_reference', sa.String(255), nullable=True),
        sa.Column('freshness_last_confirmed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('graph_engine_reference', sa.String(255), nullable=True),
        sa.Column('confidence_rule_id', sa.Uuid(), nullable=True),
        sa.Column('active_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.CheckConstraint(
            "curation_status IN ('PROPOSED', 'VALIDATED', 'ACCEPTED', 'REJECTED', 'SUPERSEDED')",
            name='ck_knowledge_asset_registry_curation_status',
        ),
        sa.PrimaryKeyConstraint('knowledge_asset_id'),
    )
    op.create_index(
        'ix_knowledge_asset_registry_organization_id', 'knowledge_asset_registry', ['organization_id']
    )


def downgrade() -> None:
    op.drop_index('ix_knowledge_asset_registry_organization_id', table_name='knowledge_asset_registry')
    op.drop_table('knowledge_asset_registry')
