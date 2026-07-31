"use client";

import { useEstablishDomainPermission } from "@/features/domain-permission/state/useEstablishDomainPermission";
import { DomainPermissionSearchGrid } from "@/features/domain-permission/components/DomainPermissionSearchGrid";
import { EstablishDomainPermissionSection } from "@/features/domain-permission/components/EstablishDomainPermissionSection";

export function DomainPermissionManagementScreen() {
  const { state, establish } = useEstablishDomainPermission();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Domain Permissions</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Establish and understand Domain Permission grants (C-003).
        </p>
      </div>

      <DomainPermissionSearchGrid />
      <EstablishDomainPermissionSection state={state} onEstablish={establish} />
    </div>
  );
}
