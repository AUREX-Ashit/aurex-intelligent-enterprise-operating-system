"""domain_reference_registry

Revision ID: c9e4a7f3b2d1
Revises: d2d840d224b6
Create Date: 2026-07-27 12:00:00.000000

AMD-014 — Domain Business Object Architecture Completion. Adds `domains`,
a platform-seeded, tenant-extensible (URA-001-43), hierarchical
(URA-001-44) reference/master-data table describing the Domain only
(Finance, HR, Risk, Supply Chain, Cyber Security, Legal, Business
Resilience, or a tenant-added equivalent). No lifecycle state machine
and no Domain Owner/Domain Admin relationship is added here (URA-001-45/
-46 remain open, not silently resolved — see AMD-014 §4/§6). Purely
additive: no existing table is altered.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c9e4a7f3b2d1'
down_revision: Union[str, Sequence[str], None] = 'd2d840d224b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'domains',
        sa.Column('id',               sa.UUID(),        nullable=False),
        sa.Column('organization_id',  sa.UUID(),        nullable=True),
        sa.Column('domain_name',      sa.String(255),   nullable=False),
        sa.Column('parent_domain_id', sa.UUID(),        nullable=True),
        sa.Column('active_flag',      sa.Boolean(),     nullable=False, server_default=sa.text('true')),
        sa.Column('created_at',       sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name='fk_domains_organization_id'),
        sa.ForeignKeyConstraint(['parent_domain_id'], ['domains.id'], name='fk_domains_parent_domain_id'),
        sa.PrimaryKeyConstraint('id', name='pk_domains'),
    )
    # Supports OrganizationRepository.list_visible()'s NULL-or-tenant lookup.
    op.create_index('ix_domains_organization_id', 'domains', ['organization_id'])


def downgrade() -> None:
    op.drop_index('ix_domains_organization_id', table_name='domains')
    op.drop_table('domains')
