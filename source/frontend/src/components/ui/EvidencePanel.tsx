import type { ReactNode } from "react";
import { ProgressiveDisclosure } from "@/components/ui/ProgressiveDisclosure";
import { StatusBadge } from "@/components/ui/StatusBadge";

/**
 * Evidence Panel — DS-001's reference Progressive Disclosure widget
 * (`SD-001-020`, `IMP-001 §10.4`). Renders confidence score and evidence
 * reference at Summary level by default, expands to the full evidence
 * chain on user interaction (Evidence state). Read-only, consuming form
 * only — never a data-collecting form (`IMP-FE-002`), correct for every
 * caller in this repository so far, since no Sacred 12 screen exists
 * that would render this component. First conforming implementation
 * anywhere in this repository (`SER-001 SE-007`, `IRA-012 §4.4`).
 */
export interface EvidencePanelAuditEntry {
  label: string;
  timestamp: string;
}

export interface EvidencePanelProps {
  confidenceScore: number | null;
  evidenceReference: string | null;
  detailsContent?: ReactNode;
  auditTrail?: EvidencePanelAuditEntry[];
}

export function EvidencePanel({
  confidenceScore,
  evidenceReference,
  detailsContent,
  auditTrail = [],
}: EvidencePanelProps) {
  const confidenceTone = confidenceScore === null ? "muted" : confidenceScore >= 70 ? "success" : "warning";

  return (
    <ProgressiveDisclosure
      summary={
        <div className="flex flex-wrap items-center gap-2">
          <StatusBadge tone={confidenceTone}>
            {confidenceScore === null ? "Confidence not available" : `Confidence ${confidenceScore}%`}
          </StatusBadge>
          {evidenceReference && (
            <span className="text-xs text-muted-foreground">{evidenceReference}</span>
          )}
        </div>
      }
      details={
        detailsContent ?? (
          <p className="text-sm text-muted-foreground">No additional detail recorded for this output.</p>
        )
      }
      evidence={
        evidenceReference ? (
          <p className="text-sm text-foreground">{evidenceReference}</p>
        ) : (
          <p className="text-sm text-muted-foreground">
            No evidence reference recorded — this output is a disclosed placeholder, not a computed answer.
          </p>
        )
      }
      auditHistory={
        auditTrail.length === 0 ? (
          <p className="text-sm text-muted-foreground">No audit history recorded.</p>
        ) : (
          <ul className="space-y-1">
            {auditTrail.map((entry, index) => (
              <li key={index} className="text-xs text-muted-foreground">
                {entry.timestamp} — {entry.label}
              </li>
            ))}
          </ul>
        )
      }
    />
  );
}
