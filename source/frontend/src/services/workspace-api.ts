/**
 * Workspace API wrapper — the only module permitted to call
 * GET /workspaces/candidates. Built on the shared `apiClient`, not raw
 * fetch. Mirrors AuthService's routers/workspace.py exactly (WP-09
 * BA-01, EX-C008-01/02).
 */

import { apiClient } from "@/lib/api-client";
import type { WorkspaceCandidatesResponse } from "@/types/workspace";

export function getWorkspaceCandidates(): Promise<WorkspaceCandidatesResponse> {
  return apiClient.get<WorkspaceCandidatesResponse>("/workspaces/candidates");
}
