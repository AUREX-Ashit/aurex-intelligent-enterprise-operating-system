"""impact_assessment

Revision ID: b8e4d1a7c3f9
Revises: a3c6f8e1d5b2
Create Date: 2026-08-05 09:00:00.000000

WP-04 BA-05 — Assess Structural Consequence (ERB-C005-05 / EX-C005-07
per PE-001-C005; IMC-000001, ADR-009, IRA-004 §23).

Creates `impact_assessments` — a genuine new table (not an Extend),
since IMC-000001 is its own registered Aggregate Root (IRA-004 §23).
FK to `structural_proposals.id` (one specific revision, not a
proposal_id lineage) — already exists as of this migration's own
down_revision.

`status` is constrained to IRA-004 §23's own registered Lifecycle
Model. Only CREATED is reachable by this Business Activity's own code
(TD-057).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b8e4d1a7c3f9'
down_revision: Union[str, Sequence[str], None] = 'a3c6f8e1d5b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'impact_assessments',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('structural_proposal_id', sa.Uuid(), nullable=False),
        sa.Column('impact_description', sa.Text(), nullable=False),
        sa.Column('uncertainty_notes', sa.Text(), nullable=True),
        sa.Column('downstream_implications', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='CREATED'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('CREATED', 'INVALIDATED', 'ARCHIVED')",
            name='ck_impact_assessments_status',
        ),
        sa.ForeignKeyConstraint(['structural_proposal_id'], ['structural_proposals.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('impact_assessments')
