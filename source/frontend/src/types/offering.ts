/**
 * Mirrors AuthService's schemas/offering.py exactly (C-021 Product &
 * Service Catalog, WP-20 BA-01 — "Establish / Manage Offering Definition").
 * No field added, renamed, or omitted relative to the backend contract.
 *
 * Scope is strictly ROD-C021 D1–D8 as amended by RO decisions O1 (identity
 * generation) and O2 (category_ref optional/nullable). No composition,
 * relationships, publication, retirement, pricing computation, Subscription,
 * Customer/Account, or Entitlement semantics are represented here.
 */

/** COM-001-021 Product ↔ Service classification axis (the only axis in BA-01). */
export type OfferingKind = "PRODUCT" | "SERVICE";

/** COM-001-020 offering state. BA-01 only ever produces `draft`. */
export type OfferingState = "draft" | "published" | "retired";

export interface EstablishOfferingDefinitionRequest {
  offering_name: string;
  offering_kind: OfferingKind;
  /** Optional opaque category reference (RO decision O2). Omit for none; if given, must be non-empty. */
  category_ref?: string | null;
  /** Optional opaque list-price reference (ROD-C021 D6). A reference string only — never a number. */
  list_price_reference?: string | null;
}

export interface OfferingDefinitionResponse {
  id: string;
  /** COM-001-001 Universal Identity (`PREFIX-NNNNNN`) and the stable Offering Reference. System-assigned. */
  offering_reference: string;
  offering_name: string;
  offering_kind: string;
  category_ref: string | null;
  list_price_reference: string | null;
  state: string;
  version: number;
  supersedes_id: string | null;
  created_at: string;
  updated_at: string | null;
}
