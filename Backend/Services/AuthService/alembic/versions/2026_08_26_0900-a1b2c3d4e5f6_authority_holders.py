"""authority_holders

Revision ID: a1b2c3d4e5f6
Revises: c7e2b5a9f1d4
Create Date: 2026-08-26 09:00:00.000000

C-040 Tenant Administration — TDS-017 §23 (Authority Runtime Enforcement).
Realizes the Organization-independent authority-holder persistence
mechanism for the constitutionally established AI-001/AI-002 authorities
(ADR-029 §10/§11, ADR-030-035, AI-001/AI-002/AI-003). Deliberately carries
no organization_id column of any kind, unlike approval_authorities/
runtime_assignment_policies, both of which are organization_id NOT NULL
and structurally incompatible with a platform-wide, pre-Organization
authority (ADR-031 §8, TDS-017 §5). Purely additive: this migration
creates one new table only; no existing table (including
approval_authorities and runtime_assignment_policies) is altered.

An active-holder uniqueness constraint (at most one ACTIVE row per
authority_identity) is enforced via a partial unique index rather than a
table-level UNIQUE constraint, since multiple SUPERSEDED historical rows
for the same authority_identity must remain valid (TDS-017 §23's own
versioning requirement, mirroring approval_authorities's own
version/status/supersedes_id pattern).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'c7e2b5a9f1d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'authority_holders',
        sa.Column('id',                          sa.UUID(),        nullable=False),
        sa.Column('authority_identity',           sa.String(20),    nullable=False),
        sa.Column('holder_person_id',              sa.UUID(),        nullable=False),
        sa.Column('appointment_instrument_ref',    sa.String(255),   nullable=False),
        sa.Column('version',                       sa.Integer(),     nullable=False, server_default='1'),
        sa.Column('status',                        sa.String(20),    nullable=False, server_default='ACTIVE'),
        sa.Column('effective_from',                sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_to',                  sa.DateTime(timezone=True), nullable=True),
        sa.Column('supersedes_id',                 sa.UUID(),        nullable=True),
        sa.Column('created_at',                    sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['holder_person_id'], ['persons.id'], name='fk_authority_holders_holder_person_id'),
        sa.ForeignKeyConstraint(['supersedes_id'], ['authority_holders.id'], name='fk_authority_holders_supersedes_id'),
        sa.PrimaryKeyConstraint('id', name='pk_authority_holders'),
        sa.CheckConstraint(
            "authority_identity IN ('AI-001', 'AI-002')",
            name='ck_authority_holders_authority_identity',
        ),
        sa.CheckConstraint(
            "status IN ('ACTIVE', 'SUPERSEDED')",
            name='ck_authority_holders_status',
        ),
    )
    op.create_index('ix_authority_holders_authority_identity', 'authority_holders', ['authority_identity'])
    op.create_index('ix_authority_holders_holder_person_id', 'authority_holders', ['holder_person_id'])
    op.create_index(
        'ux_authority_holders_active_authority',
        'authority_holders',
        ['authority_identity'],
        unique=True,
        sqlite_where=sa.text("status = 'ACTIVE'"),
        postgresql_where=sa.text("status = 'ACTIVE'"),
    )


def downgrade() -> None:
    op.drop_index('ux_authority_holders_active_authority', table_name='authority_holders')
    op.drop_index('ix_authority_holders_holder_person_id', table_name='authority_holders')
    op.drop_index('ix_authority_holders_authority_identity', table_name='authority_holders')
    op.drop_table('authority_holders')
