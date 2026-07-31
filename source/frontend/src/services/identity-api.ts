/**
 * Identity Management API wrapper (WP-08, C-001) — the only module
 * permitted to call POST /identity/refresh-status, POST /identity/recover,
 * or POST /identity/classify-handoff-rejection. Built on the shared
 * `apiClient` (src/lib/api-client.ts), not raw fetch. No endpoint beyond
 * these three exists here; none is invented (IRA-008 §5).
 */

import { apiClient } from "@/lib/api-client";
import type {
  IdentityRecoveryRequestResponse,
  IdentityStatusResponse,
  RecoverIdentityRequest,
} from "@/types/identity";

export function refreshIdentityStatus(): Promise<IdentityStatusResponse> {
  return apiClient.post<IdentityStatusResponse>("/identity/refresh-status");
}

export function recoverIdentity(
  request: RecoverIdentityRequest,
): Promise<IdentityRecoveryRequestResponse> {
  return apiClient.post<IdentityRecoveryRequestResponse>("/identity/recover", request);
}
