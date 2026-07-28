"""membership_context_establishment

Revision ID: d4f8e2a6c1b9
Revises: c3e9a5f7b2d4
Create Date: 2026-07-31 09:00:00.000000

WP-03 BA-01 — Establish Membership Context (ERB-C007-01 / EX-C007-01 +
EX-C007-02 per PE-001-C007).

Creates `organization_nodes` — WP-03's own minimal, disclosed subset
of Master Technical Architecture's canonical `organization_node`
(ERG-001-02/03's EnterpriseNode). Only node_code/node_name/node_type/
active_flag are implemented; the ~20 further ESG/Enterprise-Structure
-specific columns (legal_entity_name, sector, materiality/risk scores,
etc.) belong to Enterprise Structure Management (C-005)'s own future
scope and are deferred, not silently omitted (TD-032). No row is
seeded here — MDP-001 explicitly excludes `organization_node` from
build-time seeding ("populate exclusively through real tenant
onboarding and real business operation"), and no Business Activity
anywhere yet owns creating one.

Extends `memberships` (WP-00-era table) with `home_node_id` (nullable
— canonically NOT NULL, but no Business Activity yet establishes an
OrganizationNode row to reference; TD-032), `membership_type`
(URA-001-106), `license_type` (URA-001-111), `effective_from`,
`effective_to` (SD-002-011-style, Establish-scoped only). `role_id`
and `membership_status` (both WP-00-era) are untouched.

Purely additive: no existing column is altered or dropped.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd4f8e2a6c1b9'
down_revision: Union[str, Sequence[str], None] = 'c3e9a5f7b2d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'organization_nodes',
        sa.Column('id',         sa.UUID(),                   nullable=False),
        sa.Column('node_code',  sa.String(100),               nullable=False),
        sa.Column('node_name',  sa.String(255),                nullable=False),
        sa.Column('node_type',  sa.String(255),                nullable=False),
        sa.Column('active_flag', sa.Boolean(),                 nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True),    nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),    nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_organization_nodes'),
        sa.UniqueConstraint('node_code', name='uq_organization_nodes_node_code'),
    )

    op.add_column('memberships', sa.Column('home_node_id', sa.UUID(), nullable=True))
    op.add_column('memberships', sa.Column('membership_type', sa.String(20), nullable=False, server_default='INTERNAL'))
    op.add_column('memberships', sa.Column('license_type', sa.String(20), nullable=False, server_default='FULL'))
    op.add_column('memberships', sa.Column('effective_from', sa.DateTime(timezone=True), nullable=True))
    op.add_column('memberships', sa.Column('effective_to', sa.DateTime(timezone=True), nullable=True))

    op.create_foreign_key(
        'fk_memberships_home_node_id',
        'memberships', 'organization_nodes',
        ['home_node_id'], ['id'],
    )
    op.create_check_constraint(
        'ck_memberships_membership_type',
        'memberships',
        "membership_type IN ('INTERNAL', 'EXTERNAL')",
    )
    op.create_check_constraint(
        'ck_memberships_license_type',
        'memberships',
        "license_type IN ('FULL', 'LIGHT')",
    )

    # Backfill effective_from for pre-existing rows (WP-00 seed data),
    # then close the column, mirroring WP-01's own two-step nullable ->
    # backfill -> NOT NULL pattern for additive columns on a table with
    # existing rows.
    op.execute("UPDATE memberships SET effective_from = joined_at WHERE effective_from IS NULL")
    op.alter_column('memberships', 'effective_from', nullable=False)


def downgrade() -> None:
    op.drop_constraint('ck_memberships_license_type', 'memberships', type_='check')
    op.drop_constraint('ck_memberships_membership_type', 'memberships', type_='check')
    op.drop_constraint('fk_memberships_home_node_id', 'memberships', type_='foreignkey')
    op.drop_column('memberships', 'effective_to')
    op.drop_column('memberships', 'effective_from')
    op.drop_column('memberships', 'license_type')
    op.drop_column('memberships', 'membership_type')
    op.drop_column('memberships', 'home_node_id')
    op.drop_table('organization_nodes')
