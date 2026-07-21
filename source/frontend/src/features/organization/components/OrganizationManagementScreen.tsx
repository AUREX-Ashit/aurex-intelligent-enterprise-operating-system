"use client";

import { useEstablishOrganization } from "@/features/organization/state/useEstablishOrganization";
import { useViewOrganization } from "@/features/organization/state/useViewOrganization";
import { EstablishOrganizationForm } from "@/features/organization/components/EstablishOrganizationForm";
import { OrganizationResultPanel } from "@/features/organization/components/OrganizationResultPanel";
import { ViewOrganizationSection } from "@/features/organization/components/ViewOrganizationSection";

/**
 * WP-01 Business Activities implemented: BA-01 Establish Organization,
 * BA-02 View Organization Details. Remaining Business Activities
 * (Search, Update, Activate/Suspend, Configuration, Audit History —
 * IRA-001 §9) extend this screen as they land; this is not a stand-in
 * for the full capability.
 */
export function OrganizationManagementScreen() {
  const { state: establishState, establish } = useEstablishOrganization();
  const { state: viewState, view } = useViewOrganization();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Organization Management</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Establish or look up an organization. Requires the PLATFORM_ADMIN role.
        </p>
      </div>

      <EstablishOrganizationForm state={establishState} onEstablish={establish} />
      <OrganizationResultPanel state={establishState} />

      <ViewOrganizationSection state={viewState} onView={view} />
    </div>
  );
}
