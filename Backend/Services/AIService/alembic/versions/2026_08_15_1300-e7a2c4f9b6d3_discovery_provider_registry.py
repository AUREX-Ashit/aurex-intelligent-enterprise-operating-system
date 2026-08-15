"""discovery_provider_registry

Revision ID: e7a2c4f9b6d3
Revises: c3f8e1a9d2b6
Create Date: 2026-08-15 13:00:00.000000

WP-14 BA-01 — Establish Discovery Provider Configuration (C-090 Enterprise
Discovery). Extends AIService's existing Alembic chain (WP-14 BA-04's own
`c3f8e1a9d2b6`) — does not bootstrap a second one. Introduces the single
canonical, LOCKED table `Master_Technical_Architecture.md` AMD-013
specifies for this Business Activity (`discovery_provider_registry`, line
3301) — no column added, removed, or retyped beyond that specification.

Does not create `api_credential_registry` or `confidence_scoring_registry`
— both remain unimplemented anywhere in this repository (same disposition
BA-04's own migration `c3f8e1a9d2b6` already found for
`confidence_scoring_registry`); `credential_id`/`governing_policy_id` are
declared nullable, no FK.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e7a2c4f9b6d3'
down_revision: Union[str, Sequence[str], None] = 'c3f8e1a9d2b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'discovery_provider_registry',
        sa.Column('discovery_provider_id', sa.Uuid(), nullable=False),
        sa.Column('provider_name', sa.String(255), nullable=True),
        sa.Column('provider_category', sa.String(50), nullable=False),
        sa.Column('provider_type', sa.String(100), nullable=False),
        sa.Column('connection_config_json', sa.JSON(), nullable=True),
        sa.Column('credential_id', sa.Uuid(), nullable=True),
        sa.Column('discovery_cadence', sa.String(50), nullable=False, server_default='ON_DEMAND'),
        sa.Column('governing_policy_id', sa.Uuid(), nullable=True),
        sa.Column('active_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=True),
        sa.CheckConstraint(
            "provider_category IN ('ENTERPRISE', 'EXTERNAL', 'REALTIME')",
            name='ck_discovery_provider_registry_provider_category',
        ),
        sa.CheckConstraint(
            "provider_type IN ("
            "'UPLOADED_DOCUMENT', 'SHAREPOINT', 'ONEDRIVE', 'GOOGLE_DRIVE', 'TEAMS', 'SLACK', 'CONFLUENCE', "
            "'JIRA', 'SAP', 'ORACLE', 'SALESFORCE', 'SERVICENOW', 'SQL_DATABASE', 'DATA_WAREHOUSE', 'ENTERPRISE_API', "
            "'CORPORATE_WEBSITE', 'ANNUAL_REPORT', 'SUSTAINABILITY_REPORT', 'REGULATORY_FILING', "
            "'GOVERNMENT_DATABASE', 'STOCK_EXCHANGE_FILING', 'STANDARDS_BODY', 'PUBLIC_API', 'INTERNET_SEARCH', "
            "'BENCHMARK_PROVIDER', 'INDUSTRY_DATABASE', "
            "'EMAIL', 'EVENT_STREAM', 'IOT', 'SENSOR', 'MESSAGE_QUEUE'"
            ")",
            name='ck_discovery_provider_registry_provider_type',
        ),
        sa.CheckConstraint(
            "discovery_cadence IN ('CONTINUOUS', 'SCHEDULED', 'ON_DEMAND')",
            name='ck_discovery_provider_registry_discovery_cadence',
        ),
        sa.PrimaryKeyConstraint('discovery_provider_id'),
    )
    op.create_index(
        op.f('ix_discovery_provider_registry_organization_id'),
        'discovery_provider_registry',
        ['organization_id'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_discovery_provider_registry_organization_id'), table_name='discovery_provider_registry')
    op.drop_table('discovery_provider_registry')
