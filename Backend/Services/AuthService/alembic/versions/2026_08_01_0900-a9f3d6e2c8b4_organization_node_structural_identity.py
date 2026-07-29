"""organization_node_structural_identity

Revision ID: a9f3d6e2c8b4
Revises: d4f8e2a6c1b9
Create Date: 2026-08-01 09:00:00.000000

WP-04 BA-01 — Establish Organization Node (ERB-C005-01 / EX-C005-01 +
EX-C005-02 per PE-001-C005; ERG-001-02/03; IRA-004 §9/§11).

Extends `organization_nodes` (WP-03 BA-01's own minimal subset) with the
Structural Identity columns Master Technical Architecture's canonical
`organization_node` DDL specifies: `legal_entity_name`, `business_unit`,
`sector`, `operational_status`, `effective_from`, `effective_to`.

Deliberately deferred, not silently omitted (TD-043): `geography_id`
(no `geography_registry` table exists anywhere in this repository to
reference), `parent_available_flag` (naturally derived once
`organization_hierarchy` exists — WP-04 BA-08's own future scope), and
the materiality/risk/scenario/passport scores (`strategic_importance_
score`, `risk_criticality_score`, `reporting_currency`, `benchmark_
group`, `scenario_sensitive_flag`, `external_dependency_flag`,
`entity_materiality_score`, `data_readiness_score`, `external_data_
retrieval_flag`, `passport_shareable_flag`) — these belong to a
different, independently-governed bounded context per ERG-001-02, not
to C-005's own Structural Identity slice.

`effective_from`/`effective_to` are added as `DateTime(timezone=True)`,
not the canonical DDL's literal `VARCHAR(255)` — mirroring
`memberships.effective_from`/`effective_to`'s own established shape
(WP-03 BA-01) rather than reproducing an inconsistent column type
(TD-044 records this disclosed departure).

Purely additive: no existing column is altered or dropped.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a9f3d6e2c8b4'
down_revision: Union[str, Sequence[str], None] = 'd4f8e2a6c1b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('organization_nodes', sa.Column('legal_entity_name', sa.String(255), nullable=True))
    op.add_column('organization_nodes', sa.Column('business_unit', sa.String(255), nullable=True))
    op.add_column('organization_nodes', sa.Column('sector', sa.String(255), nullable=True))
    op.add_column('organization_nodes', sa.Column('operational_status', sa.String(50), nullable=True))
    op.add_column('organization_nodes', sa.Column('effective_from', sa.DateTime(timezone=True), nullable=True))
    op.add_column('organization_nodes', sa.Column('effective_to', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('organization_nodes', 'effective_to')
    op.drop_column('organization_nodes', 'effective_from')
    op.drop_column('organization_nodes', 'operational_status')
    op.drop_column('organization_nodes', 'sector')
    op.drop_column('organization_nodes', 'business_unit')
    op.drop_column('organization_nodes', 'legal_entity_name')
