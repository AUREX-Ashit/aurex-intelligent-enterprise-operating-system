"""membership_approval_authority

Revision ID: f9a3c7e1b5d2
Revises: b2c3d4e5f6a7
Create Date: 2026-08-29 11:00:00.000000

C-003 Role & Permission Management — WP-18 (TDS-018, Approval Authority
Runtime Binding). Creates `membership_approval_authority`, the canonical
Membership <-> Approval Authority join table already specified in
`Master_Technical_Architecture.md` (lines 1318-1329) but never
implemented anywhere in this codebase until now — the "real dependent of
an Approval Authority" `approval_authority_repository.py`'s own
`get_active_dependents()` docstring already disclosed (TD-023/TD-028).

Exact canonical column set: membership_id, approval_authority_id,
effective_from, effective_to, composite PK on the first three. No column
beyond what is canonically specified is added.

An active-binding uniqueness constraint (at most one currently-open,
`effective_to IS NULL`, binding per (membership_id, approval_authority_id)
pair) is enforced via a partial unique index — TDS-018 §19's own disclosed
hardening recommendation, mirroring `authority_holders`'s own
`ux_authority_holders_active_authority` precedent exactly.

Purely additive: this migration creates one new table only. No existing
table — including `approval_authorities` and `memberships`, both
certified (WP-02/WP-03) — is altered in any way.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f9a3c7e1b5d2'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'membership_approval_authority',
        sa.Column('membership_id',          sa.UUID(),        nullable=False),
        sa.Column('approval_authority_id',  sa.UUID(),        nullable=False),
        sa.Column('effective_from',         sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_to',           sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['membership_id'], ['memberships.id'], name='fk_membership_approval_authority_membership_id'),
        sa.ForeignKeyConstraint(['approval_authority_id'], ['approval_authorities.id'], name='fk_membership_approval_authority_approval_authority_id'),
        sa.PrimaryKeyConstraint('membership_id', 'approval_authority_id', 'effective_from', name='pk_membership_approval_authority'),
    )
    op.create_index(
        'ux_membership_approval_authority_active',
        'membership_approval_authority',
        ['membership_id', 'approval_authority_id'],
        unique=True,
        sqlite_where=sa.text("effective_to IS NULL"),
        postgresql_where=sa.text("effective_to IS NULL"),
    )


def downgrade() -> None:
    op.drop_index('ux_membership_approval_authority_active', table_name='membership_approval_authority')
    op.drop_table('membership_approval_authority')
