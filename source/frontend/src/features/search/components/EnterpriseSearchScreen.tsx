"use client";

import { ExecuteSearchSection } from "@/features/search/components/ExecuteSearchSection";
import { RegisterContentSection } from "@/features/search/components/RegisterContentSection";
import { SearchIndexSection } from "@/features/search/components/SearchIndexSection";
import { useSearchManagement } from "@/features/search/state/useSearchManagement";

/**
 * WP-11 — Enterprise Search (C-093). Composes BA-01 (index configuration),
 * BA-03 (content registration), and BA-02 (query) on the existing
 * `enterprise-intelligence` admin nav slot — reused, not a new nav item
 * (`IRA-011 §7`). Placement of BA-02 as a persona-facing surface distinct
 * from BA-01/03's own admin surface was left undecided by IRA-011;
 * consolidating all three here is this Work Package's own disclosed
 * choice, not a DS-001 navigation pattern invented for this purpose.
 */
export function EnterpriseSearchScreen() {
  const {
    establishState,
    listState,
    registerState,
    searchState,
    establishIndex,
    loadIndexConfigurations,
    registerContent,
    executeSearch,
  } = useSearchManagement();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Enterprise Search</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Establish a search index, register searchable content, and ask evidence-cited questions across it
          (C-093).
        </p>
      </div>

      <ExecuteSearchSection state={searchState} onSearch={executeSearch} />
      <SearchIndexSection
        establishState={establishState}
        listState={listState}
        onEstablish={establishIndex}
        onLoad={loadIndexConfigurations}
      />
      <RegisterContentSection state={registerState} onRegister={registerContent} />
    </div>
  );
}
