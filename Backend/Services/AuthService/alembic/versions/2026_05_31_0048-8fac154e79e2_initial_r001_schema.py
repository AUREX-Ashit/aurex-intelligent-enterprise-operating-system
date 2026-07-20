"""initial_r001_schema

Revision ID: 8fac154e79e2
Revises:
Create Date: 2026-05-31 00:48:53.432510

R-001 Phase 1 — initial schema for:
  organizations, persons, identities, roles, permissions,
  role_permissions, memberships, refresh_tokens

Legacy tables (tenants, users) are intentionally excluded from this
migration. They remain in models/user.py but are not imported by
models/__init__.py and therefore do not appear in Base.metadata.
They should be removed in a separate cleanup migration.

Creation order respects foreign-key dependencies:
  1. organizations      (no FKs)
  2. persons            (no FKs)
  3. roles              (no FKs)
  4. permissions        (no FKs)
  5. identities         (FK → persons)
  6. role_permissions   (FK → roles, permissions)
  7. memberships        (FK → persons, organizations, roles)
  8. refresh_tokens     (FK → identities)

Drop order in downgrade() is the exact reverse.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8fac154e79e2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # 1. organizations
    #    Tenant boundary. organization_id appears in JWT claims.
    # ------------------------------------------------------------------
    op.create_table(
        'organizations',
        sa.Column('id',                sa.UUID(),        nullable=False),
        sa.Column('organization_code', sa.String(50),    nullable=False),
        sa.Column('organization_name', sa.String(255),   nullable=False),
        sa.Column('organization_type', sa.String(50),    nullable=False),
        sa.Column('is_active',         sa.Boolean(),     nullable=False, server_default=sa.text('true')),
        sa.Column('created_at',        sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',        sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_organizations'),
        sa.UniqueConstraint('organization_code', name='uq_organizations_organization_code'),
    )
    # Explicit index on organization_code to support fast tenant lookups via header
    op.create_index('ix_organizations_organization_code', 'organizations', ['organization_code'], unique=True)

    # ------------------------------------------------------------------
    # 2. persons
    #    A human being known to the platform. Has no direct FK constraints.
    #    Credentials live in identities; org context lives in memberships.
    # ------------------------------------------------------------------
    op.create_table(
        'persons',
        sa.Column('id',           sa.UUID(),       nullable=False),
        sa.Column('first_name',   sa.String(100),  nullable=False),
        sa.Column('last_name',    sa.String(100),  nullable=False),
        sa.Column('display_name', sa.String(255),  nullable=False),
        sa.Column('is_active',    sa.Boolean(),    nullable=False, server_default=sa.text('true')),
        sa.Column('created_at',   sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',   sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_persons'),
    )

    # ------------------------------------------------------------------
    # 3. roles
    #    role_code is embedded in JWT claims; must be fast to look up.
    # ------------------------------------------------------------------
    op.create_table(
        'roles',
        sa.Column('id',             sa.UUID(),       nullable=False),
        sa.Column('role_code',      sa.String(100),  nullable=False),
        sa.Column('role_name',      sa.String(255),  nullable=False),
        sa.Column('description',    sa.String(1000), nullable=True),
        sa.Column('is_system_role', sa.Boolean(),    nullable=False, server_default=sa.text('false')),
        sa.Column('created_at',     sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',     sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name='pk_roles'),
        sa.UniqueConstraint('role_code', name='uq_roles_role_code'),
    )
    op.create_index('ix_roles_role_code', 'roles', ['role_code'], unique=True)

    # ------------------------------------------------------------------
    # 4. permissions
    #    Fine-grained authorization grants assigned to roles.
    # ------------------------------------------------------------------
    op.create_table(
        'permissions',
        sa.Column('id',              sa.UUID(),       nullable=False),
        sa.Column('permission_code', sa.String(100),  nullable=False),
        sa.Column('permission_name', sa.String(255),  nullable=False),
        sa.Column('description',     sa.String(1000), nullable=True),
        sa.Column('created_at',      sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_permissions'),
        sa.UniqueConstraint('permission_code', name='uq_permissions_permission_code'),
    )
    op.create_index('ix_permissions_permission_code', 'permissions', ['permission_code'], unique=True)

    # ------------------------------------------------------------------
    # 5. identities
    #    Login credentials. Many-to-one with persons.
    #    email is globally unique (one email = one identity across all persons).
    #    password_hash nullable → supports OAuth/SSO identities with no password.
    #    identity_id appears in JWT claims.
    # ------------------------------------------------------------------
    op.create_table(
        'identities',
        sa.Column('id',            sa.UUID(),      nullable=False),
        sa.Column('person_id',     sa.UUID(),      nullable=False),
        sa.Column('email',         sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=True),
        sa.Column('identity_type', sa.String(50),  nullable=False, server_default=sa.text("'LOCAL'")),
        sa.Column('is_primary',    sa.Boolean(),   nullable=False, server_default=sa.text('true')),
        sa.Column('is_verified',   sa.Boolean(),   nullable=False, server_default=sa.text('false')),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at',    sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',    sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ['person_id'], ['persons.id'],
            name='fk_identities_person_id',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='pk_identities'),
        sa.UniqueConstraint('email', name='uq_identities_email'),
    )
    # Login lookup: auth service queries identities by email on every login
    op.create_index('ix_identities_email', 'identities', ['email'], unique=True)

    # ------------------------------------------------------------------
    # 6. role_permissions
    #    Junction: roles ↔ permissions.
    #    CASCADE on both FKs: deleting a role removes its grants.
    #    NOTE: permission FK uses CASCADE — see review note M-RLP-001.
    # ------------------------------------------------------------------
    op.create_table(
        'role_permissions',
        sa.Column('id',            sa.UUID(), nullable=False),
        sa.Column('role_id',       sa.UUID(), nullable=False),
        sa.Column('permission_id', sa.UUID(), nullable=False),
        sa.Column('created_at',    sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ['role_id'], ['roles.id'],
            name='fk_role_permissions_role_id',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['permission_id'], ['permissions.id'],
            name='fk_role_permissions_permission_id',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='pk_role_permissions'),
        sa.UniqueConstraint('role_id', 'permission_id', name='uq_role_permission'),
    )
    # Indexes to support "all permissions for role X" and "all roles with permission Y"
    op.create_index('ix_role_permissions_role_id',       'role_permissions', ['role_id'])
    op.create_index('ix_role_permissions_permission_id', 'role_permissions', ['permission_id'])

    # ------------------------------------------------------------------
    # 7. memberships
    #    Connects a Person to an Organization through a Role.
    #    uq_membership_person_organization enforces one active membership
    #    per (person, organization) pair — required for deterministic JWT
    #    membership_id resolution during login.
    #    CASCADE on person and organization FKs; RESTRICT on role FK
    #    (a role cannot be deleted while memberships reference it).
    # ------------------------------------------------------------------
    op.create_table(
        'memberships',
        sa.Column('id',                sa.UUID(),      nullable=False),
        sa.Column('person_id',         sa.UUID(),      nullable=False),
        sa.Column('organization_id',   sa.UUID(),      nullable=False),
        sa.Column('role_id',           sa.UUID(),      nullable=False),
        sa.Column('membership_status', sa.String(50),  nullable=False, server_default=sa.text("'ACTIVE'")),
        sa.Column('is_primary',        sa.Boolean(),   nullable=False, server_default=sa.text('false')),
        sa.Column('joined_at',         sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at',        sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',        sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ['person_id'], ['persons.id'],
            name='fk_memberships_person_id',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['organization_id'], ['organizations.id'],
            name='fk_memberships_organization_id',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['role_id'], ['roles.id'],
            name='fk_memberships_role_id',
            # No ondelete — PostgreSQL default RESTRICT prevents orphaning
        ),
        sa.PrimaryKeyConstraint('id', name='pk_memberships'),
        sa.UniqueConstraint(
            'person_id', 'organization_id',
            name='uq_membership_person_organization',
        ),
    )
    # Indexes to support "all memberships for person X" and "all members of org Y"
    op.create_index('ix_memberships_person_id',       'memberships', ['person_id'])
    op.create_index('ix_memberships_organization_id', 'memberships', ['organization_id'])

    # ------------------------------------------------------------------
    # 8. refresh_tokens
    #    Stores hashed refresh tokens for revocation and session management.
    #    token_hash is unique and indexed — every /auth/refresh hits this index.
    #    identity_id FK cascades so tokens are purged when an identity is deleted.
    # ------------------------------------------------------------------
    op.create_table(
        'refresh_tokens',
        sa.Column('id',          sa.UUID(),      nullable=False),
        sa.Column('identity_id', sa.UUID(),      nullable=False),
        sa.Column('token_hash',  sa.String(512), nullable=False),
        sa.Column('is_revoked',  sa.Boolean(),   nullable=False, server_default=sa.text('false')),
        sa.Column('expires_at',  sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at',  sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at',  sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ['identity_id'], ['identities.id'],
            name='fk_refresh_tokens_identity_id',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='pk_refresh_tokens'),
        sa.UniqueConstraint('token_hash', name='uq_refresh_tokens_token_hash'),
    )
    # identity_id index: "all tokens for this identity" (logout, revoke-all)
    op.create_index('ix_refresh_tokens_identity_id', 'refresh_tokens', ['identity_id'])
    # token_hash index: every /auth/refresh request looks up by hash
    op.create_index('ix_refresh_tokens_token_hash',  'refresh_tokens', ['token_hash'], unique=True)


def downgrade() -> None:
    # Drop in strict reverse dependency order to satisfy FK constraints.
    op.drop_index('ix_refresh_tokens_token_hash',  table_name='refresh_tokens')
    op.drop_index('ix_refresh_tokens_identity_id', table_name='refresh_tokens')
    op.drop_table('refresh_tokens')

    op.drop_index('ix_memberships_organization_id', table_name='memberships')
    op.drop_index('ix_memberships_person_id',        table_name='memberships')
    op.drop_table('memberships')

    op.drop_index('ix_role_permissions_permission_id', table_name='role_permissions')
    op.drop_index('ix_role_permissions_role_id',       table_name='role_permissions')
    op.drop_table('role_permissions')

    op.drop_index('ix_identities_email', table_name='identities')
    op.drop_table('identities')

    op.drop_index('ix_permissions_permission_code', table_name='permissions')
    op.drop_table('permissions')

    op.drop_index('ix_roles_role_code', table_name='roles')
    op.drop_table('roles')

    op.drop_table('persons')

    op.drop_index('ix_organizations_organization_code', table_name='organizations')
    op.drop_table('organizations')
