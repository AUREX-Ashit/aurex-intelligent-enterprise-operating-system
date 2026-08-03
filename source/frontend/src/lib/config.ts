/**
 * Centralized, validated environment configuration.
 *
 * Every environment-derived value the application reads should be resolved
 * here, once, rather than each call site reading `process.env` directly.
 * That keeps the set of environment variables the app actually depends on
 * discoverable in one place, and gives every value a single, safe default
 * for local development.
 */

function readPublicEnv(name: string, fallback: string): string {
  const value = process.env[name];
  if (!value || value.trim().length === 0) {
    return fallback;
  }
  return value;
}

export const appConfig = {
  /** Base URL of AuthService — identity, person, and session endpoints. */
  authServiceUrl: readPublicEnv("NEXT_PUBLIC_AUTH_SERVICE_URL", "http://localhost:8000"),

  /**
   * Base URL of AIService — WP-11 Enterprise Search (C-093) endpoints
   * (`/search/*`). The first frontend integration against a backend
   * service other than AuthService — `api-client.ts`'s own `baseUrl`
   * request option exists specifically to support this.
   */
  aiServiceUrl: readPublicEnv("NEXT_PUBLIC_AI_SERVICE_URL", "http://localhost:3000"),

  /** Current runtime environment, as Next.js itself reports it. */
  environment: process.env.NODE_ENV ?? "development",

  isProduction: process.env.NODE_ENV === "production",
} as const;
