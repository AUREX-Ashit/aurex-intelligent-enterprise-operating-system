/**
 * Mirrors AuthService's schemas/configuration.py exactly (WP-10 BA-01/02,
 * EX-C041-01/02). No field added, renamed, or omitted relative to the
 * backend contract.
 */

export type ConfigurationFacet = "TERMINOLOGY" | "BRANDING" | "THEME" | "ACCESSIBILITY" | "LOCALIZATION";

export type ConfigurationSource = "USER" | "TENANT" | "PLATFORM_DEFAULT";

export interface ResolvedConfigurationValue {
  key: string;
  value: unknown;
  source: ConfigurationSource;
  version: number | null;
}

export interface ResolvedConfigurationBundle {
  organization_id: string;
  facets: Record<string, ResolvedConfigurationValue[]>;
  resolved_at: string;
}

export interface EstablishConfigurationEntryRequest {
  facet: ConfigurationFacet;
  key: string;
  value: unknown;
}

export interface ConfigurationEntryResponse {
  id: string;
  organization_id: string;
  scope_level: string;
  facet: string;
  key: string;
  value: unknown;
  version: number;
  lifecycle_state: string;
  effective_from: string;
  established_by_person_id: string | null;
}

export interface ConfigurationEntryListResponse {
  entries: ConfigurationEntryResponse[];
}
