"""
WP-00 Platform Bootstrap — canonical seed data.

Single source of truth for the deterministic seed data previously encoded
only as raw SQL in scripts/03_seed_r001_data.sql, scripts/05_bootstrap_first_user.sql,
and scripts/07_bootstrap_platform_admin.sql. Those three files remain in the
repository unchanged, as the original, manually-runnable reference this data
was extracted from — this module does not duplicate their logic, only their
already-approved data values, so that bootstrap_service.py can apply them
idempotently through the same SQLAlchemy ORM models the rest of AuthService
already uses (Reuse before Create — see Backend/Services/AuthService/models).

All UUIDs are the exact deterministic (uuid5) values already documented in
the SQL scripts' own header comments. Do not regenerate them — doing so
would create duplicate rows alongside any environment previously bootstrapped
via the SQL path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True)
class RoleSeed:
    id: UUID
    role_code: str
    role_name: str
    description: str
    is_system_role: bool


@dataclass(frozen=True)
class PermissionSeed:
    id: UUID
    permission_code: str
    permission_name: str
    description: str


@dataclass(frozen=True)
class PersonSeed:
    id: UUID
    first_name: str
    last_name: str
    display_name: str


@dataclass(frozen=True)
class IdentitySeed:
    id: UUID
    person_id: UUID
    email: str
    password_hash: str
    identity_type: str = "LOCAL"
    is_primary: bool = True
    is_verified: bool = True


@dataclass(frozen=True)
class OrganizationSeed:
    id: UUID
    organization_code: str
    organization_name: str
    organization_type: str


@dataclass(frozen=True)
class MembershipSeed:
    id: UUID
    person_id: UUID
    organization_id: UUID
    role_id: UUID
    membership_status: str = "ACTIVE"
    is_primary: bool = True


# ---------------------------------------------------------------------------
# BLOCK A — Roles (source: 03_seed_r001_data.sql)
# ---------------------------------------------------------------------------

ROLES: list[RoleSeed] = [
    RoleSeed(
        id=UUID("9524d250-fe5e-5334-845b-18d547a5b59c"),
        role_code="PLATFORM_ADMIN",
        role_name="Platform Administrator",
        description=(
            "CorpStage platform operator. Manages all organizations, system "
            "configuration, and platform-level settings. Operates across all "
            "organization boundaries."
        ),
        is_system_role=True,
    ),
    RoleSeed(
        id=UUID("c0d893dd-834a-539a-b0b9-cea32d756c9e"),
        role_code="ORG_ADMIN",
        role_name="Organization Administrator",
        description=(
            "Full operational control within a single organization. Manages "
            "members, workspaces, documents, and license allocation."
        ),
        is_system_role=False,
    ),
    RoleSeed(
        id=UUID("2b3bda96-a1d2-55ae-8cc5-09653a6c795e"),
        role_code="ESG_MANAGER",
        role_name="ESG Manager",
        description=(
            "Manages the organization ESG program. Validates sustainability "
            "data, compiles reports, oversees data quality, and runs AI "
            "extraction workflows."
        ),
        is_system_role=False,
    ),
    RoleSeed(
        id=UUID("39a005f5-418a-5b1c-b011-2120aa4b1b87"),
        role_code="AUDITOR",
        role_name="Auditor",
        description=(
            "External read-only audit specialist. Verifies documentation, "
            "metrics, and evidence trails. No write access to any data."
        ),
        is_system_role=False,
    ),
    RoleSeed(
        id=UUID("439b0997-aee6-57ec-b6a1-a9aa799dcfbb"),
        role_code="SUPPLIER_ADMIN",
        role_name="Supplier Administrator",
        description=(
            "Supplier organization representative. Uploads evidence and "
            "manages documents on behalf of the supplier. No access to "
            "internal ESG metrics or reports."
        ),
        is_system_role=False,
    ),
    RoleSeed(
        id=UUID("f401a452-c1ab-5df0-82fb-68ae7f8b9290"),
        role_code="BOARD_MEMBER",
        role_name="Board Member",
        description=(
            "Executive-level read access to dashboards, ESG scores, and "
            "reports. No operational or data entry access."
        ),
        is_system_role=False,
    ),
]

# ---------------------------------------------------------------------------
# BLOCK B — Permissions (source: 03_seed_r001_data.sql)
# ---------------------------------------------------------------------------

PERMISSIONS: list[PermissionSeed] = [
    PermissionSeed(UUID("2e02360a-7a9c-5790-a980-0f4351e3a0ab"), "DOCUMENT_READ", "Read Documents", "View uploaded documents and their metadata."),
    PermissionSeed(UUID("06f4f2f3-94a3-5e23-b23f-cbb048f9a46a"), "DOCUMENT_WRITE", "Write Documents", "Upload, update, and manage documents in evidence storage."),
    PermissionSeed(UUID("688d3f58-f57d-5cd6-8c7d-de663fecd267"), "METRIC_READ", "Read Metrics", "Read ESG metrics, sustainability data values, and historical records."),
    PermissionSeed(UUID("f94017b0-8f30-5798-9281-823bc4c54536"), "METRIC_EDIT", "Edit Metrics", "Create and modify metric values and sustainability data entries."),
    PermissionSeed(UUID("2a4f927d-6e37-558a-95b5-9ddea411a6da"), "REPORT_READ", "Read Reports", "View ESG reports, analytics, and draft disclosure documents."),
    PermissionSeed(UUID("52dbd32c-7b47-56ab-8726-292ba442d879"), "REPORT_EXPORT", "Export Reports", "Sign off and export finalized ESG disclosure documents."),
    PermissionSeed(UUID("896a1d45-249b-5611-9813-715860a4a29d"), "SCORE_VIEW", "View Scores", "View computed ESG scores and assessment ratings."),
    PermissionSeed(UUID("b54d3558-195d-5596-a6b5-c66a863fbe15"), "ORG_READ", "Read Organization", "Read organization settings, configuration, and member directory."),
    PermissionSeed(UUID("ae67473a-990b-5d14-a5af-8e6fad3540ec"), "ORG_WRITE", "Write Organization", "Modify organization settings, configuration, and manage members."),
    PermissionSeed(UUID("d4705417-3fc1-5044-916f-e57ae9b8c1c7"), "USER_READ", "Read Users", "View user directory and account details."),
    PermissionSeed(UUID("dc2e1856-cee9-5cd6-971c-2f0d0d82ddca"), "USER_WRITE", "Write Users", "Create, update, and deactivate user accounts and credentials."),
    PermissionSeed(UUID("09ee8ea0-173c-5a33-9e4d-22de6b6244c6"), "AI_EXTRACT", "Run AI Extraction", "Invoke AI extraction pipelines on uploaded documents to discover sustainability data."),
]

_ALL_PERMISSION_IDS = [p.id for p in PERMISSIONS]
_DOC_RW = [UUID("2e02360a-7a9c-5790-a980-0f4351e3a0ab"), UUID("06f4f2f3-94a3-5e23-b23f-cbb048f9a46a")]

# ---------------------------------------------------------------------------
# BLOCK C — Role-Permission Matrix (source: 03_seed_r001_data.sql, 42 rows)
# ---------------------------------------------------------------------------

ROLE_PERMISSIONS: dict[UUID, list[UUID]] = {
    UUID("9524d250-fe5e-5334-845b-18d547a5b59c"): list(_ALL_PERMISSION_IDS),  # PLATFORM_ADMIN — all 12
    UUID("c0d893dd-834a-539a-b0b9-cea32d756c9e"): list(_ALL_PERMISSION_IDS),  # ORG_ADMIN — all 12
    UUID("2b3bda96-a1d2-55ae-8cc5-09653a6c795e"): [  # ESG_MANAGER — 8
        UUID("2e02360a-7a9c-5790-a980-0f4351e3a0ab"), UUID("06f4f2f3-94a3-5e23-b23f-cbb048f9a46a"),
        UUID("688d3f58-f57d-5cd6-8c7d-de663fecd267"), UUID("f94017b0-8f30-5798-9281-823bc4c54536"),
        UUID("2a4f927d-6e37-558a-95b5-9ddea411a6da"), UUID("52dbd32c-7b47-56ab-8726-292ba442d879"),
        UUID("896a1d45-249b-5611-9813-715860a4a29d"), UUID("09ee8ea0-173c-5a33-9e4d-22de6b6244c6"),
    ],
    UUID("39a005f5-418a-5b1c-b011-2120aa4b1b87"): [  # AUDITOR — 4
        UUID("2e02360a-7a9c-5790-a980-0f4351e3a0ab"), UUID("688d3f58-f57d-5cd6-8c7d-de663fecd267"),
        UUID("2a4f927d-6e37-558a-95b5-9ddea411a6da"), UUID("896a1d45-249b-5611-9813-715860a4a29d"),
    ],
    UUID("439b0997-aee6-57ec-b6a1-a9aa799dcfbb"): list(_DOC_RW),  # SUPPLIER_ADMIN — 2
    UUID("f401a452-c1ab-5df0-82fb-68ae7f8b9290"): [  # BOARD_MEMBER — 4
        UUID("688d3f58-f57d-5cd6-8c7d-de663fecd267"), UUID("2a4f927d-6e37-558a-95b5-9ddea411a6da"),
        UUID("52dbd32c-7b47-56ab-8726-292ba442d879"), UUID("896a1d45-249b-5611-9813-715860a4a29d"),
    ],
}

# ---------------------------------------------------------------------------
# Demo Organization + Org Admin (source: 05_bootstrap_first_user.sql)
# ---------------------------------------------------------------------------

DEMO_ORGANIZATION = OrganizationSeed(
    id=UUID("5466c6bf-67b2-52ac-ba83-a8cff7b8b42e"),
    organization_code="CORP-DEMO-001",
    organization_name="CorpStage Demo Organization",
    organization_type="CORPORATE",
)

DEMO_ADMIN_PERSON = PersonSeed(
    id=UUID("5385aa88-1e34-57fa-8c0c-fef655ca3773"),
    first_name="Admin",
    last_name="User",
    display_name="Admin User",
)

DEMO_ADMIN_IDENTITY = IdentitySeed(
    id=UUID("69a5c359-8a90-5274-9835-c0636e415873"),
    person_id=DEMO_ADMIN_PERSON.id,
    email="admin@corpstage.com",
    # bcrypt cost-12 hash of CorpStage#Admin2026! — pre-computed and verified
    # round-trip in the original 05_bootstrap_first_user.sql; reused verbatim.
    password_hash="$2b$12$BhF.jMSngAwyXAmmREe6BeB53viDBigLvJ7j76pyWHCpq/CvZd7AK",
)

DEMO_ADMIN_MEMBERSHIP = MembershipSeed(
    id=UUID("53a0068c-fcc1-5aca-88f2-b19422ab3fd2"),
    person_id=DEMO_ADMIN_PERSON.id,
    organization_id=DEMO_ORGANIZATION.id,
    role_id=UUID("c0d893dd-834a-539a-b0b9-cea32d756c9e"),  # ORG_ADMIN
)

# ---------------------------------------------------------------------------
# Platform Administrator (source: 07_bootstrap_platform_admin.sql)
# Reuses DEMO_ORGANIZATION — PLATFORM_ADMIN operates across every
# organization boundary and does not require an Organization of its own.
# ---------------------------------------------------------------------------

PLATFORM_ADMIN_PERSON = PersonSeed(
    id=UUID("1ac94f77-f5fc-5ce9-9c4e-1d01d59ed6b2"),
    first_name="Platform",
    last_name="Admin",
    display_name="Platform Admin User",
)

PLATFORM_ADMIN_IDENTITY = IdentitySeed(
    id=UUID("4663ad18-6b14-5dd1-84c0-dbce51714d5f"),
    person_id=PLATFORM_ADMIN_PERSON.id,
    email="platform.admin@corpstage.com",
    # bcrypt cost-12 hash of CorpStage#PlatformAdmin2026! — pre-computed and
    # verified round-trip in the original 07_bootstrap_platform_admin.sql.
    password_hash="$2b$12$IGo4i.zyAUgt2lyGul.LauAUOD1.6F.1LZfhtyrPYV/LKd1Jp4BCC",
)

PLATFORM_ADMIN_MEMBERSHIP = MembershipSeed(
    id=UUID("231190bc-dc3f-58d3-88c3-a4832ca62c89"),
    person_id=PLATFORM_ADMIN_PERSON.id,
    organization_id=DEMO_ORGANIZATION.id,
    role_id=UUID("9524d250-fe5e-5334-845b-18d547a5b59c"),  # PLATFORM_ADMIN
)
