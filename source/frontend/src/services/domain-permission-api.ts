/**
 * Domain Permission API wrapper — the only module permitted to call
 * POST /domain-permissions, GET /domain-permissions, and
 * GET /domain-permissions/{id}. Built on the shared `apiClient`, not raw
 * fetch. Mirrors AuthService's routers/domain_permission.py exactly.
 */

import { apiClient } from "@/lib/api-client";
import type {
  DomainPermissionResponse,
  EstablishDomainPermissionRequest,
  SearchDomainPermissionsParams,
} from "@/types/domain-permission";

export function establishDomainPermission(
  request: EstablishDomainPermissionRequest,
): Promise<DomainPermissionResponse> {
  return apiClient.post<DomainPermissionResponse>("/domain-permissions", request);
}

export function getDomainPermission(domainPermissionId: string): Promise<DomainPermissionResponse> {
  return apiClient.get<DomainPermissionResponse>(`/domain-permissions/${domainPermissionId}`);
}

export function searchDomainPermissions(
  params: SearchDomainPermissionsParams = {},
): Promise<DomainPermissionResponse[]> {
  const query = new URLSearchParams();
  if (params.domain_id) query.set("domain_id", params.domain_id);
  if (params.membership_id) query.set("membership_id", params.membership_id);
  if (params.status) query.set("status", params.status);

  const queryString = query.toString();
  return apiClient.get<DomainPermissionResponse[]>(
    `/domain-permissions${queryString ? `?${queryString}` : ""}`,
  );
}
