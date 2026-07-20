/**
 * Auth API wrapper — the only module permitted to call POST /auth/login or
 * POST /auth/refresh. Built on the shared `apiClient` (src/lib/api-client.ts),
 * not raw fetch. No endpoint beyond these two exists here; none is
 * invented. Mirrors AuthService's routers/auth.py, mounted at prefix
 * "/auth" (see AuthService/main.py), exactly — including the optional
 * X-Tenant-ID header for multi-org disambiguation.
 */

import { apiClient } from "@/lib/api-client";
import type { LoginRequest, LoginResponse, RefreshTokenResponse } from "@/types/auth";

export function login(request: LoginRequest, organizationId?: string): Promise<LoginResponse> {
  return apiClient.post<LoginResponse>("/auth/login", request, {
    skipAuthRetry: true,
    headers: organizationId ? { "X-Tenant-ID": organizationId } : undefined,
  });
}

export function refresh(refreshToken: string): Promise<RefreshTokenResponse> {
  return apiClient.post<RefreshTokenResponse>("/auth/refresh", undefined, {
    skipAuthRetry: true,
    headers: { Authorization: `Bearer ${refreshToken}` },
  });
}
