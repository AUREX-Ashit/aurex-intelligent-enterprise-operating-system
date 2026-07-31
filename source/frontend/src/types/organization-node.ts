/**
 * Mirrors AuthService's schemas/organization_node.py exactly. No field
 * added, renamed, or omitted relative to the backend contract (WP-04,
 * C-005). node_type and operational_status are free text server-side, not
 * closed enums — rendered here as plain strings, not a fixed option list.
 */

export interface EstablishOrganizationNodeRequest {
  node_code: string;
  node_name: string;
  node_type: string;
  legal_entity_name?: string | null;
  business_unit?: string | null;
  sector?: string | null;
  operational_status?: string | null;
  effective_from?: string | null;
  effective_to?: string | null;
}

export interface OrganizationNodeResponse {
  id: string;
  node_code: string;
  node_name: string;
  node_type: string;
  legal_entity_name: string | null;
  business_unit: string | null;
  sector: string | null;
  operational_status: string | null;
  active_flag: boolean;
  effective_from: string | null;
  effective_to: string | null;
}
