"""person_management

Revision ID: 05f620c521e9
Revises: f3a7c5e9b2d8
Create Date: 2026-08-10 09:00:00.000000

WP-07 BA-04/06/07/08 — Person Management (C-006, PE-001-C006 v1.1).

Creates four audit/traceability tables. None is a registered canonical
Business Object (IRA-007 §5/§9): each fails CMD-001 §26.3a's
Cross-Experience Reference Test and Governed Lifecycle test — produced
and consumed only within its own realizing EX, never retrieved by
identity as Required/Consumed Context by a separately-invoked later EX.
Same disposition as WP-04's own Comparison Context / Downstream
Continuation Context (neither registered).

- person_distinction_decisions (BA-04, EX-C006-04)
- person_reconciliation_decisions (BA-06, EX-C006-06)
- person_corrections (BA-07, EX-C006-07)
- person_enrichments (BA-08, EX-C006-08)

No table for BA-09/10 hand-offs (IRA-007 §5): the outcome is recorded
via record_audit() only, mirroring WP-02 BA-10's own precedent.

FKs to persons.id — already exists as of this migration's own
down_revision.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '05f620c521e9'
down_revision: Union[str, Sequence[str], None] = 'f3a7c5e9b2d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'person_distinction_decisions',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('candidate_person_ids', sa.JSON(), nullable=False),
        sa.Column('decision_type', sa.String(20), nullable=False),
        sa.Column('selected_person_id', sa.Uuid(), nullable=True),
        sa.Column('rationale', sa.Text(), nullable=False),
        sa.Column('decided_by', sa.String(255), nullable=True),
        sa.Column('decided_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "decision_type IN ('SELECTED_EXISTING', 'NEW_PERSON')",
            name='ck_person_distinction_decisions_decision_type',
        ),
        sa.ForeignKeyConstraint(['selected_person_id'], ['persons.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'person_reconciliation_decisions',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('person_id_a', sa.Uuid(), nullable=False),
        sa.Column('person_id_b', sa.Uuid(), nullable=False),
        sa.Column('decision', sa.String(30), nullable=False),
        sa.Column('rationale', sa.Text(), nullable=False),
        sa.Column('reviewed_by', sa.String(255), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "decision IN ('CONFIRMED_DUPLICATE', 'CONFIRMED_DISTINCT', 'ESCALATED')",
            name='ck_person_reconciliation_decisions_decision',
        ),
        sa.ForeignKeyConstraint(['person_id_a'], ['persons.id']),
        sa.ForeignKeyConstraint(['person_id_b'], ['persons.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_person_reconciliation_decisions_person_id_a', 'person_reconciliation_decisions', ['person_id_a'])
    op.create_index('ix_person_reconciliation_decisions_person_id_b', 'person_reconciliation_decisions', ['person_id_b'])

    op.create_table(
        'person_corrections',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('person_id', sa.Uuid(), nullable=False),
        sa.Column('field_name', sa.String(50), nullable=False),
        sa.Column('prior_value', sa.Text(), nullable=False),
        sa.Column('corrected_value', sa.Text(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('approval_reference', sa.String(255), nullable=True),
        sa.Column('corrected_by', sa.String(255), nullable=True),
        sa.Column('corrected_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "field_name IN ('first_name', 'last_name', 'display_name')",
            name='ck_person_corrections_field_name',
        ),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_person_corrections_person_id', 'person_corrections', ['person_id'])

    op.create_table(
        'person_enrichments',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('person_id', sa.Uuid(), nullable=False),
        sa.Column('attribute_name', sa.String(255), nullable=False),
        sa.Column('attribute_value', sa.Text(), nullable=False),
        sa.Column('source', sa.String(255), nullable=False),
        sa.Column('sensitivity_classification', sa.String(20), nullable=False),
        sa.Column('accepted_by', sa.String(255), nullable=True),
        sa.Column('accepted_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "sensitivity_classification IN ('PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED')",
            name='ck_person_enrichments_sensitivity_classification',
        ),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_person_enrichments_person_id', 'person_enrichments', ['person_id'])


def downgrade() -> None:
    op.drop_index('ix_person_enrichments_person_id', table_name='person_enrichments')
    op.drop_table('person_enrichments')

    op.drop_index('ix_person_corrections_person_id', table_name='person_corrections')
    op.drop_table('person_corrections')

    op.drop_index('ix_person_reconciliation_decisions_person_id_b', table_name='person_reconciliation_decisions')
    op.drop_index('ix_person_reconciliation_decisions_person_id_a', table_name='person_reconciliation_decisions')
    op.drop_table('person_reconciliation_decisions')

    op.drop_table('person_distinction_decisions')
