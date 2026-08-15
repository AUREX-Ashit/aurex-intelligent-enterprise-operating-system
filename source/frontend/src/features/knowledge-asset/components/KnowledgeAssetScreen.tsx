"use client";

import { EstablishKnowledgeAssetSection } from "@/features/knowledge-asset/components/EstablishKnowledgeAssetSection";
import { KnowledgeAssetStatusSection } from "@/features/knowledge-asset/components/KnowledgeAssetStatusSection";
import { useKnowledgeAssetManagement } from "@/features/knowledge-asset/state/useKnowledgeAssetManagement";

/**
 * WP-14 BA-04 — Establish Knowledge Asset (C-091 Knowledge Management).
 * Minimum Enterprise Experience: establish + status view only, per
 * `IRA-014 §6` BA-04's own Frontend/UX row and `§9` Plan B. Composed on
 * the existing `enterprise-intelligence` admin nav slot, alongside
 * WP-11's own `EnterpriseSearchScreen` — reused, not a new nav item,
 * mirroring that screen's own identical "compose multiple Business
 * Activities on one existing slot" precedent (its own docstring: "reused,
 * not a new nav item"). No lifecycle transition, edit, delete,
 * search/list, Knowledge Graph, discovery, or convergence functionality
 * is built here — deliberately out of this Business Activity's own scope.
 */
export function KnowledgeAssetScreen() {
  const { establishState, retrieveState, establish, retrieve } = useKnowledgeAssetManagement();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight text-foreground">Knowledge Assets</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Curate Signals into governed Knowledge Assets, each carrying Provenance from first existence
          (C-091).
        </p>
      </div>

      <EstablishKnowledgeAssetSection establishState={establishState} onEstablish={establish} />
      <KnowledgeAssetStatusSection retrieveState={retrieveState} onRetrieve={retrieve} />
    </div>
  );
}
