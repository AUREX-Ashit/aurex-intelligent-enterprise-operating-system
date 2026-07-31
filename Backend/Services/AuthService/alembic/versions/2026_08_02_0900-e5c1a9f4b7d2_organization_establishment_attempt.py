"""organization_establishment_attempt

Revision ID: e5c1a9f4b7d2
Revises: a9f3d6e2c8b4
Create Date: 2026-08-02 09:00:00.000000

WP-01A / IRA-001A — Constitutional correction to BA-01 (Establish
Organization), realizing ERB-C004-01's own Organization Anchor Context
(PE-001-C004 §1.16) as a genuinely separate, non-authoritative
construct, plus the two previously-missing Business Activities BA-01B
(Verify Organization Domain Claim, ERB-C004-02) and BA-01C (Activate
Organization, first-time, ERB-C004-03).

Creates `organization_establishment_attempts` — additive only. Does
NOT alter `organizations` in any way (no column added, dropped, or
retyped) — BA-02 through BA-07 require no migration and no code
change, since none of them ever query this new table.

`activated_organization_id` is a nullable FK into `organizations.id`,
set only at first-time activation (BA-01C), for post-hoc lineage
traceability only (PE-001-C004 §1.17) — never consulted by any
existence/validity resolution path.

Purely additive: no existing table or column is altered or dropped.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e5c1a9f4b7d2'
down_revision: Union[str, Sequence[str], None] = 'a9f3d6e2c8b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'organization_establishment_attempts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_code', sa.String(50), nullable=False),
        sa.Column('organization_name', sa.String(255), nullable=False),
        sa.Column('organization_type', sa.String(50), nullable=False),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('primary_domain', sa.String(255), nullable=True),
        sa.Column('domain_verification_status', sa.String(20), nullable=False, server_default='NOT_CLAIMED'),
        sa.Column('no_domain_activation_reason', sa.Text(), nullable=True),
        sa.Column('activated_organization_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_organization_establishment_attempts'),
        sa.UniqueConstraint('organization_code', name='uq_organization_establishment_attempts_organization_code'),
    )

    op.create_foreign_key(
        'fk_org_establishment_attempts_activated_org_id',
        'organization_establishment_attempts', 'organizations',
        ['activated_organization_id'], ['id'],
    )
    op.create_check_constraint(
        'ck_org_establishment_attempts_domain_verification_status',
        'organization_establishment_attempts',
        "domain_verification_status IN ('NOT_CLAIMED', 'UNVERIFIED', 'VERIFIED')",
    )
    op.create_index(
        'ix_organization_establishment_attempts_organization_code',
        'organization_establishment_attempts', ['organization_code'],
    )


def downgrade() -> None:
    op.drop_index('ix_organization_establishment_attempts_organization_code', table_name='organization_establishment_attempts')
    op.drop_constraint('ck_org_establishment_attempts_domain_verification_status', 'organization_establishment_attempts', type_='check')
    op.drop_constraint('fk_org_establishment_attempts_activated_org_id', 'organization_establishment_attempts', type_='foreignkey')
    op.drop_table('organization_establishment_attempts')
