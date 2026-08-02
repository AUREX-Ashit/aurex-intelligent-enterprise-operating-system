"use client";

import { useConfigurationManagement } from "@/features/configuration/state/useConfigurationManagement";
import { ConfigurationEntriesSection } from "@/features/configuration/components/ConfigurationEntriesSection";
import { EstablishConfigurationSection } from "@/features/configuration/components/EstablishConfigurationSection";

export function ConfigurationManagementScreen() {
  const { establishState, entriesState, establish, loadEntries } = useConfigurationManagement();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Enterprise Configuration</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Resolve and establish Terminology, Branding, Theme, Accessibility, and Localization for your
          Organization (C-041).
        </p>
      </div>

      <ConfigurationEntriesSection state={entriesState} onLoad={loadEntries} />
      <EstablishConfigurationSection state={establishState} onEstablish={establish} />
    </div>
  );
}
