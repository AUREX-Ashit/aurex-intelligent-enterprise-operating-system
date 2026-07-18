/**
 * Health/readiness check against AuthService. Operational infrastructure,
 * not a Business Activity — safe to wire up for real, and used here to
 * demonstrate the API Foundation (src/lib/api-client.ts) end-to-end.
 */

import { apiClient } from "@/lib/api-client";
import type { HealthCheckResponse } from "@/types/health";

export function fetchHealth(): Promise<HealthCheckResponse> {
  return apiClient.get<HealthCheckResponse>("/health");
}
