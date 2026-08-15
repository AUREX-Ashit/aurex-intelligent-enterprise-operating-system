/**
 * Mirrors AIService's schemas/knowledge_asset.py exactly (WP-14 BA-04,
 * C-091 Knowledge Management). No field added, renamed, or omitted
 * relative to the backend contract.
 */

export interface EstablishKnowledgeAssetRequest {
  knowledge_asset_name?: string | null;
  knowledge_asset_type?: string | null;
  provenance_reference: string;
  source_ingestion_id?: string | null;
  confidence_rule_id?: string | null;
}

export interface KnowledgeAssetResponse {
  knowledge_asset_id: string;
  knowledge_asset_name: string | null;
  knowledge_asset_type: string | null;
  curation_status: string;
  provenance_reference: string | null;
  source_ingestion_id: string | null;
  confidence_rule_id: string | null;
  freshness_last_confirmed_at: string | null;
  graph_engine_reference: string | null;
  active_flag: boolean;
  organization_id: string;
  created_at: string;
}
