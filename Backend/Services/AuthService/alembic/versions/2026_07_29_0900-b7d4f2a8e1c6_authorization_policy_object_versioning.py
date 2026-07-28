"""authorization_policy_object_versioning

Revision ID: b7d4f2a8e1c6
Revises: a4c8e1f6d9b3
Create Date: 2026-07-29 09:00:00.000000

WP-02 BA-07 — Version and Re-effective-Date Authorization Policy Object
(ERB-C003-02 / EX-C003-07 per PE-001-C003). Realizes SD-002-011's
Canonical Temporal Model (Effective From, Effective To, Version, Status,
Approval Reference) and BR-C003-05 (every version amendment preserves
its immediately prior version as an inspectable historical record)
uniformly across all five WP-02 authorization policy objects — roles,
domain_permissions, approval_authorities, delegation_policies, and
runtime_assignment_policies — per IMP-001 §13.17's Engineering
Specialization Framework governing rule that one mechanism, not
type-specific variants, realizes a shared Enterprise Engineering
artifact.

domain_permissions already had effective_from/effective_to (BA-02); this
migration adds only the four properties it was missing (version, status,
approval_reference, supersedes_id). The other four tables gain the full
five-property set. New columns default to version=1, status='ACTIVE',
matching every already-established row's implicit current state.

One necessary correction, not purely additive: roles.role_code carried
a plain, whole-table UNIQUE constraint (WP-00, uq_roles_role_code /
ix_roles_role_code) predating versioning. Under BR-C003-05, a SUPERSEDED
row legitimately shares role_code with its current ACTIVE successor —
the plain constraint would reject every Role version amendment outright.
This migration replaces it with a partial unique index scoped to
status = 'ACTIVE', discovered as an unavoidable consequence of BA-07's
own versioning requirement while implementing it, not a speculative
change. Existing data is unaffected: every pre-existing role_code has
exactly one row today, and every one of them defaults to status='ACTIVE'
above, so the new partial index is satisfied immediately.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b7d4f2a8e1c6'
down_revision: Union[str, Sequence[str], None] = 'a4c8e1f6d9b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_FULL_SET_TABLES = [
    ("roles", "ck_roles_status"),
    ("approval_authorities", "ck_approval_authorities_status"),
    ("delegation_policies", "ck_delegation_policies_status"),
    ("runtime_assignment_policies", "ck_runtime_assignment_policies_status"),
]


def upgrade() -> None:
    # Four tables gain the full Canonical Temporal Model: version, status,
    # effective_from, effective_to, approval_reference, supersedes_id.
    for table_name, status_constraint_name in _FULL_SET_TABLES:
        op.add_column(table_name, sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
        op.add_column(table_name, sa.Column('status', sa.String(20), nullable=False, server_default='ACTIVE'))
        op.add_column(table_name, sa.Column('effective_from', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
        op.add_column(table_name, sa.Column('effective_to', sa.DateTime(timezone=True), nullable=True))
        op.add_column(table_name, sa.Column('approval_reference', sa.String(255), nullable=True))
        op.add_column(table_name, sa.Column('supersedes_id', sa.UUID(), nullable=True))
        op.create_foreign_key(
            f'fk_{table_name}_supersedes_id', table_name, table_name,
            ['supersedes_id'], ['id'],
        )
        op.create_check_constraint(
            status_constraint_name, table_name,
            "status IN ('ACTIVE', 'SUPERSEDED')",
        )
        op.create_index(f'ix_{table_name}_supersedes_id', table_name, ['supersedes_id'])

    # domain_permissions already has effective_from/effective_to (BA-02) —
    # add only the four properties it was missing.
    op.add_column('domain_permissions', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('domain_permissions', sa.Column('status', sa.String(20), nullable=False, server_default='ACTIVE'))
    op.add_column('domain_permissions', sa.Column('approval_reference', sa.String(255), nullable=True))
    op.add_column('domain_permissions', sa.Column('supersedes_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'fk_domain_permissions_supersedes_id', 'domain_permissions', 'domain_permissions',
        ['supersedes_id'], ['id'],
    )
    op.create_check_constraint(
        'ck_domain_permissions_status', 'domain_permissions',
        "status IN ('ACTIVE', 'SUPERSEDED')",
    )
    op.create_index('ix_domain_permissions_supersedes_id', 'domain_permissions', ['supersedes_id'])

    # Necessary correction (see module docstring): roles.role_code's
    # uniqueness must be scoped to ACTIVE rows only, now that a Role's
    # version history can hold multiple rows sharing one role_code.
    op.drop_index('ix_roles_role_code', table_name='roles')
    op.drop_constraint('uq_roles_role_code', 'roles', type_='unique')
    op.create_index(
        'ix_roles_role_code_active_unique', 'roles', ['role_code'],
        unique=True, sqlite_where=sa.text("status = 'ACTIVE'"), postgresql_where=sa.text("status = 'ACTIVE'"),
    )


def downgrade() -> None:
    op.drop_index('ix_roles_role_code_active_unique', table_name='roles')
    op.create_unique_constraint('uq_roles_role_code', 'roles', ['role_code'])
    op.create_index('ix_roles_role_code', 'roles', ['role_code'], unique=True)

    op.drop_index('ix_domain_permissions_supersedes_id', table_name='domain_permissions')
    op.drop_constraint('ck_domain_permissions_status', 'domain_permissions', type_='check')
    op.drop_constraint('fk_domain_permissions_supersedes_id', 'domain_permissions', type_='foreignkey')
    op.drop_column('domain_permissions', 'supersedes_id')
    op.drop_column('domain_permissions', 'approval_reference')
    op.drop_column('domain_permissions', 'status')
    op.drop_column('domain_permissions', 'version')

    for table_name, status_constraint_name in reversed(_FULL_SET_TABLES):
        op.drop_index(f'ix_{table_name}_supersedes_id', table_name=table_name)
        op.drop_constraint(status_constraint_name, table_name, type_='check')
        op.drop_constraint(f'fk_{table_name}_supersedes_id', table_name, type_='foreignkey')
        op.drop_column(table_name, 'supersedes_id')
        op.drop_column(table_name, 'approval_reference')
        op.drop_column(table_name, 'effective_to')
        op.drop_column(table_name, 'effective_from')
        op.drop_column(table_name, 'status')
        op.drop_column(table_name, 'version')
