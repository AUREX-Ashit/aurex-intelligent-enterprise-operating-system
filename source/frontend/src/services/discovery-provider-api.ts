/**
 * Discovery Provider API wrapper — the only module permitted to call
 * AIService's `/discovery-providers/*` endpoints. Mirrors AIService's
 * routers/discovery_providers.py exactly (WP-14 BA-01, C-090). Every call
 * targets `appConfig.aiServiceUrl`, mirroring src/services/search-api.ts's
 * own established precedent for an AIService-hosted domain.
 */

import { apiClient } from "@/lib/api-client";
import { appConfig } from "@/lib/config";
import type {
  DiscoveryProviderListResponse,
  DiscoveryProviderResponse,
  EstablishDiscoveryProviderRequest,
} from "@/types/discovery-provider";

const baseUrl = appConfig.aiServiceUrl;

export function establishDiscoveryProvider(
  request: EstablishDiscoveryProviderRequest,
): Promise<DiscoveryProviderResponse> {
  return apiClient.post<DiscoveryProviderResponse>("/discovery-providers", request, { baseUrl });
}

export function listDiscoveryProviders(): Promise<DiscoveryProviderListResponse> {
  return apiClient.get<DiscoveryProviderListResponse>("/discovery-providers", { baseUrl });
}
