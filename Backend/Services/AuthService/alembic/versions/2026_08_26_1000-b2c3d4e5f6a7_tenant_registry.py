"""tenant_registry

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-08-26 10:00:00.000000

C-040 Tenant Administration — TDS-016 (tenant_registry / organization
Remediation, chartered minimum BA "Tenant Establishment only", Repository
Owner Decision 2026-08-26). Realizes ADR-034 Section 7 items 1 and 3:
1:1 cardinality enforcement (a UNIQUE constraint on the referencing side)
and the schema/domain-model reconciliation TDS-016 performs.

Creates tenant_registry (TDS-016 Section 5's own corrected column set —
lifecycle_state's four-state CHECK, version, effective_from/to, updated_at,
approved_by_actor_id/approved_at, allocated_by_actor_id/allocated_at,
created_at) and adds organizations.tenant_id (nullable FK to
tenant_registry.id, UNIQUE). Deliberately does NOT create every column
Master_Technical_Architecture.md's own tenant_registry draft lists
(deployment_model, azure_region, azure_subscription_id, database_schema,
storage_container_prefix, cache_key_prefix, encryption_key_reference,
data_residency_country, tier, contract_start_date, contract_end_date,
tenant_name) — each is a Technical Provisioning Authority concern
(ADR-026 Section 13), explicitly out of scope for this remediation
(TDS-016 Section 1) and for the chartered minimum BA.

Deliberately does NOT add a back-reference organization_id column on
tenant_registry (TDS-016 Section 5's own explicit, reasoned non-addition)
and does NOT add a NOT NULL constraint to organizations.tenant_id
(TDS-016 Section 7 — a genuine pre-Establishment window is architecturally
required by ADR-026's own phased process).

Purely additive: no existing column is renamed, retyped, or dropped;
middleware/tenant.py, dependencies.py, and routers/configuration.py are
untouched by this migration (TD-158's disposition preserved unchanged).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tenant_registry',
        sa.Column('id',                     sa.UUID(),        nullable=False),
        sa.Column('tenant_code',            sa.String(100),   nullable=False),
        sa.Column('lifecycle_state',        sa.String(20),    nullable=False),
        sa.Column('version',                sa.Integer(),     nullable=False, server_default='1'),
        sa.Column('effective_from',         sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_to',           sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at',             sa.DateTime(timezone=True), nullable=True),
        sa.Column('approved_by_actor_id',   sa.UUID(),        nullable=False),
        sa.Column('approved_at',            sa.DateTime(timezone=True), nullable=False),
        sa.Column('allocated_by_actor_id',  sa.UUID(),        nullable=False),
        sa.Column('allocated_at',           sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at',             sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_tenant_registry'),
        sa.UniqueConstraint('tenant_code', name='uq_tenant_registry_tenant_code'),
        sa.CheckConstraint(
            "lifecycle_state IN ('PROVISIONED', 'MIGRATING', 'OFFBOARDING', 'OFFBOARDED')",
            name='ck_tenant_registry_lifecycle_state',
        ),
    )
    op.create_index('ix_tenant_registry_tenant_code', 'tenant_registry', ['tenant_code'])

    op.add_column(
        'organizations',
        sa.Column('tenant_id', sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        'fk_organizations_tenant_id', 'organizations', 'tenant_registry',
        ['tenant_id'], ['id'],
    )
    op.create_unique_constraint('uq_organizations_tenant_id', 'organizations', ['tenant_id'])


def downgrade() -> None:
    op.drop_constraint('uq_organizations_tenant_id', 'organizations', type_='unique')
    op.drop_constraint('fk_organizations_tenant_id', 'organizations', type_='foreignkey')
    op.drop_column('organizations', 'tenant_id')
    op.drop_index('ix_tenant_registry_tenant_code', table_name='tenant_registry')
    op.drop_table('tenant_registry')
