/**
 * Mirrors AIService's schemas/unclassified_intelligence.py exactly
 * (WP-14 BA-02/BA-03, C-090). No field added, renamed, or omitted
 * relative to the backend contract.
 */

export const ALLOWED_EXTRACTION_METHODS = ["MANUAL_ENTRY", "API_INGEST"] as const;

export interface RegisterIntelligenceCandidateRequest {
  raw_extracted_value: string;
  source_document_reference: string;
  source_page_section?: string | null;
  extraction_method: (typeof ALLOWED_EXTRACTION_METHODS)[number];
}

export interface IntelligenceCandidateResponse {
  unclassified_id: string;
  organization_id: string;
  raw_extracted_value: string;
  source_document_reference: string;
  source_page_section: string | null;
  extraction_method: string;
  llm_label_suggestion: string | null;
  llm_confidence_score: number | null;
  probable_domain: string | null;
  probable_bq_id: string | null;
  resolution_status: string;
  convergence_signal_raised_flag: boolean;
  active_flag: boolean;
  created_at: string;
  updated_at: string;
}

// ---------------------------------------------------------------------------
// BA-03 — Resolve Enterprise Intelligence Candidate (Convergence Decision)
// ---------------------------------------------------------------------------

export const RESOLUTION_OUTCOMES = ["MAPPED_TO_EXISTING", "NEW_CDE_CREATED", "DISCARDED"] as const;

export interface ResolveIntelligenceCandidateRequest {
  outcome: (typeof RESOLUTION_OUTCOMES)[number];
  metric_id?: string | null;
  metric_name?: string | null;
  metric_code?: string | null;
  metric_description?: string | null;
  unit_of_measure?: string | null;
  formula_logic?: string | null;
  semantic_match_rejected_reason?: string | null;
}

export interface ResolvedIntelligenceCandidateResponse {
  unclassified_id: string;
  resolution_status: string;
  resolved_by_user_id: string | null;
  resolved_at: string | null;
  resolved_metric_id: string | null;
  resolved_customer_metric_id: string | null;
  semantic_match_attempted_flag: boolean | null;
  semantic_match_result_metric_id: string | null;
  semantic_match_score: number | null;
  same_organization_duplicate_customer_metric_id: string | null;
  evidence_id: string | null;
}
