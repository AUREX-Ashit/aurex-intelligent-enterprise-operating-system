"""structural_change_intent

Revision ID: f7a2d9c4e6b1
Revises: e5c1a9f4b7d2
Create Date: 2026-08-03 09:00:00.000000

WP-04 BA-03 — Frame Structural Change Intent (ERB-C005-03 / EX-C005-04
per PE-001-C005; SCI-000001, ADR-006, IRA-004 §21).

Creates `structural_change_intents` — a genuine new table (not an
Extend of any existing object), since SCI-000001 is its own registered
Aggregate Root, not a sub-object of EnterpriseNode/EnterpriseRelationship
(IRA-004 §21). Carries no FK to `organization_nodes` and no
`organization_id` column — see models/structural_change_intent.py's
own docstring for the disclosed rationale (the structural-target
binding is BA-04's own future scope, per the `DERIVED_FROM` relationship
IRA-004 §21 records as Pending Canonical Binding).

`status` is constrained to IRA-004 §21's full registered Lifecycle
Model (CREATED, MODIFIED, SUPERSEDED, ABANDONED, WITHDRAWN, ARCHIVED),
though this Business Activity's own code only ever writes CREATED
(TD, see IMP-REPORT-WP-04) — the constraint reflects SCI-000001's
actual registered lifecycle, not an invented one.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f7a2d9c4e6b1'
down_revision: Union[str, Sequence[str], None] = 'e5c1a9f4b7d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'structural_change_intents',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('change_rationale', sa.Text(), nullable=False),
        sa.Column('target_outcome', sa.Text(), nullable=False),
        sa.Column('decision_boundary', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='CREATED'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('CREATED', 'MODIFIED', 'SUPERSEDED', 'ABANDONED', 'WITHDRAWN', 'ARCHIVED')",
            name='ck_structural_change_intents_status',
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('structural_change_intents')
