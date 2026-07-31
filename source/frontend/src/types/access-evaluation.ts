/**
 * Mirrors AuthService's schemas/access_evaluation.py exactly (BA-01 only).
 * No field added, renamed, or omitted relative to the backend contract
 * (WP-05, C-002).
 */
import type { DomainPermissionLevel } from "@/types/domain-permission";

export interface EvaluateAccessRequest {
  membership_id: string;
  domain_id: string;
  permission_level: DomainPermissionLevel;
}

export interface AccessEvaluationOutcomeResponse {
  id: string;
  membership_id: string;
  domain_id: string;
  permission_level: string;
  outcome_type: string;
  validity_status: string;
  reason: string;
  approval_authority_id: string | null;
  created_at: string;
  updated_at: string | null;
}
