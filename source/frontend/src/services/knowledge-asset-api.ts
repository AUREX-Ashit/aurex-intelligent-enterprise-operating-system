/**
 * Knowledge Asset API wrapper — the only module permitted to call
 * AIService's `/knowledge-assets/*` endpoints. Mirrors AIService's
 * routers/knowledge_assets.py exactly (WP-14 BA-04, C-091). Every call
 * targets `appConfig.aiServiceUrl`, mirroring src/services/search-api.ts's
 * own established precedent for an AIService-hosted domain.
 */

import { apiClient } from "@/lib/api-client";
import { appConfig } from "@/lib/config";
import type { EstablishKnowledgeAssetRequest, KnowledgeAssetResponse } from "@/types/knowledge-asset";

const baseUrl = appConfig.aiServiceUrl;

export function establishKnowledgeAsset(
  request: EstablishKnowledgeAssetRequest,
): Promise<KnowledgeAssetResponse> {
  return apiClient.post<KnowledgeAssetResponse>("/knowledge-assets", request, { baseUrl });
}

export function getKnowledgeAsset(knowledgeAssetId: string): Promise<KnowledgeAssetResponse> {
  return apiClient.get<KnowledgeAssetResponse>(`/knowledge-assets/${knowledgeAssetId}`, { baseUrl });
}
