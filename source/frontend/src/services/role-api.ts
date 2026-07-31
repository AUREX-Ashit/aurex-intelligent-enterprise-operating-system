/**
 * Role API wrapper — the only module permitted to call POST /roles. Built
 * on the shared `apiClient`, not raw fetch. Mirrors AuthService's
 * routers/role.py exactly. No list/search endpoint exists for Role
 * (WP-02 built no such Business Activity), so none is called here.
 */

import { apiClient } from "@/lib/api-client";
import type { EstablishRoleRequest, RoleResponse } from "@/types/role";

export function establishRole(request: EstablishRoleRequest): Promise<RoleResponse> {
  return apiClient.post<RoleResponse>("/roles", request);
}
