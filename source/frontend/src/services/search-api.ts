/**
 * Enterprise Search API wrapper — the only module permitted to call
 * AIService's `/search/*` endpoints. Mirrors AIService's routers/search.py
 * exactly (WP-11 BA-01/02/03, C-093). Every call targets
 * `appConfig.aiServiceUrl`, not AuthService's own default base URL.
 */

import { apiClient } from "@/lib/api-client";
import { appConfig } from "@/lib/config";
import type {
  EstablishIndexConfigurationRequest,
  ExecuteSearchRequest,
  IndexConfigurationListResponse,
  IndexConfigurationResponse,
  RegisterContentRequest,
  RegisteredContentResponse,
  SearchResponse,
} from "@/types/search";

const baseUrl = appConfig.aiServiceUrl;

export function establishIndexConfiguration(
  request: EstablishIndexConfigurationRequest,
): Promise<IndexConfigurationResponse> {
  return apiClient.post<IndexConfigurationResponse>("/search/index-configurations", request, { baseUrl });
}

export function listIndexConfigurations(): Promise<IndexConfigurationListResponse> {
  return apiClient.get<IndexConfigurationListResponse>("/search/index-configurations", { baseUrl });
}

export function registerSearchContent(request: RegisterContentRequest): Promise<RegisteredContentResponse> {
  return apiClient.post<RegisteredContentResponse>("/search/content", request, { baseUrl });
}

export function executeSearch(request: ExecuteSearchRequest): Promise<SearchResponse> {
  return apiClient.post<SearchResponse>("/search/query", request, { baseUrl });
}
