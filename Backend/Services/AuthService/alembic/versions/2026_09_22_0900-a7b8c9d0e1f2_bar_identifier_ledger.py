"""bar_identifier_ledger

Revision ID: a7b8c9d0e1f2
Revises: f6a7b8c9d0e1
Create Date: 2026-09-22 09:00:00.000000

Enterprise BAR — WP-23 Workstream B ("Business Activity Identifier
issuance mechanism"). Creates the single, BAR-owned identifier ledger
table, hosted in `AuthService` per the WP-23 Charter (no dedicated hosting
decision was required — this table has no capability-specific business
data, and `AuthService` already hosts every other cross-cutting registry
table in this repository, e.g. `configuration_entry`, `tenant_registry`).

CLAUDE.md §18 / §19.4 confirmation at the point of creation: this
migration is PURELY ADDITIVE — one `op.create_table(...)` call plus its
index. NO `ALTER` to any existing table. No PostgreSQL SEQUENCE is
created — the `identifier` allocation mechanism is an application-level
allocator (`BarIdentifierService._next_identifier`) backed by the UNIQUE
constraint, mirroring `[RO DECISION]` O1's own already-certified pattern
for `c021_offering_definition.offering_reference`. No new architectural
question arises — the table shape was recorded conceptually in the
independently-authored consolidated BAR design
(`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §4`/
`§6`) and the WP-23 Charter, and surfaces no further Repository Owner
decision.

Design notes:
  * `identifier` (String(20), UNIQUE) is the canonical Business Activity
    Identifier (`SD-002-004`, D5) — `BA-NNNNNN`, system-assigned,
    monotonic, unique, concurrency-safe. Never caller-supplied.
  * This table carries NO Business Activity name, capability, Work
    Package, registration-status, or any other registration-record
    field — deliberately, per the approved design's own separation of
    "identifier issuance" from "Business Activity registration"
    (`§19a.6`). Workstream C (not yet built) will consume this table's
    own issuance capability inside its own, separate registration
    record — not built by this migration.
  * `issued_at` is a plain audit/traceability timestamp.
  * No `organization_id` column — this table is platform-global metadata
    about the enterprise BAR mechanism itself, not tenant business data.

`down_revision` is the current single non-branching head `f6a7b8c9d0e1`
(WP-21 / c022_commercial_account); this migration becomes the new single
head, no branch.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a7b8c9d0e1f2'
down_revision: Union[str, Sequence[str], None] = 'f6a7b8c9d0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'bar_identifier_ledger',
        sa.Column('id',          sa.UUID(),                  nullable=False),
        sa.Column('identifier',  sa.String(20),               nullable=False),
        sa.Column('issued_at',   sa.DateTime(timezone=True),  nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_bar_identifier_ledger'),
        sa.UniqueConstraint('identifier', name='uq_bar_identifier_ledger_identifier'),
    )
    op.create_index(
        'ix_bar_identifier_ledger_identifier',
        'bar_identifier_ledger', ['identifier'],
    )


def downgrade() -> None:
    op.drop_index('ix_bar_identifier_ledger_identifier', table_name='bar_identifier_ledger')
    op.drop_table('bar_identifier_ledger')
