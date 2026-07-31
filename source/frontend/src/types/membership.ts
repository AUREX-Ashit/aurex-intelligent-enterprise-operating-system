/**
 * Mirrors AuthService's schemas/membership.py exactly. No field added,
 * renamed, or omitted relative to the backend contract (WP-03, C-007).
 */

export type MembershipType = "INTERNAL" | "EXTERNAL";
export type LicenseType = "FULL" | "LIGHT";

export interface EstablishMembershipRequest {
  person_id: string;
  organization_id: string;
  role_id: string;
  home_node_id?: string | null;
  membership_type?: MembershipType;
  license_type?: LicenseType;
  effective_from?: string | null;
  effective_to?: string | null;
  is_primary?: boolean;
}

export interface MembershipResponse {
  id: string;
  person_id: string;
  organization_id: string;
  role_id: string;
  home_node_id: string | null;
  membership_type: string;
  license_type: string;
  membership_status: string;
  is_primary: boolean;
  effective_from: string;
  effective_to: string | null;
  joined_at: string;
  created_at: string;
  updated_at: string | null;
}

export type MembershipAuthorityConsequence =
  | "ACTIVE_AND_EFFECTIVE"
  | "ACTIVE_NOT_YET_EFFECTIVE"
  | "ACTIVE_BUT_LAPSED"
  | "NOT_ACTIVE";

export interface MembershipUnderstandingResponse extends MembershipResponse {
  currently_effective: boolean;
  authority_consequence: MembershipAuthorityConsequence;
}

export interface ChangeMembershipTermsRequest {
  membership_type?: MembershipType | null;
  license_type?: LicenseType | null;
  home_node_id?: string | null;
  effective_from?: string | null;
  effective_to?: string | null;
  reason?: string | null;
}

export interface MembershipPortfolioResponse {
  memberships: MembershipResponse[];
}
