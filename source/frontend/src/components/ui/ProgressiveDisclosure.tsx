"use client";

import { useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";

/**
 * Progressive Disclosure — DS-001's mandatory-reuse component contract
 * (`SD-001-021`, `IMP-001 §10.3`/`IMP-FE-004`). Every data-bearing widget
 * shall implement four distinct render states (Summary, Details, Evidence,
 * Audit History) as a required prop interface — not an ad-hoc pattern. This
 * is the first conforming implementation anywhere in this repository
 * (`SER-001 SE-001`, `IRA-012 §4.4`); every future capability composes this
 * component rather than reinventing its own disclosure pattern.
 */
export type ProgressiveDisclosureLevel = "summary" | "details" | "evidence" | "audit-history";

export interface ProgressiveDisclosureProps {
  summary: ReactNode;
  details: ReactNode;
  evidence: ReactNode;
  auditHistory: ReactNode;
  defaultLevel?: ProgressiveDisclosureLevel;
  className?: string;
}

const LEVELS: { key: ProgressiveDisclosureLevel; label: string }[] = [
  { key: "summary", label: "Summary" },
  { key: "details", label: "Details" },
  { key: "evidence", label: "Evidence" },
  { key: "audit-history", label: "Audit History" },
];

export function ProgressiveDisclosure({
  summary,
  details,
  evidence,
  auditHistory,
  defaultLevel = "summary",
  className,
}: ProgressiveDisclosureProps) {
  const [level, setLevel] = useState<ProgressiveDisclosureLevel>(defaultLevel);
  const content: Record<ProgressiveDisclosureLevel, ReactNode> = {
    summary,
    details,
    evidence,
    "audit-history": auditHistory,
  };

  return (
    <div className={className}>
      <div role="tablist" aria-label="Disclosure level" className="flex gap-1 border-b border-border">
        {LEVELS.map((entry) => (
          <button
            key={entry.key}
            type="button"
            role="tab"
            aria-selected={level === entry.key}
            onClick={() => setLevel(entry.key)}
            className={cn(
              "rounded-t-md px-3 py-1.5 text-xs font-semibold transition",
              level === entry.key
                ? "border border-b-0 border-border bg-surface text-foreground"
                : "text-muted-foreground hover:text-foreground",
            )}
          >
            {entry.label}
          </button>
        ))}
      </div>
      <div role="tabpanel" className="pt-3">
        {content[level]}
      </div>
    </div>
  );
}
