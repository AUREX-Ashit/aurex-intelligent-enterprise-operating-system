/**
 * Product & Service Catalog API wrapper (C-021, WP-20 BA-01) — the only
 * module permitted to call the /offerings endpoints. Built on the shared
 * `apiClient` (which attaches Authorization; X-Tenant-ID is attached too but
 * the /offerings prefix is tenant-middleware-exempt on the backend, since
 * the C-021 catalog is platform-global — ROD-C021 D8). Mirrors AuthService's
 * routers/offering.py exactly: establish, list, read. No publish/retire/
 * transition/delete endpoint is charted, so none is called here.
 */

import { apiClient } from "@/lib/api-client";
import type {
  EstablishOfferingDefinitionRequest,
  OfferingDefinitionResponse,
} from "@/types/offering";

export function establishOfferingDefinition(
  request: EstablishOfferingDefinitionRequest,
): Promise<OfferingDefinitionResponse> {
  return apiClient.post<OfferingDefinitionResponse>("/offerings", request);
}

export function listOfferingDefinitions(): Promise<OfferingDefinitionResponse[]> {
  return apiClient.get<OfferingDefinitionResponse[]>("/offerings");
}

export function getOfferingDefinition(offeringId: string): Promise<OfferingDefinitionResponse> {
  return apiClient.get<OfferingDefinitionResponse>(`/offerings/${offeringId}`);
}
