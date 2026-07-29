"""structural_validation

Revision ID: d2a8f4c6b9e3
Revises: c9f5e2b8d4a6
Create Date: 2026-08-07 09:00:00.000000

WP-04 BA-07 — Validate Transition Readiness (ERB-C005-07 / EX-C005-10
per PE-001-C005; VLC-000001, ADR-012, IRA-004 §26).

Creates `structural_validations` — a genuine new table (not an
Extend), since VLC-000001 is its own registered Aggregate Root
(IRA-004 §26). FKs to `structural_proposals.id` and
`structural_reviews.id` — both already exist as of this migration's
own down_revision.

No `readiness_result` column: BR-C005-007 is hard-enforced at the
service layer before a row is ever created, so every row represents a
"ready" validation by construction (see
models/structural_validation.py's own docstring).

`status` is constrained to IRA-004 §26's own registered Lifecycle
Model. Only CREATED is reachable by this Business Activity's own code
(TD-065).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd2a8f4c6b9e3'
down_revision: Union[str, Sequence[str], None] = 'c9f5e2b8d4a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'structural_validations',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('structural_proposal_id', sa.Uuid(), nullable=False),
        sa.Column('structural_review_id', sa.Uuid(), nullable=False),
        sa.Column('readiness_notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='CREATED'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('CREATED', 'INVALIDATED', 'ARCHIVED')",
            name='ck_structural_validations_status',
        ),
        sa.ForeignKeyConstraint(['structural_proposal_id'], ['structural_proposals.id']),
        sa.ForeignKeyConstraint(['structural_review_id'], ['structural_reviews.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('structural_validations')
