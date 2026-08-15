/**
 * Mirrors AIService's schemas/discovery_provider.py exactly (WP-14 BA-01,
 * C-090). No field added, renamed, or omitted relative to the backend
 * contract.
 */

export type ProviderCategory = "ENTERPRISE" | "EXTERNAL" | "REALTIME";

export const PROVIDER_TYPES_BY_CATEGORY: Record<ProviderCategory, string[]> = {
  ENTERPRISE: [
    "UPLOADED_DOCUMENT", "SHAREPOINT", "ONEDRIVE", "GOOGLE_DRIVE", "TEAMS", "SLACK", "CONFLUENCE",
    "JIRA", "SAP", "ORACLE", "SALESFORCE", "SERVICENOW", "SQL_DATABASE", "DATA_WAREHOUSE", "ENTERPRISE_API",
  ],
  EXTERNAL: [
    "CORPORATE_WEBSITE", "ANNUAL_REPORT", "SUSTAINABILITY_REPORT", "REGULATORY_FILING",
    "GOVERNMENT_DATABASE", "STOCK_EXCHANGE_FILING", "STANDARDS_BODY", "PUBLIC_API", "INTERNET_SEARCH",
    "BENCHMARK_PROVIDER", "INDUSTRY_DATABASE",
  ],
  REALTIME: ["EMAIL", "EVENT_STREAM", "IOT", "SENSOR", "MESSAGE_QUEUE"],
};

export const DISCOVERY_CADENCES = ["CONTINUOUS", "SCHEDULED", "ON_DEMAND"] as const;

export interface EstablishDiscoveryProviderRequest {
  provider_name?: string | null;
  provider_category: ProviderCategory;
  provider_type: string;
  connection_config_json?: Record<string, unknown> | null;
  credential_id?: string | null;
  discovery_cadence: (typeof DISCOVERY_CADENCES)[number];
  governing_policy_id?: string | null;
  platform_wide: boolean;
}

export interface DiscoveryProviderResponse {
  discovery_provider_id: string;
  provider_name: string | null;
  provider_category: ProviderCategory;
  provider_type: string;
  connection_config_json: Record<string, unknown> | null;
  credential_id: string | null;
  discovery_cadence: string;
  governing_policy_id: string | null;
  active_flag: boolean;
  organization_id: string | null;
  created_at: string;
}

export interface DiscoveryProviderListResponse {
  discovery_providers: DiscoveryProviderResponse[];
}
