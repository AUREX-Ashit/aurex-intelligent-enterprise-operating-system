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
}

/**
 * Resolves an access token to attach to outgoing requests, if any.
 *
 * Deliberately a no-op today (always returns null). Authentication is
 * infrastructure being prepared here, not implemented: this is the single
 * seam a future login implementation wires a real session store into, via
 * `setAuthTokenProvider`, without any other part of the API layer changing.
 */
let tokenProvider: () => string | null = () => null;

export function setAuthTokenProvider(provider: () => string | null): void {
  tokenProvider = provider;
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
): Promise<T> {
  const url = path.startsWith("http") ? path : `${appConfig.authServiceUrl}${path}`;
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");

  const token = tokenProvider();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
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
