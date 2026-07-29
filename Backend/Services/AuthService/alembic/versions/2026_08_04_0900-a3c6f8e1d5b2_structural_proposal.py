"""structural_proposal

Revision ID: a3c6f8e1d5b2
Revises: f7a2d9c4e6b1
Create Date: 2026-08-04 09:00:00.000000

WP-04 BA-04 — Shape / Refine Proposed Structural Outcome (ERB-C005-04 /
EX-C005-05, -06 per PE-001-C005; POC-000001, ADR-008, IRA-004 §22).

Creates `structural_proposals` — a genuine new table (not an Extend),
since POC-000001 is its own registered Aggregate Root (IRA-004 §22).
Append-only revision model: `proposal_id` groups revisions of the same
logical proposal (equals `id` for revision 1); `revision_number`
distinguishes them within that lineage; no unique constraint spans
(proposal_id, revision_number) alone since concurrent-revision races
are not addressed by this Business Activity — disclosed as TD-056, not
silently omitted.

FKs to `structural_change_intents.id` (SCI-000001) and
`organization_nodes.id` (ADR-007's EnterpriseNode-only v1 scope) — both
already exist as of this migration's own down_revision.

`status` is constrained to IRA-004 §22's own registered Lifecycle
Model, minus REVISED (realized structurally via a new row, not a
status value — see models/structural_proposal.py). Only CREATED and
SUPERSEDED are reachable by this Business Activity's own code.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a3c6f8e1d5b2'
down_revision: Union[str, Sequence[str], None] = 'f7a2d9c4e6b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'structural_proposals',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('proposal_id', sa.Uuid(), nullable=False),
        sa.Column('revision_number', sa.Integer(), nullable=False),
        sa.Column('structural_change_intent_id', sa.Uuid(), nullable=False),
        sa.Column('target_organization_node_id', sa.Uuid(), nullable=False),
        sa.Column('proposed_outcome_description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='CREATED'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('CREATED', 'SUPERSEDED', 'VALIDATED', 'ARCHIVED')",
            name='ck_structural_proposals_status',
        ),
        sa.ForeignKeyConstraint(['structural_change_intent_id'], ['structural_change_intents.id']),
        sa.ForeignKeyConstraint(['target_organization_node_id'], ['organization_nodes.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_structural_proposals_proposal_id'), 'structural_proposals', ['proposal_id'], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_structural_proposals_proposal_id'), table_name='structural_proposals')
    op.drop_table('structural_proposals')
