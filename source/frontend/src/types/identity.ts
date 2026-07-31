/**
 * Mirrors AuthService's schemas/identity.py exactly. No field added,
 * renamed, or omitted relative to the backend contract (WP-08 BA-01/02/03,
 * EX-C001-06/07/08).
 */

export type IdentityContextStatus = "CURRENT" | "UNRESOLVED";

export interface IdentityStatusResponse {
  identity_id: string;
  person_id: string;
  status: IdentityContextStatus;
  checked_at: string;
}

export type RoutedPath = "NEW_IDENTITY" | "RE_RESOLUTION";

export interface RecoverIdentityRequest {
  person_id: string;
  reason: string;
}

export interface IdentityRecoveryRequestResponse {
  id: string;
  person_id: string;
  routed_path: RoutedPath;
  status: string;
  created_at: string;
}

export type IdentityHandoffClassification = "CAPABILITY_SCOPED_INSUFFICIENCY" | "INTEGRITY_SIGNAL";

export interface ClassifyHandoffRejectionRequest {
  identity_id: string;
  rejecting_capability: string;
  stated_reason: string;
}

export interface HandoffRejectionOutcome {
  identity_id: string;
  classification: IdentityHandoffClassification;
  identity_context_preserved: boolean;
  routed_to: string | null;
  explanation: string;
  checked_at: string;
}
