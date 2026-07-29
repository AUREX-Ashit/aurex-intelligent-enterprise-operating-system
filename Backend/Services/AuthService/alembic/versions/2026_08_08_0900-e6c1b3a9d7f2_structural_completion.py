"""structural_completion

Revision ID: e6c1b3a9d7f2
Revises: d2a8f4c6b9e3
Create Date: 2026-08-08 09:00:00.000000

WP-04 BA-08 — Complete Structural Transition (ERB-C005-08 / EX-C005-11
per PE-001-C005; RSC-000001, ADR-013, IRA-004 §27).

Creates `structural_completions` — a genuine new table (not an
Extend), since RSC-000001 is its own registered Aggregate Root
(IRA-004 §27). FK to `structural_validations.id` — already exists as
of this migration's own down_revision.

`structural_validation_id` is UNIQUE — enforces the guarded
(non-idempotent) completion decision at the database level, a second
line of defense behind the service layer's own pre-check (mirroring
`uq_organizations_organization_code`'s own established role for
`OrganizationService.establish()`).

**Option A scope:** this migration does not touch `organization_nodes`
and does not create `organization_hierarchy` or
`consolidation_determination` — the deferred ERG-001 mutation
mechanism is recorded as TD-070, not built here.

`status` is constrained to IRA-004 §27's own registered Lifecycle
Model. Only CREATED is reachable by this Business Activity's own code
(TD-069).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e6c1b3a9d7f2'
down_revision: Union[str, Sequence[str], None] = 'd2a8f4c6b9e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'structural_completions',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('structural_validation_id', sa.Uuid(), nullable=False),
        sa.Column('completion_notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='CREATED'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('CREATED', 'ARCHIVED')",
            name='ck_structural_completions_status',
        ),
        sa.ForeignKeyConstraint(['structural_validation_id'], ['structural_validations.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('structural_validation_id', name='uq_structural_completions_structural_validation_id'),
    )


def downgrade() -> None:
    op.drop_table('structural_completions')
