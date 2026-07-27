"""approval_authority_registry

Revision ID: b8d3f6a1c4e2
Revises: e7f2b4a9c3d5
Create Date: 2026-07-27 16:00:00.000000

WP-02 BA-03 — Establish Approval Authority (ERB-C003-01 / EX-C003-03 per
PE-001-C003). Realizes Master Technical Architecture's canonical
approval_authority_registry (AMD-011), completed by this same work
package's own architecture-completion pass to add scope_type (GLOBAL/
COMPANY/DOMAIN/OBJECT, URA-001-61) as an explicit, stored discriminator,
domain_id (DOMAIN scope), and object_type/object_id (OBJECT scope,
mirroring runtime_assignment_registry's own anchor pattern). scope_type
is required (not inferred from anchor presence) because GLOBAL and
COMPANY share an identical anchor pattern once organization_id is
required for every scope — the two are indistinguishable without their
own stored discriminator. Purely additive: this migration creates one
new table only; no existing table is altered.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b8d3f6a1c4e2'
down_revision: Union[str, Sequence[str], None] = 'e7f2b4a9c3d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'approval_authorities',
        sa.Column('id',                     sa.UUID(),        nullable=False),
        sa.Column('organization_id',        sa.UUID(),        nullable=False),
        sa.Column('authority_name',         sa.String(255),   nullable=False),
        sa.Column('approval_strategy',      sa.String(50),    nullable=False),
        sa.Column('majority_threshold_pct', sa.Integer(),     nullable=True),
        sa.Column('scope_type',             sa.String(50),    nullable=False),
        sa.Column('domain_id',              sa.UUID(),        nullable=True),
        sa.Column('object_type',            sa.String(100),   nullable=True),
        sa.Column('object_id',              sa.UUID(),        nullable=True),
        sa.Column('created_at',             sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',             sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name='fk_approval_authorities_organization_id'),
        sa.ForeignKeyConstraint(['domain_id'], ['domains.id'], name='fk_approval_authorities_domain_id'),
        sa.PrimaryKeyConstraint('id', name='pk_approval_authorities'),
        sa.CheckConstraint(
            "approval_strategy IN ('ANY_ONE', 'ALL', 'MAJORITY', 'SEQUENTIAL')",
            name='ck_approval_authorities_approval_strategy',
        ),
        sa.CheckConstraint(
            "scope_type IN ('GLOBAL', 'COMPANY', 'DOMAIN', 'OBJECT')",
            name='ck_approval_authorities_scope_type',
        ),
        sa.CheckConstraint(
            "(scope_type IN ('GLOBAL', 'COMPANY') AND domain_id IS NULL AND object_type IS NULL AND object_id IS NULL) OR "
            "(scope_type = 'DOMAIN' AND domain_id IS NOT NULL AND object_type IS NULL AND object_id IS NULL) OR "
            "(scope_type = 'OBJECT' AND domain_id IS NULL AND object_type IS NOT NULL AND object_id IS NOT NULL)",
            name='ck_approval_authorities_scope_consistency',
        ),
    )
    op.create_index('ix_approval_authorities_organization_id', 'approval_authorities', ['organization_id'])
    op.create_index('ix_approval_authorities_domain_id', 'approval_authorities', ['domain_id'])


def downgrade() -> None:
    op.drop_index('ix_approval_authorities_domain_id', table_name='approval_authorities')
    op.drop_index('ix_approval_authorities_organization_id', table_name='approval_authorities')
    op.drop_table('approval_authorities')
