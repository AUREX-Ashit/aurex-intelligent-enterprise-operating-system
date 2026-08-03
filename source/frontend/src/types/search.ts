/**
 * Mirrors AIService's schemas/search.py exactly (WP-11 BA-01/02/03,
 * C-093). No field added, renamed, or omitted relative to the backend
 * contract.
 */

export interface EstablishIndexConfigurationRequest {
  index_name: string;
  embedding_model: string;
  embedding_dimension: number;
  retrieval_mode: "SEMANTIC" | "LEXICAL" | "HYBRID";
  refresh_cadence?: string | null;
  platform_wide: boolean;
}

export interface IndexConfigurationResponse {
  vector_index_id: string;
  index_name: string;
  embedding_model: string;
  embedding_dimension: number;
  retrieval_mode: string;
  refresh_cadence: string | null;
  active_flag: boolean;
  organization_id: string | null;
  created_at: string;
}

export interface IndexConfigurationListResponse {
  index_configurations: IndexConfigurationResponse[];
}

export interface RegisterContentRequest {
  index_name: string;
  text: string;
  evidence_type?: string | null;
  evidence_source?: string | null;
  file_reference?: string | null;
}

export interface RegisteredContentResponse {
  evidence_id: string;
  vector_index_id: string;
  chunk_count: number;
  document_chunk_ids: string[];
  created_at: string;
}

export interface ExecuteSearchRequest {
  query: string;
  index_name?: string | null;
  top_k: number;
}

export interface SearchResultItem {
  document_chunk_id: string;
  evidence_id: string;
  score: number;
  citation: string;
  metadata: Record<string, unknown>;
}

export interface SearchResponse {
  vector_index_id: string;
  results: SearchResultItem[];
  message: string | null;
}
