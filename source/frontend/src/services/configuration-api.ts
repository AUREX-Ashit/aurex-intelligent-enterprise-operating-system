/**
 * Configuration API wrapper — the only module permitted to call
 * GET /configuration, GET /configuration/entries, and POST /configuration.
 * Mirrors AuthService's routers/configuration.py exactly (WP-10 BA-01/02,
 * EX-C041-01/02).
 */

import { apiClient } from "@/lib/api-client";
import type {
  ConfigurationEntryListResponse,
  ConfigurationEntryResponse,
  EstablishConfigurationEntryRequest,
  ResolvedConfigurationBundle,
} from "@/types/configuration";

export function resolveConfiguration(facets?: string[]): Promise<ResolvedConfigurationBundle> {
  const query = facets && facets.length > 0 ? `?${facets.map((f) => `facet=${encodeURIComponent(f)}`).join("&")}` : "";
  return apiClient.get<ResolvedConfigurationBundle>(`/configuration${query}`);
}

export function establishConfiguration(
  request: EstablishConfigurationEntryRequest,
): Promise<ConfigurationEntryResponse> {
  return apiClient.post<ConfigurationEntryResponse>("/configuration", request);
}

export function listConfigurationEntries(): Promise<ConfigurationEntryListResponse> {
  return apiClient.get<ConfigurationEntryListResponse>("/configuration/entries");
}
