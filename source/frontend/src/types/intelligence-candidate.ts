/**
 * Mirrors AIService's schemas/unclassified_intelligence.py exactly
 * (WP-14 BA-02, C-090). No field added, renamed, or omitted relative to
 * the backend contract.
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
