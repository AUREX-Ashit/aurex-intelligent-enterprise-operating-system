"""delegation_policy_registry

Revision ID: f2a7c9e4b6d1
Revises: b8d3f6a1c4e2
Create Date: 2026-07-27 18:00:00.000000

WP-02 BA-04 — Establish Delegation Policy (ERB-C003-01 / EX-C003-04 per
PE-001-C003). Realizes Master Technical Architecture's canonical
delegation_policy_registry (v7.0) — a governed, reusable rule
(delegation_type, scope, sub-delegation permission), explicitly distinct
from a delegation instance (delegation_registry, unaffected — still not
implemented in AuthService, since delegation instances are an
operational act EX-C003-04 itself places outside this capability).
Purely additive: no existing table is altered.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f2a7c9e4b6d1'
down_revision: Union[str, Sequence[str], None] = 'b8d3f6a1c4e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'delegation_policies',
        sa.Column('id',                     sa.UUID(),        nullable=False),
        sa.Column('organization_id',        sa.UUID(),        nullable=False),
        sa.Column('policy_name',            sa.String(255),   nullable=False),
        sa.Column('delegation_type',        sa.String(100),   nullable=False),
        sa.Column('scope_type',             sa.String(50),    nullable=False),
        sa.Column('domain_id',              sa.UUID(),        nullable=True),
        sa.Column('object_type',            sa.String(100),   nullable=True),
        sa.Column('object_id',              sa.UUID(),        nullable=True),
        sa.Column('event_code',             sa.String(100),   nullable=True),
        sa.Column('sub_delegation_allowed', sa.Boolean(),     nullable=False, server_default=sa.text('false')),
        sa.Column('created_at',             sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',             sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name='fk_delegation_policies_organization_id'),
        sa.ForeignKeyConstraint(['domain_id'], ['domains.id'], name='fk_delegation_policies_domain_id'),
        sa.PrimaryKeyConstraint('id', name='pk_delegation_policies'),
        sa.CheckConstraint(
            "scope_type IN ('ORGANIZATION', 'DOMAIN', 'OBJECT', 'EVENT')",
            name='ck_delegation_policies_scope_type',
        ),
        sa.CheckConstraint(
            "(scope_type = 'ORGANIZATION' AND domain_id IS NULL AND object_type IS NULL AND object_id IS NULL AND event_code IS NULL) OR "
            "(scope_type = 'DOMAIN' AND domain_id IS NOT NULL AND object_type IS NULL AND object_id IS NULL AND event_code IS NULL) OR "
            "(scope_type = 'OBJECT' AND domain_id IS NULL AND object_type IS NOT NULL AND object_id IS NOT NULL AND event_code IS NULL) OR "
            "(scope_type = 'EVENT' AND domain_id IS NULL AND object_type IS NULL AND object_id IS NULL AND event_code IS NOT NULL)",
            name='ck_delegation_policies_scope_consistency',
        ),
    )
    op.create_index('ix_delegation_policies_organization_id', 'delegation_policies', ['organization_id'])
    op.create_index('ix_delegation_policies_domain_id', 'delegation_policies', ['domain_id'])


def downgrade() -> None:
    op.drop_index('ix_delegation_policies_domain_id', table_name='delegation_policies')
    op.drop_index('ix_delegation_policies_organization_id', table_name='delegation_policies')
    op.drop_table('delegation_policies')
