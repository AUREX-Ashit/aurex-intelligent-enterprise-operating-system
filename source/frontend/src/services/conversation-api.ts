/**
 * AI Conversation Management API wrapper — the only module permitted to
 * call AIService's `/conversations/*` endpoints. Mirrors AIService's
 * routers/conversation.py exactly (WP-12 BA-01/02/03, C-094). Every call
 * targets `appConfig.aiServiceUrl`, not AuthService's own default base URL,
 * mirroring `search-api.ts`'s own precedent (WP-11).
 */

import { apiClient } from "@/lib/api-client";
import { appConfig } from "@/lib/config";
import type {
  ConversationResponse,
  ExecuteInteractionRequest,
  InteractionListResponse,
  InteractionResponse,
} from "@/types/conversation";

const baseUrl = appConfig.aiServiceUrl;

export function establishConversation(): Promise<ConversationResponse> {
  return apiClient.post<ConversationResponse>("/conversations", undefined, { baseUrl });
}

export function closeConversation(conversationId: string): Promise<ConversationResponse> {
  return apiClient.post<ConversationResponse>(`/conversations/${conversationId}/close`, undefined, { baseUrl });
}

export function executeInteraction(
  conversationId: string,
  request: ExecuteInteractionRequest,
): Promise<InteractionResponse> {
  return apiClient.post<InteractionResponse>(`/conversations/${conversationId}/interactions`, request, { baseUrl });
}

export function listInteractions(conversationId: string): Promise<InteractionListResponse> {
  return apiClient.get<InteractionListResponse>(`/conversations/${conversationId}/interactions`, { baseUrl });
}
