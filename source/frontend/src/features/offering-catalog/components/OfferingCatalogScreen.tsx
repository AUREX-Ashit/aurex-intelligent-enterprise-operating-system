"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { EstablishOfferingDefinitionSection } from "@/features/offering-catalog/components/EstablishOfferingDefinitionSection";
import { OfferingDefinitionListSection } from "@/features/offering-catalog/components/OfferingDefinitionListSection";
import { useOfferingCatalog } from "@/features/offering-catalog/state/useOfferingCatalog";

/**
 * C-021 Product & Service Catalog — WP-20 BA-01 ("Establish / Manage
 * Offering Definition"). Exactly the three authorized operations
 * (ROD-C021 D4; TDS-C021 §13/§14): establish a draft Atomic Offering
 * Definition, list the platform-global catalog, and read one. No
 * publication, retirement, composition, relationship, pricing, Subscription,
 * Customer/Account, or Entitlement UI — those are out of BA-01 scope.
 */
export function OfferingCatalogScreen() {
  const { establishState, listState, detailState, establish, loadList, loadDetail } =
    useOfferingCatalog();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Product & Service Catalog"
        description="Establish and review the enterprise's authoritative Offering Definitions (C-021, WP-20 BA-01)."
      />
      <EstablishOfferingDefinitionSection state={establishState} onEstablish={establish} />
      <OfferingDefinitionListSection
        listState={listState}
        detailState={detailState}
        onLoad={loadList}
        onSelect={loadDetail}
      />
    </div>
  );
}
