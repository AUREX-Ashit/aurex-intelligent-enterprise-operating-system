/**
 * Mirrors AuthService's schemas/domain_permission.py exactly. No field
 * added, renamed, or omitted relative to the backend contract (WP-02/WP-06,
 * C-003).
 */

export type DomainPermissionLevel =
  | "VIEW"
  | "ENTER"
  | "EDIT"
  | "REVIEW"
  | "APPROVE"
  | "ASSIGN"
  | "DELEGATE"
  | "ADMIN";

export type VersionStatus = "ACTIVE" | "SUPERSEDED" | "DEPRECATED" | "RETIRED";

export interface EstablishDomainPermissionRequest {
  membership_id: string;
  domain_id: string;
  permission_level: DomainPermissionLevel;
  effective_from?: string | null;
  effective_to?: string | null;
}

export interface DomainPermissionResponse {
  id: string;
  membership_id: string;
  domain_id: string;
  permission_level: string;
  effective_from: string;
  effective_to: string | null;
  version: number;
  status: string;
  approval_reference: string | null;
  supersedes_id: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface SearchDomainPermissionsParams {
  domain_id?: string;
  membership_id?: string;
  status?: VersionStatus;
}
