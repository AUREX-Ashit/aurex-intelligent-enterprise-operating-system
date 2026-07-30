"""access_evaluation_outcome

Revision ID: f3a7c5e9b2d8
Revises: e6c1b3a9d7f2
Create Date: 2026-08-09 09:00:00.000000

WP-05 BA-01 through BA-04 — Access Evaluation Outcome (AEO-000001,
ADR-015, IRA-005 §11/§12).

Creates `access_evaluation_outcomes` — the first Physical Implementation
Mapping for AEO-000001 (ADR-015's own §"Explicitly Not Decided" left
this Pending). FKs to `memberships.id`, `domains.id`, and
`approval_authorities.id` (nullable — populated only for DEFERRED
outcomes) — all already exist as of this migration's own down_revision.

`outcome_type` and `validity_status` are each constrained to ADR-015's
own full registered Lifecycle Model (four and five values respectively)
-- this Work Package's own code only ever writes UNRESOLVED/DEFERRED
for outcome_type (IRA-005 §12; PERMITTED/DENIED require a URA-001-76
resolver not yet authorized here) and CREATED/PRESERVED/INVALIDATED/
EXPIRED for validity_status (SUPERSEDED is never written, same class of
gap — see TD register).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f3a7c5e9b2d8'
down_revision: Union[str, Sequence[str], None] = 'e6c1b3a9d7f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'access_evaluation_outcomes',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('membership_id', sa.Uuid(), nullable=False),
        sa.Column('domain_id', sa.Uuid(), nullable=False),
        sa.Column('permission_level', sa.String(50), nullable=False),
        sa.Column('outcome_type', sa.String(20), nullable=False),
        sa.Column('validity_status', sa.String(20), nullable=False, server_default='CREATED'),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('approval_authority_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "outcome_type IN ('PERMITTED', 'DENIED', 'UNRESOLVED', 'DEFERRED')",
            name='ck_access_evaluation_outcomes_outcome_type',
        ),
        sa.CheckConstraint(
            "validity_status IN ('CREATED', 'PRESERVED', 'SUPERSEDED', 'INVALIDATED', 'EXPIRED')",
            name='ck_access_evaluation_outcomes_validity_status',
        ),
        sa.CheckConstraint(
            "permission_level IN ('VIEW', 'ENTER', 'EDIT', 'REVIEW', 'APPROVE', 'ASSIGN', 'DELEGATE', 'ADMIN')",
            name='ck_access_evaluation_outcomes_permission_level',
        ),
        sa.ForeignKeyConstraint(['membership_id'], ['memberships.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['domain_id'], ['domains.id']),
        sa.ForeignKeyConstraint(['approval_authority_id'], ['approval_authorities.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_access_evaluation_outcomes_membership_id', 'access_evaluation_outcomes', ['membership_id'])
    op.create_index('ix_access_evaluation_outcomes_domain_id', 'access_evaluation_outcomes', ['domain_id'])


def downgrade() -> None:
    op.drop_index('ix_access_evaluation_outcomes_domain_id', table_name='access_evaluation_outcomes')
    op.drop_index('ix_access_evaluation_outcomes_membership_id', table_name='access_evaluation_outcomes')
    op.drop_table('access_evaluation_outcomes')
