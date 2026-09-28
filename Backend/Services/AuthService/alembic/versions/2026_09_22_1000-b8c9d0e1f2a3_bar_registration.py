"""bar_registration

Revision ID: b8c9d0e1f2a3
Revises: a7b8c9d0e1f2
Create Date: 2026-09-22 10:00:00.000000

Enterprise BAR — WP-23 Workstream C ("canonical Business Activity
registration mechanism"). Creates the single, BAR-owned registration
table, hosted in `AuthService` alongside `bar_identifier_ledger`
(Workstream B) for the same reason — no capability-specific business
data, and `AuthService` already hosts every other cross-cutting registry
table in this repository.

CLAUDE.md §18 / §19.4 confirmation at the point of creation: this
migration is PURELY ADDITIVE — one `op.create_table(...)` call plus its
indexes/constraints and one `op.create_foreign_key`-equivalent (expressed
inline via `ForeignKeyConstraint`). NO `ALTER` to any existing table,
including `bar_identifier_ledger` (the FK references it, but does not
modify it). No PostgreSQL SEQUENCE is created — identifier allocation
remains the Workstream B application-level allocator
(`BarRegistrationService._next_identifier`, reusing
`BarIdentifierRepository.max_identifier_sequence`). No new architectural
question arises — the table shape was recorded conceptually in the
independently-authored consolidated BAR design
(`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §4`)
and `BAR-INDEX.md §3`, and surfaces no further Repository Owner decision.

Design notes:
  * `identifier` (String(20), UNIQUE, FOREIGN KEY ->
    `bar_identifier_ledger.identifier`) — a registration can only exist
    for an identifier BAR itself has already issued (D5); the FK
    enforces this at the database level, not merely by application
    discipline.
  * `business_activity_reference` (String(255)) + `owning_work_package`
    (String(50)) together carry a UNIQUE constraint
    (`uq_bar_registration_wp_reference`) — the duplicate-registration
    protection (`[IMPLEMENTATION DESIGN]`; no source specifies a
    duplicate-detection key, so this reuses two already-approved fields
    rather than inventing a new identity scheme).
  * `registration_status` (String(20)) carries a CHECK constraint
    restricting it to the single literal value `'REGISTERED'` — D2/D6's
    own two-state minimum, where "not registered" is the absence of a
    row, not a second stored value.
  * `owning_capability` / `owning_work_package` are opaque `String`
    references only — no FK into any capability/WP table, since neither
    exists as a database object (`CAP-001`/`WPR-001` are governance
    documents, per D7's own "linked, not merged" boundary).
  * `registering_act` is a free-text governance-act citation, never
    validated against a fixed enum.
  * `is_retroactive` (Boolean) is caller-supplied, per D3's own
    retroactive-vs-prospective distinction.
  * No `organization_id` column — platform-global metadata about the
    enterprise BAR mechanism itself, not tenant business data.

`down_revision` is the current single non-branching head `a7b8c9d0e1f2`
(WP-23 Workstream B / `bar_identifier_ledger`); this migration becomes
the new single head, no branch.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b8c9d0e1f2a3'
down_revision: Union[str, Sequence[str], None] = 'a7b8c9d0e1f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'bar_registration',
        sa.Column('id',                            sa.UUID(),                  nullable=False),
        sa.Column('identifier',                    sa.String(20),              nullable=False),
        sa.Column('business_activity_reference',   sa.String(255),             nullable=False),
        sa.Column('owning_capability',              sa.String(50),              nullable=False),
        sa.Column('owning_work_package',            sa.String(50),              nullable=False),
        sa.Column('registration_status',            sa.String(20),              nullable=False, server_default='REGISTERED'),
        sa.Column('registering_act',                sa.String(255),             nullable=False),
        sa.Column('registered_at',                  sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_retroactive',                 sa.Boolean(),               nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_bar_registration'),
        sa.ForeignKeyConstraint(
            ['identifier'], ['bar_identifier_ledger.identifier'],
            name='fk_bar_registration_identifier',
        ),
        sa.UniqueConstraint('identifier', name='uq_bar_registration_identifier'),
        sa.UniqueConstraint(
            'owning_work_package', 'business_activity_reference',
            name='uq_bar_registration_wp_reference',
        ),
        sa.CheckConstraint(
            "registration_status = 'REGISTERED'",
            name='ck_bar_registration_status',
        ),
    )
    op.create_index(
        'ix_bar_registration_identifier',
        'bar_registration', ['identifier'],
    )


def downgrade() -> None:
    op.drop_index('ix_bar_registration_identifier', table_name='bar_registration')
    op.drop_table('bar_registration')
