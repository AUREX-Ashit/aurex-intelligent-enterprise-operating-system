"""organization_retired_lifecycle_state

Revision ID: d2d840d224b6
Revises: b3f7a1c9d2e4
Create Date: 2026-07-21 21:00:00.000000

WP-01, Retire Organization & Preserve Continuity (BA-07, ERB-C004-07 per
PE-001-C004).

PE-001-C004 defines a third, terminal lifecycle state, RETIRED, in
addition to the ACTIVE/SUSPENDED pair ADR-005 scoped as WP-01's interim
model. This migration widens the existing `ck_organizations_status`
CHECK constraint (added in b3f7a1c9d2e4) to also permit 'RETIRED' — no
new column, no renamed/dropped column, purely an additive constraint
change consistent with ADR-005's interim lifecycle model (a plain
status column, not yet the metadata-driven state machine SD-002-051
ultimately requires).
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd2d840d224b6'
down_revision: Union[str, Sequence[str], None] = 'b3f7a1c9d2e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('ck_organizations_status', 'organizations', type_='check')
    op.create_check_constraint(
        'ck_organizations_status',
        'organizations',
        "status IN ('ACTIVE', 'SUSPENDED', 'RETIRED')",
    )


def downgrade() -> None:
    op.drop_constraint('ck_organizations_status', 'organizations', type_='check')
    op.create_check_constraint(
        'ck_organizations_status',
        'organizations',
        "status IN ('ACTIVE', 'SUSPENDED')",
    )
