/**
 * Mirrors AuthService's schemas/workspace.py exactly (WP-09 BA-01,
 * EX-C008-01/02). No field added, renamed, or omitted relative to the
 * backend contract.
 */

export interface WorkspaceCandidate {
  membership_id: string;
  organization_id: string;
  organization_name: string;
  role_code: string;
  role_name: string;
  home_node_id: string | null;
  is_primary: boolean;
}

export interface WorkspaceCandidatesResponse {
  candidates: WorkspaceCandidate[];
}

export type WorkspaceContextStatus = "CURRENT" | "UNRESOLVED";

export interface WorkspaceStatusResponse {
  membership_id: string;
  organization_id: string;
  status: WorkspaceContextStatus;
  checked_at: string;
}
