"""organization_lifecycle_profile_fields

Revision ID: b3f7a1c9d2e4
Revises: 8fac154e79e2
Create Date: 2026-07-20 19:30:00.000000

WP-01, Establish Organization (Business Activity 1 of C-004).

Adds the two columns needed for this Business Activity, scoped per
ADR-004 (Organization Canonical Schema Scope) and ADR-005 (Organization
Lifecycle Interim Model):

  - status:      interim lifecycle state ('ACTIVE' / 'SUSPENDED'), per
                 ADR-005 — a plain column, not the metadata-driven state
                 machine SD-002-051 ultimately requires (no Metadata
                 Runtime exists yet to drive one). Extension point: this
                 column is the seam a future Metadata Runtime migration
                 replaces.
  - description: minimal Organization Profile field. Deliberately not
                 the full organization_master shape (sector, industry,
                 reporting_framework_json, etc.) — those remain deferred
                 to future work packages per ADR-004.

Purely additive — no existing column is renamed, retyped, or dropped.
`is_active` is left untouched for backward compatibility with WP-00's
bootstrap seeding and any existing consumer; `status` is the new
lifecycle-authoritative field going forward.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b3f7a1c9d2e4'
down_revision: Union[str, Sequence[str], None] = '8fac154e79e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'organizations',
        sa.Column('status', sa.String(20), nullable=False, server_default=sa.text("'ACTIVE'")),
    )
    op.add_column(
        'organizations',
        sa.Column('description', sa.String(1000), nullable=True),
    )
    op.create_check_constraint(
        'ck_organizations_status',
        'organizations',
        "status IN ('ACTIVE', 'SUSPENDED')",
    )


def downgrade() -> None:
    op.drop_constraint('ck_organizations_status', 'organizations', type_='check')
    op.drop_column('organizations', 'description')
    op.drop_column('organizations', 'status')
