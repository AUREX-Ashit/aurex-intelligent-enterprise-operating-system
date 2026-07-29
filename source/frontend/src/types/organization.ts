/**
 * Mirrors AuthService's schemas/organization.py exactly. No field added,
 * renamed, or omitted relative to the backend contract (WP-01, Establish
 * Organization).
 */

export interface EstablishOrganizationRequest {
  organization_code: string;
  organization_name: string;
  organization_type: string;
  description?: string | null;
}

/**
 * IRA-001A (backend constitutional correction, TD-049): Establish Organization
 * is now a two-step flow — POST /organization-establishment-attempts, then
 * POST .../activate. This type mirrors AuthService's
 * OrganizationEstablishmentAttemptResponse and is consumed only internally
 * by services/organization-api.ts's establishOrganization(), which still
 * returns Promise<OrganizationResponse> to every existing caller — no other
 * frontend file needs to know this intermediate step exists.
 */
export interface OrganizationEstablishmentAttemptResponse {
  id: string;
  organization_code: string;
  organization_name: string;
  organization_type: string;
  description: string | null;
  primary_domain: string | null;
  domain_verification_status: "NOT_CLAIMED" | "UNVERIFIED" | "VERIFIED";
  activated_organization_id: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface UpdateOrganizationProfileRequest {
  organization_name: string;
  organization_type: string;
  description?: string | null;
}

export type OrganizationStatus = "ACTIVE" | "SUSPENDED";

export interface OrganizationResponse {
  id: string;
  organization_code: string;
  organization_name: string;
  organization_type: string;
  description: string | null;
  status: OrganizationStatus;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

export type OrganizationSortField = "organization_name" | "organization_code" | "created_at";
export type SortOrder = "asc" | "desc";

export interface SearchOrganizationsParams {
  q?: string;
  status?: OrganizationStatus;
  skip?: number;
  limit?: number;
  sort_by?: OrganizationSortField;
  sort_order?: SortOrder;
}

export interface OrganizationListResponse {
  items: OrganizationResponse[];
  total: number;
  skip: number;
  limit: number;
}
