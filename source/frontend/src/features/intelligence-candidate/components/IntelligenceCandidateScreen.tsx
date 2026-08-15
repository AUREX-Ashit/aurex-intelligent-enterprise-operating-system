"use client";

import { IntelligenceCandidateSection } from "@/features/intelligence-candidate/components/IntelligenceCandidateSection";
import { useIntelligenceCandidateManagement } from "@/features/intelligence-candidate/state/useIntelligenceCandidateManagement";

/**
 * WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090
 * Enterprise Discovery). Minimum Enterprise Experience: register only,
 * per `IRA-014 §6` BA-02's own Frontend/UX row ("A registration form").
 * Composed on the existing `enterprise-intelligence` admin nav slot,
 * alongside `WP-11`'s own `EnterpriseSearchScreen` and WP-14 BA-01/BA-04's
 * own screens — reused, not a new nav item. No resolution queue,
 * candidate listing, or convergence functionality is built here —
 * deliberately BA-03's own scope, not this Business Activity's.
 */
export function IntelligenceCandidateScreen() {
  const { registerState, register } = useIntelligenceCandidateManagement();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight text-foreground">Intelligence Candidates</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Capture extracted facts with no matching Canonical Data Element, so none is discarded
          (C-090).
        </p>
      </div>

      <IntelligenceCandidateSection registerState={registerState} onRegister={register} />
    </div>
  );
}
