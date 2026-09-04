/**
 * Mirrors AuthService's schemas/entitlement_license.py exactly (C-023,
 * WP-17 BA-01 — "Establish Entitlement/License Context (Administrative)").
 * No field added, renamed, or omitted relative to the backend contract.
 */

/** The four URA-001-115 specialized C-023 license types. NOT FULL/LIGHT. */
export type C023LicenseType = "SUPPLIER" | "AUDITOR" | "BOARD_MEMBER" | "CONSULTANT";

export type EntitlementLicenseStatus = "ACTIVE" | "SUSPENDED" | "REVOKED";

export interface EstablishEntitlementLicenseRequest {
  /** Membership Anchor — provide to establish a License. */
  membership_id?: string | null;
  c023_license_type?: C023LicenseType | null;
  /** Entitlement Anchor — provide to establish an Entitlement. Must equal X-Tenant-ID. */
  organization_id?: string | null;
  domain_id?: string | null;
  entitlement_type_ref?: string | null;
  entitlement_source_reference?: string | null;
  effective_from?: string | null;
  effective_to?: string | null;
}

export interface LicenseContextResponse {
  id: string;
  membership_id: string;
  status: string;
  effective_from: string;
  effective_to: string | null;
  entitlement_source_reference: string | null;
  approval_authority_id: string;
  committed_by_actor_id: string;
  committed_at: string;
  c023_license_type: string | null;
  created_at: string;
}

export interface EntitlementContextResponse {
  id: string;
  organization_id: string;
  domain_id: string | null;
  entitlement_type_ref: string;
  status: string;
  effective_from: string;
  effective_to: string | null;
  entitlement_source_reference: string | null;
  approval_authority_id: string;
  committed_by_actor_id: string;
  committed_at: string;
  created_at: string;
}

export interface EstablishEntitlementLicenseResponse {
  license: LicenseContextResponse | null;
  entitlement: EntitlementContextResponse | null;
}

export interface ContextOutcomeResponse {
  kind: "LICENSE" | "ENTITLEMENT";
  license: LicenseContextResponse | null;
  entitlement: EntitlementContextResponse | null;
}
