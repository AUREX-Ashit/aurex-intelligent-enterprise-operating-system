"""configuration_entry

Revision ID: c7e2b5a9f1d4
Revises: b1d6f4c8a3e7
Create Date: 2026-08-12 09:00:00.000000

WP-10 — Configuration Management (C-041). Registers Configuration Entry
(CFG-000001, ADR-019) as a canonical Business Object per CMD-001
§26.3a/§26.4 (IRA-010 §6): independent identity, cross-Business-Activity
reference (BA-01 resolves records BA-02 established), and a governed
lifecycle (CMD-001 §12.5's mandatory Versioning/Effective Dating/
Lifecycle State/Audit Trail).

- configuration_entries (BA-01/BA-02, EX-C041-01/02): one row per
  TENANT- or USER-scope override, identified by
  (organization_id, person_id, scope_level, facet, key). Global Platform
  scope is never persisted — see models/configuration_entry.py's own
  class docstring.

FK to organizations.id / persons.id — already exist as of this
migration's own down_revision.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c7e2b5a9f1d4'
down_revision: Union[str, Sequence[str], None] = 'b1d6f4c8a3e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'configuration_entries',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('person_id', sa.Uuid(), nullable=True),
        sa.Column('scope_level', sa.String(20), nullable=False),
        sa.Column('facet', sa.String(20), nullable=False),
        sa.Column('key', sa.String(100), nullable=False),
        sa.Column('value', sa.JSON(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('lifecycle_state', sa.String(20), nullable=False, server_default='ACTIVE'),
        sa.Column('effective_from', sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_to', sa.DateTime(timezone=True), nullable=True),
        sa.Column('established_by_person_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "scope_level IN ('TENANT', 'USER')",
            name='ck_configuration_entries_scope_level',
        ),
        sa.CheckConstraint(
            "facet IN ('TERMINOLOGY', 'BRANDING', 'THEME', 'ACCESSIBILITY', 'LOCALIZATION')",
            name='ck_configuration_entries_facet',
        ),
        sa.CheckConstraint(
            "lifecycle_state IN ('ACTIVE', 'SUPERSEDED', 'RETIRED')",
            name='ck_configuration_entries_lifecycle_state',
        ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['established_by_person_id'], ['persons.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_configuration_entries_organization_id', 'configuration_entries', ['organization_id'])
    op.create_index('ix_configuration_entries_scope_level', 'configuration_entries', ['scope_level'])
    op.create_index('ix_configuration_entries_facet', 'configuration_entries', ['facet'])
    op.create_index(
        'ix_configuration_entries_org_facet_key',
        'configuration_entries',
        ['organization_id', 'facet', 'key'],
    )


def downgrade() -> None:
    op.drop_index('ix_configuration_entries_org_facet_key', table_name='configuration_entries')
    op.drop_index('ix_configuration_entries_facet', table_name='configuration_entries')
    op.drop_index('ix_configuration_entries_scope_level', table_name='configuration_entries')
    op.drop_index('ix_configuration_entries_organization_id', table_name='configuration_entries')
    op.drop_table('configuration_entries')
