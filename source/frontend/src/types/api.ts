/**
 * Generic, backend-agnostic API types. No Business Activity, capability, or
 * resource-specific shape belongs here — those live beside the service
 * that owns them in `src/services/`.
 */

export interface ApiErrorShape {
  message: string;
  status: number;
  detail?: unknown;
}
