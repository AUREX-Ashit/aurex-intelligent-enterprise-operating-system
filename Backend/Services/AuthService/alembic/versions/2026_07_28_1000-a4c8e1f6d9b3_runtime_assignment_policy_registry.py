"""runtime_assignment_policy_registry

Revision ID: a4c8e1f6d9b3
Revises: f2a7c9e4b6d1
Create Date: 2026-07-28 10:00:00.000000

WP-02 BA-05 — Establish Runtime Assignment Policy (ERB-C003-01 /
EX-C003-05 per PE-001-C003). Realizes Master Technical Architecture's
canonical runtime_assignment_policy_registry (v7.1) — a governed,
reusable rule (assignment_target_type, configured lifecycle states,
optional escalation reference), explicitly distinct from a Runtime
Assignment instance (runtime_assignment_registry, unaffected in
AuthService — still not implemented here, since assignment instances are
an operational act EX-C003-05 itself places outside this capability).
Purely additive: no existing table is altered.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a4c8e1f6d9b3'
down_revision: Union[str, Sequence[str], None] = 'f2a7c9e4b6d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'runtime_assignment_policies',
        sa.Column('id',                          sa.UUID(),        nullable=False),
        sa.Column('organization_id',              sa.UUID(),        nullable=False),
        sa.Column('policy_name',                  sa.String(255),   nullable=False),
        sa.Column('assignment_target_type',       sa.String(50),    nullable=False),
        sa.Column('configured_lifecycle_states',  sa.JSON(),        nullable=False),
        sa.Column('escalation_policy_id',         sa.UUID(),        nullable=True),
        sa.Column('created_at',                   sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',                   sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name='fk_runtime_assignment_policies_organization_id'),
        sa.PrimaryKeyConstraint('id', name='pk_runtime_assignment_policies'),
        sa.CheckConstraint(
            "assignment_target_type IN ('NAMED_USER', 'BUSINESS_ROLE', 'GROUP', 'EXTERNAL_USER')",
            name='ck_runtime_assignment_policies_target_type',
        ),
    )
    op.create_index('ix_runtime_assignment_policies_organization_id', 'runtime_assignment_policies', ['organization_id'])


def downgrade() -> None:
    op.drop_index('ix_runtime_assignment_policies_organization_id', table_name='runtime_assignment_policies')
    op.drop_table('runtime_assignment_policies')
