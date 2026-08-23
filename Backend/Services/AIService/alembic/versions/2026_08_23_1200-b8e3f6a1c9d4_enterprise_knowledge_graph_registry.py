"""enterprise_knowledge_graph_registry

Revision ID: b8e3f6a1c9d4
Revises: a4d9e6c2f8b3
Create Date: 2026-08-23 12:00:00.000000

WP-14 BA-05 — Synchronize Enterprise Knowledge Graph (C-092 Knowledge
Graph Management). Extends AIService's existing Alembic chain (WP-14
BA-03's own `a4d9e6c2f8b3`) — does not bootstrap a second one. Introduces
the single canonical, LOCKED table `Master_Technical_Architecture.md`
AMD-012 (`enterprise_knowledge_graph_registry`, line 3170) and AMD-016
(the `organization_id` tenant-boundary amendment, line 3214) together
specify for this Business Activity — no column added, removed, or
retyped beyond that specification.

Per `WP-14_BA-04_Establish_Knowledge_Asset_Business_Activity_Charter.md`
"BA-05 — Implementation Authorization" and `RO-DEC-WP14-BA05-03`
(`TDS-013 §20`/`§26a`): hosting-service placement in `AIService` is
Repository-Owner-confirmed, not merely a recommendation.

Does not create `confidence_scoring_registry` — remains unimplemented
anywhere in this repository; `confidence_rule_id` is declared nullable,
no FK, mirroring the identical precedent `c3f8e1a9d2b6` already
established for `knowledge_asset_registry.confidence_rule_id`.

No `CREATE POLICY`/RLS is created here — consistent with every other
AMD-012 sibling table's own migration in this service (`ix_*_
organization_id` only). Tenant isolation for BA-05's own write path is
enforced at the application/service layer (`TDS-013 §22` layer 1,
`RelationshipResolutionService`).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b8e3f6a1c9d4'
down_revision: Union[str, Sequence[str], None] = 'a4d9e6c2f8b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'enterprise_knowledge_graph_registry',
        sa.Column('knowledge_graph_id', sa.Uuid(), nullable=False),
        sa.Column('source_entity_type', sa.String(255), nullable=True),
        sa.Column('source_entity_id', sa.Uuid(), nullable=True),
        sa.Column('relationship_type', sa.String(255), nullable=True),
        sa.Column('target_entity_type', sa.String(255), nullable=True),
        sa.Column('target_entity_id', sa.Uuid(), nullable=True),
        sa.Column('relationship_weight', sa.String(255), nullable=True),
        sa.Column('confidence_score', sa.Integer(), nullable=True),
        sa.Column('explainability_reference', sa.String(255), nullable=True),
        sa.Column('active_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('confidence_rule_id', sa.Uuid(), nullable=True),
        sa.Column('graph_engine_reference', sa.String(255), nullable=True),
        sa.Column('organization_id', sa.Uuid(), nullable=True),
        sa.PrimaryKeyConstraint('knowledge_graph_id'),
    )
    op.create_index(
        'ix_enterprise_knowledge_graph_registry_organization_id',
        'enterprise_knowledge_graph_registry',
        ['organization_id'],
    )


def downgrade() -> None:
    op.drop_index(
        'ix_enterprise_knowledge_graph_registry_organization_id',
        table_name='enterprise_knowledge_graph_registry',
    )
    op.drop_table('enterprise_knowledge_graph_registry')
