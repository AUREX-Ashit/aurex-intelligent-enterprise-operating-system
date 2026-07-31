"""identity_management

Revision ID: b1d6f4c8a3e7
Revises: 05f620c521e9
Create Date: 2026-08-11 09:00:00.000000

WP-08 BA-02 — Identity Management (C-001, PE-001-C001 v1.1).

Creates one audit/traceability table. Not a registered canonical
Business Object (IRA-008 §6): fails CMD-001 §26.3a's Cross-Experience
Reference Test and Governed Lifecycle test — produced and consumed
only within EX-C001-07's own realization, never retrieved by identity
as Required/Consumed Context by a separately-invoked later EX. Same
disposition as WP-07's own four audit-trail tables.

- identity_recovery_requests (BA-02, EX-C001-07, self-service scope)

No table for BA-01 (EX-C001-06, read-only re-confirmation, no
persistence) or BA-03 (EX-C001-08, classification-only, no
persistence, mirroring WP-02 BA-10's own precedent) — IRA-008 §5.

FKs to persons.id / identities.id — already exist as of this
migration's own down_revision.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b1d6f4c8a3e7'
down_revision: Union[str, Sequence[str], None] = '05f620c521e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'identity_recovery_requests',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('person_id', sa.Uuid(), nullable=False),
        sa.Column('requested_by_identity_id', sa.Uuid(), nullable=True),
        sa.Column('reason', sa.String(1000), nullable=False),
        sa.Column('routed_path', sa.String(20), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "routed_path IN ('NEW_IDENTITY', 'RE_RESOLUTION')",
            name='ck_identity_recovery_request_routed_path',
        ),
        sa.CheckConstraint(
            "status IN ('PENDING')",
            name='ck_identity_recovery_request_status',
        ),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['requested_by_identity_id'], ['identities.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_identity_recovery_requests_person_id', 'identity_recovery_requests', ['person_id'])


def downgrade() -> None:
    op.drop_index('ix_identity_recovery_requests_person_id', table_name='identity_recovery_requests')
    op.drop_table('identity_recovery_requests')
