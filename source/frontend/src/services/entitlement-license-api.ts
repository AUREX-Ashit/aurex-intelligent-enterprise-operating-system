/**
 * Entitlement & License API wrapper (C-023, WP-17 BA-01) — the only
 * module permitted to call POST /entitlement-license-contexts and
 * GET /entitlement-license-contexts/{id}. Built on the shared `apiClient`
 * (which attaches Authorization and X-Tenant-ID), not raw fetch. Mirrors
 * AuthService's routers/entitlement_license.py exactly. WP-17 BA-01
 * charters no list/search endpoint, so none is called here.
 */

import { apiClient } from "@/lib/api-client";
import type {
  ContextOutcomeResponse,
  EstablishEntitlementLicenseRequest,
  EstablishEntitlementLicenseResponse,
} from "@/types/entitlement-license";

export function establishEntitlementLicenseContext(
  request: EstablishEntitlementLicenseRequest,
): Promise<EstablishEntitlementLicenseResponse> {
  return apiClient.post<EstablishEntitlementLicenseResponse>(
    "/entitlement-license-contexts",
    request,
  );
}

export function getEntitlementLicenseOutcome(contextId: string): Promise<ContextOutcomeResponse> {
  return apiClient.get<ContextOutcomeResponse>(`/entitlement-license-contexts/${contextId}`);
}
