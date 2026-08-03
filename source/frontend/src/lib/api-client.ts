/**
 * Reusable, environment-aware API client.
 *
 * This is transport infrastructure only — GET/POST/PUT/DELETE against any
 * backend path, with centralized error handling and an optional bearer
 * token hook. It contains no knowledge of any specific endpoint, resource,
 * or Business Activity; those belong in `src/services/`, layered on top of
 * this client, one file per backend domain.
 */

import { appConfig } from "./config";
import { logger } from "./logger";

export class ApiError extends Error {
  readonly status: number;
  readonly detail?: unknown;

  constructor(message: string, status: number, detail?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

interface RequestOptions {
  headers?: HeadersInit;
  signal?: AbortSignal;
  /**
   * Opts a call out of the 401 refresh-and-retry behavior below. Set only
   * by src/services/auth-api.ts's own login/refresh calls, where a 401 is
   * a genuine authentication failure to surface, not an expired session
   * to silently recover from.
   */
  skipAuthRetry?: boolean;
  /**
   * Overrides the default base URL (`appConfig.authServiceUrl`) for this
   * call. Introduced by WP-11 (Enterprise Search, C-093) — the first
   * backend domain hosted outside AuthService (`AIService`,
   * `appConfig.aiServiceUrl`); see `src/services/search-api.ts`.
   */
  baseUrl?: string;
}

/**
 * Resolves an access token to attach to outgoing requests, if any.
 * Wired to real storage via `setAuthTokenProvider` (see src/app/providers.tsx).
 */
let tokenProvider: () => string | null = () => null;

export function setAuthTokenProvider(provider: () => string | null): void {
  tokenProvider = provider;
}

/**
 * Resolves the caller's own current tenant (Organization) to attach as
 * X-Tenant-ID, if any. Introduced by WP-10 (Configuration Management,
 * C-041) — the first backend prefix (/configuration) genuinely requiring
 * this header rather than being exempted by AuthService's own
 * TenantMiddleware (middleware/tenant.py's own new comment block).
 * Wired to the session's own decoded organization_id claim (see
 * src/app/providers.tsx), mirroring `tokenProvider`'s identical shape.
 */
let tenantIdProvider: () => string | null = () => null;

export function setTenantIdProvider(provider: () => string | null): void {
  tenantIdProvider = provider;
}

/**
 * Attempts to silently renew the session (via AuthService's POST
 * /auth/refresh — see src/services/auth-api.ts) when a request comes back
 * 401. Resolves `true` if a new access token is now available and the
 * failed request should be retried once, `false` otherwise (no refresh
 * token, or the refresh itself failed — the caller sees the original 401).
 * Wired via `setRefreshHandler` (see src/app/providers.tsx).
 */
let refreshHandler: (() => Promise<boolean>) | null = null;
let refreshInFlight: Promise<boolean> | null = null;

export function setRefreshHandler(handler: (() => Promise<boolean>) | null): void {
  refreshHandler = handler;
}

async function parseErrorBody(response: Response): Promise<{ message: string; detail?: unknown }> {
  try {
    const payload = await response.json();
    if (typeof payload?.detail === "string") {
      return { message: payload.detail, detail: payload.detail };
    }
    if (typeof payload?.message === "string") {
      return { message: payload.message, detail: payload };
    }
    return { message: `Request failed with HTTP ${response.status}.`, detail: payload };
  } catch {
    return { message: `Request failed with HTTP ${response.status}.` };
  }
}

type Method = "GET" | "POST" | "PUT" | "DELETE";

async function request<T>(
  method: Method,
  path: string,
  body?: unknown,
  options: RequestOptions = {},
  isRetryAfterRefresh = false,
): Promise<T> {
  const url = path.startsWith("http") ? path : `${options.baseUrl ?? appConfig.authServiceUrl}${path}`;
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");

  const token = tokenProvider();
  if (token && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const tenantId = tenantIdProvider();
  if (tenantId && !headers.has("X-Tenant-ID")) {
    headers.set("X-Tenant-ID", tenantId);
  }

  logger.debug("API request", { method, url });

  let response: Response;
  try {
    response = await fetch(url, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
      signal: options.signal,
    });
  } catch {
    logger.error("API request failed to reach the server", { method, url });
    throw new ApiError("Unable to reach the server. Check your connection and try again.", 0);
  }

  if (!response.ok) {
    if (response.status === 401 && !options.skipAuthRetry && !isRetryAfterRefresh && refreshHandler) {
      if (!refreshInFlight) {
        refreshInFlight = refreshHandler().finally(() => {
          refreshInFlight = null;
        });
      }
      const refreshed = await refreshInFlight;
      if (refreshed) {
        return request<T>(method, path, body, options, true);
      }
    }

    const { message, detail } = await parseErrorBody(response);
    logger.warn("API request returned an error response", { method, url, status: response.status });
    throw new ApiError(message, response.status, detail);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const apiClient = {
  get: <T>(path: string, options?: RequestOptions) => request<T>("GET", path, undefined, options),
  post: <T>(path: string, body?: unknown, options?: RequestOptions) =>
    request<T>("POST", path, body, options),
  put: <T>(path: string, body?: unknown, options?: RequestOptions) =>
    request<T>("PUT", path, body, options),
  delete: <T>(path: string, options?: RequestOptions) => request<T>("DELETE", path, undefined, options),
};
