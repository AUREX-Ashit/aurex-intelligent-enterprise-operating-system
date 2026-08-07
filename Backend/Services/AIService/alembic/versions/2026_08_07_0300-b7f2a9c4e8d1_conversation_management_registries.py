"""conversation_management_registries

Revision ID: b7f2a9c4e8d1
Revises: d4a9c1e7f3b5
Create Date: 2026-08-07 03:00:00.000000

WP-12 — AI Conversation Management (C-094). Extends AIService's existing
Alembic chain (WP-11's `d4a9c1e7f3b5`) — does not bootstrap a second one,
per `IRA-012 §3`/`TDS-012 §4`. Introduces the physical realization of the
Business Object relationship `ADR-020` Clarifications 1-2 already decided:

- conversation_registry (BA-01): realizes the registered "AI Conversation"
  Business Object (CMD-001 §24.4).
- interaction_registry (BA-02 writes, BA-03 reads): decomposition element
  of conversation_registry, not independently registered.
- interaction_prompt_execution (BA-02): join table for the containment
  relationship ADR-020 Clarification 2 decided (one Interaction may invoke
  a Reasoning Engine more than once, RTA-001 §13.9b).

No column here is speculative — every field traces to a specific ADR-020
decision or ADR-022 principle, per TDS-012 §4's own schema proposal.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b7f2a9c4e8d1'
down_revision: Union[str, Sequence[str], None] = 'd4a9c1e7f3b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'conversation_registry',
        sa.Column('conversation_id', sa.Uuid(), nullable=False),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('established_by', sa.Uuid(), nullable=False),
        sa.Column('state', sa.String(10), nullable=False, server_default='OPEN'),
        sa.Column('state_transitioned_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('state_transition_reason', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("state IN ('OPEN', 'CLOSED')", name='ck_conversation_registry_state'),
        sa.CheckConstraint(
            "state_transition_reason IN ('EXPLICIT_ACTION', 'RUNTIME_POLICY') OR state_transition_reason IS NULL",
            name='ck_conversation_registry_state_transition_reason',
        ),
        sa.PrimaryKeyConstraint('conversation_id'),
    )
    op.create_index('ix_conversation_registry_organization_id', 'conversation_registry', ['organization_id'])

    op.create_table(
        'interaction_registry',
        sa.Column('interaction_id', sa.Uuid(), nullable=False),
        sa.Column('conversation_id', sa.Uuid(), nullable=False),
        sa.Column('sequence_number', sa.Integer(), nullable=False),
        sa.Column('business_activity_id', sa.Uuid(), nullable=False),
        sa.Column('status', sa.String(10), nullable=False, server_default='PENDING'),
        sa.Column('input_reference', sa.String(4000), nullable=False),
        sa.Column('output_reference', sa.String(8000), nullable=True),
        sa.Column('confidence_score', sa.Integer(), nullable=True),
        sa.Column('evidence_reference', sa.String(2000), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.CheckConstraint("status IN ('PENDING', 'COMPLETE', 'FAILED')", name='ck_interaction_registry_status'),
        sa.ForeignKeyConstraint(
            ['conversation_id'], ['conversation_registry.conversation_id'], ondelete='CASCADE'
        ),
        sa.UniqueConstraint(
            'conversation_id', 'sequence_number', name='uq_interaction_registry_conversation_sequence'
        ),
        sa.PrimaryKeyConstraint('interaction_id'),
    )
    op.create_index('ix_interaction_registry_conversation_id', 'interaction_registry', ['conversation_id'])
    op.create_index('ix_interaction_registry_organization_id', 'interaction_registry', ['organization_id'])

    op.create_table(
        'interaction_prompt_execution',
        sa.Column('interaction_id', sa.Uuid(), nullable=False),
        sa.Column('prompt_execution_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ['interaction_id'], ['interaction_registry.interaction_id'], ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('interaction_id', 'prompt_execution_id'),
    )


def downgrade() -> None:
    op.drop_table('interaction_prompt_execution')

    op.drop_index('ix_interaction_registry_organization_id', table_name='interaction_registry')
    op.drop_index('ix_interaction_registry_conversation_id', table_name='interaction_registry')
    op.drop_table('interaction_registry')

    op.drop_index('ix_conversation_registry_organization_id', table_name='conversation_registry')
    op.drop_table('conversation_registry')
