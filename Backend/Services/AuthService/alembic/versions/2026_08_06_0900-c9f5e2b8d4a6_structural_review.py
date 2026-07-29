"""structural_review

Revision ID: c9f5e2b8d4a6
Revises: b8e4d1a7c3f9
Create Date: 2026-08-06 09:00:00.000000

WP-04 BA-06 — Review Proposed Structural Outcome / Resolve Structural
Review Concerns (ERB-C005-06 / EX-C005-08, -09 per PE-001-C005;
RVC-000001, ADR-011, IRA-004 §25).

Creates `structural_reviews` — a genuine new table (not an Extend),
since RVC-000001 is its own registered Aggregate Root (IRA-004 §25).
FK to `structural_proposals.id` (one specific revision) — already
exists as of this migration's own down_revision.

`status` is constrained to IRA-004 §25's own registered Lifecycle
Model. Only CREATED and CONCERNS_RESOLVED are reachable by this
Business Activity's own code (TD-062).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c9f5e2b8d4a6'
down_revision: Union[str, Sequence[str], None] = 'b8e4d1a7c3f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'structural_reviews',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('structural_proposal_id', sa.Uuid(), nullable=False),
        sa.Column('review_position', sa.Text(), nullable=False),
        sa.Column('concerns', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='CREATED'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('CREATED', 'CONCERNS_RESOLVED', 'INVALIDATED', 'ARCHIVED')",
            name='ck_structural_reviews_status',
        ),
        sa.ForeignKeyConstraint(['structural_proposal_id'], ['structural_proposals.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('structural_reviews')
