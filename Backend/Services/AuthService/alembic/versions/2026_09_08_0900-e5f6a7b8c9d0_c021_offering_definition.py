"""c021_offering_definition

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-09-08 09:00:00.000000

C-021 Product & Service Catalog — WP-20 BA-01 ("Establish / Manage Offering
Definition"). Creates the single C-021-owned Offering Definition table,
hosted in `AuthService` per the Repository Owner's own service-hosting
decision (`TDS-C021 §5`, Option A — `AuthService` selected over a new
`CommercialService`). The exact column set, constraints, and indexes are
`TDS-C021 §9` (the conceptual schema-shape STOP-and-report, performed after
the host was resolved) — nothing added beyond what that design records, and
as amended by Repository Owner decisions O1 (identity generation is a set of
acceptance properties, not a mandated PostgreSQL SEQUENCE) and O2
(`category_ref` is OPTIONAL / NULLABLE).

CLAUDE.md §18 / §19.4 confirmation at the point of creation: this migration
is PURELY ADDITIVE — one `op.create_table(...)` call plus its indexes. NO
`ALTER` to any existing table. No PostgreSQL SEQUENCE is created — the
`offering_reference` allocation mechanism is an application-level allocator
(`OfferingDefinitionService._next_offering_reference`) backed by the UNIQUE
constraint, per O1 (a SEQUENCE is not mandated; if a future implementation
needs one it is introduced through a separate §18/§19.4 change-control pass).
No new architectural question arises — the schema shape was recorded
conceptually in an independently-reviewed TDS and surfaced no further
Repository Owner decision (`TDS-C021 §9.11`).

Platform-global (`ROD-C021` D8): there is NO `organization_id` column. The
authority boundary is `require_platform_admin` (mirroring `roles`), enforced
at the router; `/offerings` is tenant-middleware-exempt on the same basis as
`/roles`.

Design notes carried from `TDS-C021 §9`:
  * `offering_reference` (String(30), UNIQUE) is the `COM-001-001` Universal
    Identity (`PREFIX-NNNNNN`) and the stable Offering Reference downstream
    commercial capabilities consume. System-assigned, monotonic, unique,
    concurrency-safe (O1).
  * `offering_kind` and `state` are CHECK-constrained closed sets
    (`COM-001-021` Product↔Service axis; `COM-001-020` state model),
    mirroring `ck_c132_notification_*`. BA-01 only ever writes
    `state = 'draft'`; the full closed set is declared for correctness.
  * `category_ref` and `list_price_reference` are nullable, opaque,
    non-authoritative String references — no FK, no taxonomy table, no
    price table (`COM-001-024` taxonomy authority and pricing execution are
    both Pending Canonical Binding).
  * `version` / `supersedes_id` are declared for the future Version
    Management increment (`COM-001-025`); BA-01 always writes `version = 1`
    and `supersedes_id = NULL`.
  * `created_by_actor_id` (UUID, NOT a foreign key) is a point-in-time audit
    citation of the PLATFORM_ADMIN caller's person_id — mirroring
    `committed_by_actor_id`.
  * NO uniqueness constraint on `offering_name` — two `draft` offerings may
    legitimately share a name (`TDS-C021 §9.5`).

Row-Level Security: not added here, on the same basis as every other
AuthService migration.

`down_revision` is the current single non-branching head `d4e5f6a7b8c9`
(WP-19 / c132_notification); this migration becomes the new single head, no
branch.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e5f6a7b8c9d0'
down_revision: Union[str, Sequence[str], None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'c021_offering_definition',
        sa.Column('id',                    sa.UUID(),                  nullable=False),
        sa.Column('offering_reference',    sa.String(30),              nullable=False),
        sa.Column('offering_name',         sa.String(255),             nullable=False),
        sa.Column('offering_kind',         sa.String(20),              nullable=False),
        sa.Column('category_ref',          sa.String(100),             nullable=True),
        sa.Column('list_price_reference',  sa.String(100),             nullable=True),
        sa.Column('state',                 sa.String(20),              nullable=False),
        sa.Column('version',               sa.Integer(),               nullable=False, server_default='1'),
        sa.Column('supersedes_id',         sa.UUID(),                  nullable=True),
        sa.Column('created_by_actor_id',   sa.UUID(),                  nullable=False),
        sa.Column('created_at',            sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',            sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_c021_offering_definition'),
        sa.ForeignKeyConstraint(
            ['supersedes_id'], ['c021_offering_definition.id'],
            name='fk_c021_offering_definition_supersedes_id',
        ),
        sa.UniqueConstraint('offering_reference', name='uq_c021_offering_definition_offering_reference'),
        sa.CheckConstraint(
            "offering_kind IN ('PRODUCT', 'SERVICE')",
            name='ck_c021_offering_definition_kind',
        ),
        sa.CheckConstraint(
            "state IN ('draft', 'published', 'retired')",
            name='ck_c021_offering_definition_state',
        ),
    )
    op.create_index(
        'ix_c021_offering_definition_offering_reference',
        'c021_offering_definition', ['offering_reference'],
    )
    op.create_index(
        'ix_c021_offering_definition_state',
        'c021_offering_definition', ['state'],
    )


def downgrade() -> None:
    op.drop_index('ix_c021_offering_definition_state', table_name='c021_offering_definition')
    op.drop_index('ix_c021_offering_definition_offering_reference', table_name='c021_offering_definition')
    op.drop_table('c021_offering_definition')
