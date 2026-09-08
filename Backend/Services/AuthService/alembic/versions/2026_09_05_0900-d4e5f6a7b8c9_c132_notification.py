"""c132_notification

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-09-05 09:00:00.000000

C-132 Enterprise Notifications — WP-19 BA-01 ("Establish / Manage Enterprise
Notification Context"). Creates the single C-132-owned Notification table,
hosted in `AuthService` per the Repository Owner's own service-hosting
decision (`TDS-C132 §6.5`, H-1 selected over `AIService`/H-2 and a
deferred-decision H-3). The exact column set, constraints, and indexes are
`TDS-C132 §6.6` (the conceptual schema-shape STOP-and-report, performed
after the host was resolved) — nothing added beyond what that design
records.

CLAUDE.md §18 / §19.4 confirmation at the point of creation: this migration
is PURELY ADDITIVE — one `op.create_table(...)` call plus its indexes. NO
`ALTER` to any existing table. `memberships` is only referenced by foreign
key, never modified. No new architectural question arises — the schema
shape was recorded conceptually in a finalized TDS, independently
consistency-reviewed (`TDS-C132 §28`), and surfaced no further Repository
Owner decision (`TDS-C132 §6.6` item 11).

Design notes carried from `TDS-C132 §6.6`:
  * `membership_id` (FK -> memberships.id) is BOTH the recipient anchor and
    the tenant anchor — no duplicated `organization_id` column, mirroring
    `access_evaluation_outcomes`' own choice. Tenant isolation is enforced
    at the service layer (`NotificationEstablishmentService`), exactly as
    every prior AuthService Work Package does (TD-096 / TD-159 / TD-160,
    the known repository-wide harness limitation — no new debt introduced).
  * `source_type` (free-text) + `source_id` (UUID, NOT a foreign key) are
    a point-in-time, non-authoritative citation of the causing action —
    mirroring `committed_by_actor_id` / `entitlement_source_reference`.
    A real FK is not used because the causing table varies by capability;
    inventing a polymorphic association to support one would be new
    architecture §18 does not authorize here.
  * `severity` and `status` are CHECK-constrained closed sets
    (`DS-001-350`; `TDS-C132 §10`), mirroring
    `ck_access_evaluation_outcomes_*`.
  * NO uniqueness constraint — a recipient may legitimately receive
    multiple, distinct notifications from the same source over time
    (`TDS-C132 §6.6` item 8).

Row-Level Security: not added here, on the same basis as every other
AuthService migration (`2026_09_01_0900-c3d4e5f6a7b8` docstring).

`down_revision` is the current single non-branching head `c3d4e5f6a7b8`
(WP-17); this migration becomes the new single head, no branch.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'c132_notification',
        sa.Column('id',                 sa.UUID(),                  nullable=False),
        sa.Column('membership_id',      sa.UUID(),                  nullable=False),
        sa.Column('severity',           sa.String(20),              nullable=False),
        sa.Column('what_happened',      sa.Text(),                  nullable=False),
        sa.Column('why_it_matters',     sa.Text(),                  nullable=True),
        sa.Column('what_happens_next',  sa.Text(),                  nullable=True),
        sa.Column('source_type',        sa.String(100),             nullable=False),
        sa.Column('source_id',          sa.UUID(),                  nullable=True),
        sa.Column('status',             sa.String(20),              nullable=False),
        sa.Column('created_at',         sa.DateTime(timezone=True), nullable=False),
        sa.Column('acknowledged_at',    sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at',         sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['membership_id'], ['memberships.id'], name='fk_c132_notification_membership_id'),
        sa.PrimaryKeyConstraint('id', name='pk_c132_notification'),
        sa.CheckConstraint(
            "severity IN ('success', 'info', 'warning', 'danger')",
            name='ck_c132_notification_severity',
        ),
        sa.CheckConstraint(
            "status IN ('UNREAD', 'ACKNOWLEDGED')",
            name='ck_c132_notification_status',
        ),
    )
    op.create_index(
        'ix_c132_notification_membership_id',
        'c132_notification', ['membership_id'],
    )
    op.create_index(
        'ix_c132_notification_membership_status',
        'c132_notification', ['membership_id', 'status'],
    )


def downgrade() -> None:
    op.drop_index('ix_c132_notification_membership_status', table_name='c132_notification')
    op.drop_index('ix_c132_notification_membership_id', table_name='c132_notification')
    op.drop_table('c132_notification')
