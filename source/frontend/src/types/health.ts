/**
 * Mirrors AuthService's GET /health response shape exactly.
 */
export interface HealthCheckResponse {
  status: string;
  service: string;
  dependencies: Record<string, string>;
}
