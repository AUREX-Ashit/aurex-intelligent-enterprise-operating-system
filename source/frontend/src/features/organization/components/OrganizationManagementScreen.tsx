"use client";

import { useEstablishOrganization } from "@/features/organization/state/useEstablishOrganization";
import { EstablishOrganizationForm } from "@/features/organization/components/EstablishOrganizationForm";
import { OrganizationResultPanel } from "@/features/organization/components/OrganizationResultPanel";

/**
 * WP-01 Business Activity 1: Establish Organization. Additional
 * Organization Management Business Activities (lifecycle, listing, audit
 * history — IRA-001 Phases 1/3/4/5) extend this screen as they land;
 * this is not a stand-in for the full capability.
 */
export function OrganizationManagementScreen() {
  const { state, establish } = useEstablishOrganization();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Organization Management</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Establish a new organization. Requires the PLATFORM_ADMIN role.
        </p>
      </div>

      <EstablishOrganizationForm state={state} onEstablish={establish} />
      <OrganizationResultPanel state={state} />
    </div>
  );
}
