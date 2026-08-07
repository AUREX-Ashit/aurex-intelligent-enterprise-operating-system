/**
 * Mirrors AIService's schemas/conversation.py exactly (WP-12 BA-01/02/03,
 * C-094). No field added, renamed, or omitted relative to the backend
 * contract.
 */

export interface ConversationResponse {
  conversation_id: string;
  state: string;
  state_transitioned_at: string;
  state_transition_reason: string | null;
  created_at: string;
  closed_at: string | null;
}

export interface ExecuteInteractionRequest {
  input_text: string;
  business_activity_id?: string | null;
}

export interface InteractionResponse {
  interaction_id: string;
  conversation_id: string;
  sequence_number: number;
  status: string;
  input_reference: string;
  output_reference: string | null;
  confidence_score: number | null;
  evidence_reference: string | null;
  created_at: string;
  completed_at: string | null;
}

export interface InteractionListResponse {
  interactions: InteractionResponse[];
}
