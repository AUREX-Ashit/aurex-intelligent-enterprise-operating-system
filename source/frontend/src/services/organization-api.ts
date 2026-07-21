/**
 * Organization API wrapper — the only module permitted to call
 * POST /organizations and GET /organizations/{id}. Built on the shared
 * `apiClient`, not raw fetch. Mirrors AuthService's routers/organization.py
 * exactly. The bearer token is attached automatically by apiClient's
 * tokenProvider (see src/app/providers.tsx) — both endpoints require the
 * PLATFORM_ADMIN role, enforced server-side.
 */

import { apiClient } from "@/lib/api-client";
import type { EstablishOrganizationRequest, OrganizationResponse } from "@/types/organization";

export function establishOrganization(
  request: EstablishOrganizationRequest,
): Promise<OrganizationResponse> {
  return apiClient.post<OrganizationResponse>("/organizations", request);
}

export function getOrganization(organizationId: string): Promise<OrganizationResponse> {
  return apiClient.get<OrganizationResponse>(`/organizations/${organizationId}`);
}
