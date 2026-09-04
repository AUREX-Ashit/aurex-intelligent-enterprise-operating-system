"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { useEntitlementLicense } from "@/features/entitlement-license/state/useEntitlementLicense";
import { EstablishEntitlementLicenseSection } from "@/features/entitlement-license/components/EstablishEntitlementLicenseSection";
import { EntitlementLicenseOutcomeSection } from "@/features/entitlement-license/components/EntitlementLicenseOutcomeSection";

/**
 * C-023 Licensing & Entitlement — WP-17 BA-01 ("Establish
 * Entitlement/License Context (Administrative)"). Exactly the two
 * authorized frontend items (IRA-C023 Decision 5; WP-17 §21;
 * TDS-C023 §17): (1) Establish License/Entitlement; (2) display the
 * resulting establishment/status outcome. No administration console,
 * Consumption / Allocation / Catalog / Billing / Subscription UI.
 */
export function EntitlementLicenseManagementScreen() {
  const { establishState, outcomeState, establish, loadOutcome } = useEntitlementLicense();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Entitlement & License"
        description="Establish Authoritative Entitlement/License Context and review the resulting outcome (C-023, WP-17 BA-01)."
      />
      <EstablishEntitlementLicenseSection state={establishState} onEstablish={establish} />
      <EntitlementLicenseOutcomeSection state={outcomeState} onLoad={loadOutcome} />
    </div>
  );
}
