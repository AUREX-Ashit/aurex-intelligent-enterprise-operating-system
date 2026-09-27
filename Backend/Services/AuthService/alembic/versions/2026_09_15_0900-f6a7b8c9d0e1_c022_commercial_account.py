"""c022_commercial_account

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-09-15 09:00:00.000000

C-022 Customer & Account Management — WP-21 BA-01 ("Establish Commercial
Account"). Creates the single C-022-owned Commercial Account table, hosted in
`AuthService` per the Repository Owner's own service-hosting decision
(`ROD-C022` D3). The exact column set, constraints, and indexes are
`TDS-C022 §6.1` (the conceptual schema-shape STOP-and-report) — nothing
added beyond what that design records.

CLAUDE.md §18 / §19.4 confirmation at the point of creation: this migration
is PURELY ADDITIVE — one `op.create_table(...)` call plus its index. NO
`ALTER` to any existing table. No PostgreSQL SEQUENCE is created — the
`account_reference` allocation mechanism is an application-level allocator
(`CommercialAccountService._next_account_reference`) backed by the UNIQUE
constraint, mirroring `c021_offering_definition`'s own O1 disposition.

Platform-global (`ROD-C022` D2): there is NO `organization_id` column. The
authority boundary is `require_platform_admin` (mirroring `roles`/
`offerings`), enforced at the router; `/commercial-accounts` is
tenant-middleware-exempt on the same basis.

**No `classification` column** (`ADR-038` Option A; `ROD-C022-A` D7).
`COM-001-033` governs Account as written — identity, hierarchy position, and
status only.

Design notes carried from `TDS-C022 §6.1`:
  * `account_reference` (String(30), UNIQUE) is the `COM-001-001` Universal
    Identity (`PREFIX-NNNNNN`) and the stable Account Reference
    (`COM-001-036`). System-assigned, monotonic, unique, concurrency-safe.
  * `status` is a CHECK-constrained closed set (`active`, `suspended`,
    `retired`) mirroring `ck_c021_offering_definition_state`. BA-01 only
    ever writes `status = 'active'`; the full closed set is declared for
    correctness.
  * `parent_account_id` is a nullable, self-referential FK
    (`COM-001-033`'s Account-to-Account hierarchy position) — declared for a
    future structural increment (`ERB-C022-04`); BA-01 always writes NULL.
  * `created_by_actor_id` (UUID, NOT a foreign key) is a point-in-time audit
    citation of the PLATFORM_ADMIN caller's person_id — mirroring
    `c021_offering_definition.created_by_actor_id`.
  * NO uniqueness constraint on `account_name` — `COM-001-033` states none
    (`TDS-C022 §6.1`).

Row-Level Security: not added here, on the same basis as every other
AuthService migration.

`down_revision` is the current single non-branching head `e5f6a7b8c9d0`
(WP-20 / c021_offering_definition); this migration becomes the new single
head, no branch.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f6a7b8c9d0e1'
down_revision: Union[str, Sequence[str], None] = 'e5f6a7b8c9d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'c022_commercial_account',
        sa.Column('id',                    sa.UUID(),                  nullable=False),
        sa.Column('account_reference',     sa.String(30),              nullable=False),
        sa.Column('account_name',          sa.String(255),             nullable=False),
        sa.Column('status',                sa.String(20),              nullable=False),
        sa.Column('parent_account_id',     sa.UUID(),                  nullable=True),
        sa.Column('created_by_actor_id',   sa.UUID(),                  nullable=False),
        sa.Column('created_at',            sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',            sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_c022_commercial_account'),
        sa.ForeignKeyConstraint(
            ['parent_account_id'], ['c022_commercial_account.id'],
            name='fk_c022_commercial_account_parent_account_id',
        ),
        sa.UniqueConstraint('account_reference', name='uq_c022_commercial_account_account_reference'),
        sa.CheckConstraint(
            "status IN ('active', 'suspended', 'retired')",
            name='ck_c022_commercial_account_status',
        ),
    )
    op.create_index(
        'ix_c022_commercial_account_account_reference',
        'c022_commercial_account', ['account_reference'],
    )


def downgrade() -> None:
    op.drop_index('ix_c022_commercial_account_account_reference', table_name='c022_commercial_account')
    op.drop_table('c022_commercial_account')
