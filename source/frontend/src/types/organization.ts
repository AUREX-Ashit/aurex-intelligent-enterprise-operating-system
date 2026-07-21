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
