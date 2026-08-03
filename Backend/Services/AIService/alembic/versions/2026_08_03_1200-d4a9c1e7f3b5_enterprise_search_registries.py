"""enterprise_search_registries

Revision ID: d4a9c1e7f3b5
Revises:
Create Date: 2026-08-03 12:00:00.000000

WP-11 — Enterprise Search (C-093). First-ever migration in AIService's
own Alembic chain (`IRA-011 §4.5`, prerequisite bootstrapped as part of
BA-01). Introduces the three canonical, LOCKED tables `Master_Technical_
Architecture.md` AMD-012 specifies for the "Retrieval Service" component
boundary — no column added, removed, or retyped beyond that
specification.

- vector_index_registry (BA-01): one row per configured search index.
- evidence_registry (BA-03): one row per registered source
  document/passage.
- document_chunk_registry (BA-03 writes, BA-02 reads): the chunked unit
  a Vector Database entry corresponds to.

Does not touch `rag_configs` (`RAGConfigModel`) — retained, unmigrated,
per `TD-109`'s own "no runtime data affected" disclosure; superseded in
code, not dropped from the database, by this Work Package.

Pre-existing AIService models (ESGExtractionModel, ESGValidationModel,
ESGScoringModel) are also not part of this migration — they predate
Alembic in this service and remain schema-managed via
`models.database.init_db()`'s own `Base.metadata.create_all()` at
startup, unaffected by this migration's own, separate scope
(`IRA-011 §4.5`: this bootstrap is scoped to WP-11's own three new
tables only, not a retrofit of every pre-existing model).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd4a9c1e7f3b5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'vector_index_registry',
        sa.Column('vector_index_id', sa.Uuid(), nullable=False),
        sa.Column('index_name', sa.String(255), nullable=False),
        sa.Column('embedding_model', sa.String(255), nullable=False),
        sa.Column('embedding_dimension', sa.Integer(), nullable=False),
        sa.Column('retrieval_mode', sa.String(50), nullable=False, server_default='HYBRID'),
        sa.Column('refresh_cadence', sa.String(255), nullable=True),
        sa.Column('active_flag', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=True),
        sa.CheckConstraint(
            "retrieval_mode IN ('SEMANTIC', 'LEXICAL', 'HYBRID')",
            name='ck_vector_index_registry_retrieval_mode',
        ),
        sa.PrimaryKeyConstraint('vector_index_id'),
    )
    op.create_index(
        'ix_vector_index_registry_organization_id', 'vector_index_registry', ['organization_id']
    )

    op.create_table(
        'evidence_registry',
        sa.Column('evidence_id', sa.Uuid(), nullable=False),
        sa.Column('evidence_type', sa.String(255), nullable=True),
        sa.Column('linked_entity_type', sa.String(255), nullable=True),
        sa.Column('linked_entity_id', sa.Uuid(), nullable=True),
        sa.Column('evidence_source', sa.String(255), nullable=True),
        sa.Column('file_reference', sa.String(255), nullable=True),
        sa.Column('source_timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.Column('confidence_score', sa.Integer(), nullable=True),
        sa.Column('externally_verified_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('legal_defensibility_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('retention_policy', sa.String(255), nullable=True),
        sa.Column('document_hash_signature', sa.String(255), nullable=True),
        sa.Column('ai_extracted_flag', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('active_flag', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('confidence_rule_id', sa.Uuid(), nullable=True),
        sa.PrimaryKeyConstraint('evidence_id'),
    )
    op.create_index('ix_evidence_registry_organization_id', 'evidence_registry', ['organization_id'])

    op.create_table(
        'document_chunk_registry',
        sa.Column('document_chunk_id', sa.Uuid(), nullable=False),
        sa.Column('evidence_id', sa.Uuid(), nullable=False),
        sa.Column('chunk_sequence_number', sa.Integer(), nullable=True),
        sa.Column('chunk_locator', sa.String(255), nullable=True),
        sa.Column('chunk_text_hash', sa.String(255), nullable=True),
        sa.Column('vector_index_id', sa.Uuid(), nullable=True),
        sa.Column('embedding_reference', sa.String(255), nullable=True),
        sa.Column('embedding_model_version', sa.String(255), nullable=True),
        sa.Column('active_flag', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['evidence_id'], ['evidence_registry.evidence_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['vector_index_id'], ['vector_index_registry.vector_index_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('document_chunk_id'),
    )
    op.create_index('ix_document_chunk_registry_evidence_id', 'document_chunk_registry', ['evidence_id'])
    op.create_index('ix_document_chunk_registry_vector_index_id', 'document_chunk_registry', ['vector_index_id'])
    op.create_index('ix_document_chunk_registry_organization_id', 'document_chunk_registry', ['organization_id'])


def downgrade() -> None:
    op.drop_index('ix_document_chunk_registry_organization_id', table_name='document_chunk_registry')
    op.drop_index('ix_document_chunk_registry_vector_index_id', table_name='document_chunk_registry')
    op.drop_index('ix_document_chunk_registry_evidence_id', table_name='document_chunk_registry')
    op.drop_table('document_chunk_registry')

    op.drop_index('ix_evidence_registry_organization_id', table_name='evidence_registry')
    op.drop_table('evidence_registry')

    op.drop_index('ix_vector_index_registry_organization_id', table_name='vector_index_registry')
    op.drop_table('vector_index_registry')
