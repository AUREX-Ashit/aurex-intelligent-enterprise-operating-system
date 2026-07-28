"""authorization_policy_object_deprecate_retire

Revision ID: c3e9a5f7b2d4
Revises: b7d4f2a8e1c6
Create Date: 2026-07-30 09:00:00.000000

WP-02 BA-08 — Deprecate or Retire Authorization Policy Object
(ERB-C003-02 / EX-C003-08 per PE-001-C003). Widens the `status`
CHECK constraint BA-07 introduced on all five WP-02 authorization
policy objects (roles, domain_permissions, approval_authorities,
delegation_policies, runtime_assignment_policies) to admit two further
values realizing URA-001-127's Hide/Archive distinction: DEPRECATED
(Hidden) and RETIRED (Archived) — no new column, no new table. Mirrors
WP-01's own precedent exactly: Organization's `ck_organizations_status`
CHECK constraint was widened the same way, in the same shape, to add
RETIRED at its own BA-07 (migration d2d840d224b6).

Purely additive to the constraint's own value set: no existing row's
status changes, since every existing row is already ACTIVE or
SUPERSEDED, both of which remain valid.
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c3e9a5f7b2d4'
down_revision: Union[str, Sequence[str], None] = 'b7d4f2a8e1c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_STATUS_CONSTRAINTS = [
    ("roles", "ck_roles_status"),
    ("domain_permissions", "ck_domain_permissions_status"),
    ("approval_authorities", "ck_approval_authorities_status"),
    ("delegation_policies", "ck_delegation_policies_status"),
    ("runtime_assignment_policies", "ck_runtime_assignment_policies_status"),
]


def upgrade() -> None:
    for table_name, constraint_name in _STATUS_CONSTRAINTS:
        op.drop_constraint(constraint_name, table_name, type_='check')
        op.create_check_constraint(
            constraint_name, table_name,
            "status IN ('ACTIVE', 'SUPERSEDED', 'DEPRECATED', 'RETIRED')",
        )


def downgrade() -> None:
    for table_name, constraint_name in reversed(_STATUS_CONSTRAINTS):
        op.drop_constraint(constraint_name, table_name, type_='check')
        op.create_check_constraint(
            constraint_name, table_name,
            "status IN ('ACTIVE', 'SUPERSEDED')",
        )
