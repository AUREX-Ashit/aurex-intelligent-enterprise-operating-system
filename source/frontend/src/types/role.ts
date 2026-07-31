/**
 * Mirrors AuthService's schemas/role.py exactly. No field added, renamed,
 * or omitted relative to the backend contract (WP-02, C-003). No
 * list/search endpoint exists for Role — establish-only.
 */

export interface EstablishRoleRequest {
  role_code: string;
  role_name: string;
  description?: string | null;
  is_system_role?: boolean;
}

export interface RoleResponse {
  id: string;
  role_code: string;
  role_name: string;
  description: string | null;
  is_system_role: boolean;
  version: number;
  status: string;
  effective_from: string;
  effective_to: string | null;
  approval_reference: string | null;
  supersedes_id: string | null;
  created_at: string;
  updated_at: string | null;
}
