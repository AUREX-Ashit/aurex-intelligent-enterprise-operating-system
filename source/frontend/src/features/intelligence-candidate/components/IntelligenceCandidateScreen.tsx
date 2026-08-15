"use client";

import { IntelligenceCandidateSection } from "@/features/intelligence-candidate/components/IntelligenceCandidateSection";
import { ResolveIntelligenceCandidateSection } from "@/features/intelligence-candidate/components/ResolveIntelligenceCandidateSection";
import { useIntelligenceCandidateManagement } from "@/features/intelligence-candidate/state/useIntelligenceCandidateManagement";

/**
 * WP-14 BA-02 (Register, C-090) + BA-03 (Resolve — Convergence Decision,
 * C-090) — Enterprise Intelligence Candidate. Minimum Enterprise
 * Experience per `IRA-014 §6`'s own Frontend/UX rows: BA-02 "A
 * registration form"; BA-03 "a resolution queue" — realized here as
 * resolve-by-id, not a browsable queue, since a queue's own listing
 * capability would require a GET/list endpoint `IRA-014 §6`'s own
 * "APIs/services required" row never names for either Business Activity
 * (disclosed in `ResolveIntelligenceCandidateSection.tsx`'s own
 * docstring, not silently resolved). Composed on the existing
 * `enterprise-intelligence` admin nav slot, alongside `WP-11`'s own
 * `EnterpriseSearchScreen` and WP-14 BA-01/BA-04's own screens — reused,
 * not a new nav item. No candidate listing or promotion/convergence
 * functionality is built here — deliberately out of scope for both BAs.
 */
export function IntelligenceCandidateScreen() {
  const { registerState, register, resolveState, resolve } = useIntelligenceCandidateManagement();

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight text-foreground">Intelligence Candidates</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Capture extracted facts with no matching Canonical Data Element, so none is discarded,
          and resolve them to a governed outcome (C-090).
        </p>
      </div>

      <IntelligenceCandidateSection registerState={registerState} onRegister={register} />
      <ResolveIntelligenceCandidateSection resolveState={resolveState} onResolve={resolve} />
    </div>
  );
}
