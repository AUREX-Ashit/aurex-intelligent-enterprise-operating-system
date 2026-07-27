"""domain_permission_registry

Revision ID: e7f2b4a9c3d5
Revises: c9e4a7f3b2d1
Create Date: 2026-07-27 14:00:00.000000

WP-02 BA-02 — Establish Domain Permission (ERB-C003-01 / EX-C003-02 per
PE-001-C003). Realizes URA-001-47 (standing Domain Permission grant),
mirroring Master Technical Architecture's canonical `domain_permission_registry`
(AMD-011, FK to Domain completed by AMD-014). Purely additive: no existing
table is altered.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e7f2b4a9c3d5'
down_revision: Union[str, Sequence[str], None] = 'c9e4a7f3b2d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'domain_permissions',
        sa.Column('id',              sa.UUID(),        nullable=False),
        sa.Column('membership_id',   sa.UUID(),        nullable=False),
        sa.Column('domain_id',       sa.UUID(),        nullable=False),
        sa.Column('permission_level', sa.String(50),   nullable=False),
        sa.Column('effective_from',  sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_to',    sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at',      sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',      sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['membership_id'], ['memberships.id'], name='fk_domain_permissions_membership_id', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['domain_id'], ['domains.id'], name='fk_domain_permissions_domain_id'),
        sa.PrimaryKeyConstraint('id', name='pk_domain_permissions'),
        sa.CheckConstraint(
            "permission_level IN ('VIEW', 'ENTER', 'EDIT', 'REVIEW', 'APPROVE', 'ASSIGN', 'DELEGATE', 'ADMIN')",
            name='ck_domain_permissions_permission_level',
        ),
    )
    op.create_index('ix_domain_permissions_membership_id', 'domain_permissions', ['membership_id'])
    op.create_index('ix_domain_permissions_domain_id', 'domain_permissions', ['domain_id'])


def downgrade() -> None:
    op.drop_index('ix_domain_permissions_domain_id', table_name='domain_permissions')
    op.drop_index('ix_domain_permissions_membership_id', table_name='domain_permissions')
    op.drop_table('domain_permissions')
