"""c023_license_context + c023_entitlement_context

Revision ID: c3d4e5f6a7b8
Revises: f9a3c7e1b5d2
Create Date: 2026-09-01 09:00:00.000000

C-023 Licensing & Entitlement — WP-17 BA-01 ("Establish Entitlement/License
Context (Administrative)"). Creates the two C-023-owned governance-layer
tables approved by the Repository Owner at
`TDS-C023-A §19.1` (D-1 Option A — two tables; D-2 hard intra-service FKs;
D-3 nullable `c023_license_type`; D-4 COALESCE-sentinel uniqueness; D-5
full canonical `status` set; D-6 `c023_`-prefixed names). The exact column
set, constraints, and indexes are `TDS-C023-A §3.1` / `§3.2` — nothing
added beyond what that approved design specifies.

CLAUDE.md §18 / §19.4 confirmation at the point of creation
(`IMP-REPORT-WP-17 §4(1)`, D-7(a)): this migration is PURELY ADDITIVE —
two `op.create_table(...)` calls plus their indexes. NO `ALTER` to any
existing table. `memberships`, `organizations`, `domains`,
`approval_authorities`, `membership_approval_authority` are only referenced
by foreign key, never modified — Decision 6 (`IRA-C023 §18.13`) is complied
with by construction (no `FULL`/`LIGHT` column, no FK to
`memberships.license_type`). `down_revision` is the current single
non-branching head `f9a3c7e1b5d2` (WP-18); this migration becomes the new
single head, no branch. No new architectural question arises — the schema
shape was decided by the Repository Owner, recorded verbatim, and
independently reviewed for fidelity before this migration was written.

D-4 cross-dialect note (the Repository Owner's condition on that approval):
the Entitlement-side current-context uniqueness index uses the expression

    COALESCE(domain_id, '00000000-0000-0000-0000-000000000000')

identically on both dialects.
  * PostgreSQL: `domain_id` is `uuid`; the all-zeros string literal is
    implicitly cast to `uuid` inside COALESCE (its sibling argument is
    `uuid`), so the expression needs no explicit `::uuid` cast and is
    dialect-neutral. The partial predicate `effective_to IS NULL` is
    applied via `postgresql_where`.
  * SQLite (test harness, `conftest.py`): `domain_id` round-trips as a
    hex string; COALESCE returns either that value or the 36-character
    dashed sentinel — always distinct, so two concurrent organization-wide
    (`domain_id IS NULL`) entitlements of the same type collide on the
    index exactly as intended. The partial predicate is applied via
    `sqlite_where`. This mirrors `ux_membership_approval_authority_active`
    (WP-18) and `ux_authority_holders_active_authority` (TDS-017), which
    already carry both `*_where` clauses so `Base.metadata.create_all`
    builds them under SQLite.

Row-Level Security: not added here. No AuthService migration adds RLS
policies — the repository-wide `SET app.organization_id` GUC plumbing that
such a policy would depend on does not exist yet, so a policy referencing
`current_setting('app.organization_id')` would deny every production read.
Tenant isolation is enforced at the service layer
(`EntitlementLicenseEstablishmentService`), exactly as every prior
AuthService Work Package does and as `TDS-C023-A §15` records WP-16 / WP-18
were certified under (TD-096 / TD-159 / TD-160, the known repository-wide
harness limitation — no new debt introduced).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'f9a3c7e1b5d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_ENTITLEMENT_CURRENT_UNIQUE_EXPR = (
    "COALESCE(domain_id, '00000000-0000-0000-0000-000000000000')"
)


def upgrade() -> None:
    op.create_table(
        'c023_license_context',
        sa.Column('id',                           sa.UUID(),                  nullable=False),
        sa.Column('membership_id',                sa.UUID(),                  nullable=False),
        sa.Column('status',                       sa.String(20),              nullable=False),
        sa.Column('effective_from',               sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_to',                 sa.DateTime(timezone=True), nullable=True),
        sa.Column('entitlement_source_reference', sa.String(255),             nullable=True),
        sa.Column('approval_authority_id',        sa.UUID(),                  nullable=False),
        sa.Column('committed_by_actor_id',        sa.UUID(),                  nullable=False),
        sa.Column('committed_at',                 sa.DateTime(timezone=True), nullable=False),
        sa.Column('c023_license_type',            sa.String(50),              nullable=True),
        sa.Column('created_at',                   sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',                   sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['membership_id'], ['memberships.id'], name='fk_c023_license_context_membership_id'),
        sa.ForeignKeyConstraint(['approval_authority_id'], ['approval_authorities.id'], name='fk_c023_license_context_approval_authority_id'),
        sa.PrimaryKeyConstraint('id', name='pk_c023_license_context'),
        sa.CheckConstraint(
            "status IN ('ACTIVE', 'SUSPENDED', 'REVOKED')",
            name='ck_c023_license_context_status',
        ),
        sa.CheckConstraint(
            "c023_license_type IS NULL OR "
            "c023_license_type IN ('SUPPLIER', 'AUDITOR', 'BOARD_MEMBER', 'CONSULTANT')",
            name='ck_c023_license_context_license_type',
        ),
    )
    op.create_index(
        'ix_c023_license_context_membership_id',
        'c023_license_context', ['membership_id'],
    )
    op.create_index(
        'ix_c023_license_context_approval_authority_id',
        'c023_license_context', ['approval_authority_id'],
    )
    op.create_index(
        'ux_c023_license_context_current',
        'c023_license_context', ['membership_id'],
        unique=True,
        postgresql_where=sa.text('effective_to IS NULL'),
        sqlite_where=sa.text('effective_to IS NULL'),
    )

    op.create_table(
        'c023_entitlement_context',
        sa.Column('id',                           sa.UUID(),                  nullable=False),
        sa.Column('organization_id',              sa.UUID(),                  nullable=False),
        sa.Column('domain_id',                    sa.UUID(),                  nullable=True),
        sa.Column('entitlement_type_ref',         sa.String(100),             nullable=False),
        sa.Column('status',                       sa.String(20),              nullable=False),
        sa.Column('effective_from',               sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_to',                 sa.DateTime(timezone=True), nullable=True),
        sa.Column('entitlement_source_reference', sa.String(255),             nullable=True),
        sa.Column('approval_authority_id',        sa.UUID(),                  nullable=False),
        sa.Column('committed_by_actor_id',        sa.UUID(),                  nullable=False),
        sa.Column('committed_at',                 sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at',                   sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',                   sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name='fk_c023_entitlement_context_organization_id'),
        sa.ForeignKeyConstraint(['domain_id'], ['domains.id'], name='fk_c023_entitlement_context_domain_id'),
        sa.ForeignKeyConstraint(['approval_authority_id'], ['approval_authorities.id'], name='fk_c023_entitlement_context_approval_authority_id'),
        sa.PrimaryKeyConstraint('id', name='pk_c023_entitlement_context'),
        sa.CheckConstraint(
            "status IN ('ACTIVE', 'SUSPENDED', 'REVOKED')",
            name='ck_c023_entitlement_context_status',
        ),
    )
    op.create_index(
        'ix_c023_entitlement_context_organization_id',
        'c023_entitlement_context', ['organization_id'],
    )
    op.create_index(
        'ix_c023_entitlement_context_approval_authority_id',
        'c023_entitlement_context', ['approval_authority_id'],
    )
    op.create_index(
        'ix_c023_entitlement_context_org_type',
        'c023_entitlement_context', ['organization_id', 'entitlement_type_ref'],
    )
    op.create_index(
        'ux_c023_entitlement_context_current',
        'c023_entitlement_context',
        ['organization_id', sa.text(_ENTITLEMENT_CURRENT_UNIQUE_EXPR), 'entitlement_type_ref'],
        unique=True,
        postgresql_where=sa.text('effective_to IS NULL'),
        sqlite_where=sa.text('effective_to IS NULL'),
    )


def downgrade() -> None:
    op.drop_index('ux_c023_entitlement_context_current', table_name='c023_entitlement_context')
    op.drop_index('ix_c023_entitlement_context_org_type', table_name='c023_entitlement_context')
    op.drop_index('ix_c023_entitlement_context_approval_authority_id', table_name='c023_entitlement_context')
    op.drop_index('ix_c023_entitlement_context_organization_id', table_name='c023_entitlement_context')
    op.drop_table('c023_entitlement_context')

    op.drop_index('ux_c023_license_context_current', table_name='c023_license_context')
    op.drop_index('ix_c023_license_context_approval_authority_id', table_name='c023_license_context')
    op.drop_index('ix_c023_license_context_membership_id', table_name='c023_license_context')
    op.drop_table('c023_license_context')
