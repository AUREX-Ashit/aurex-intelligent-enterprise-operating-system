"use client";

import { DiscoveryProviderSection } from "@/features/discovery-provider/components/DiscoveryProviderSection";
import { useDiscoveryProviderManagement } from "@/features/discovery-provider/state/useDiscoveryProviderManagement";

/**
 * WP-14 BA-01 — Establish Discovery Provider Configuration (C-090
 * Enterprise Discovery). Minimum Enterprise Experience: establish + list
 * only, per `IRA-014 §6` BA-01's own Frontend/UX row ("Admin config
 * screen — establish/list"). Composed on the existing
 * `enterprise-intelligence` admin nav slot, alongside `WP-11`'s own
 * `EnterpriseSearchScreen` and WP-14 BA-04's own `KnowledgeAssetScreen` —
 * reused, not a new nav item, the same "compose multiple Business
 * Activities on one existing slot" precedent both already established.
 * No connector configuration, live discovery, or candidate-intake
 * functionality is built here — deliberately out of this Business
 * Activity's own scope.
 */
export function DiscoveryProviderScreen() {
  const { establishState, listState, establish, loadProviders } = useDiscoveryProviderManagement();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight text-foreground">Discovery Providers</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Configure Enterprise Intelligence discovery sources — Enterprise, External, and Real-Time
          (C-090).
        </p>
      </div>

      <DiscoveryProviderSection
        establishState={establishState}
        listState={listState}
        onEstablish={establish}
        onLoad={loadProviders}
      />
    </div>
  );
}
