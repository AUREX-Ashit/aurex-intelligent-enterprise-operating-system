"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormHelperText, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { IntelligenceCandidateRegisterState } from "@/features/intelligence-candidate/state/useIntelligenceCandidateManagement";
import { ALLOWED_EXTRACTION_METHODS, type RegisterIntelligenceCandidateRequest } from "@/types/intelligence-candidate";

/**
 * WP-14 BA-02 — Register Enterprise Intelligence Candidate. Only the
 * fields the backend contract actually accepts
 * (schemas/unclassified_intelligence.py) are collected. `organization_id`
 * is never collected here — derived server-side from the caller's own
 * authenticated session, mirroring `EstablishKnowledgeAssetSection.tsx`'s
 * own established precedent. `extraction_method` is restricted to the two
 * values this Business Activity accepts (`MANUAL_ENTRY`/`API_INGEST`) —
 * the five automated values require a live extraction pipeline this
 * Business Activity does not build (`IRA-014 §5.2`). Fields clear only on
 * success, mirroring BA-04's own F2-corrected precedent — a failed
 * registration preserves the caller's entered values for correction.
 */
export function IntelligenceCandidateSection({
  registerState,
  onRegister,
}: {
  registerState: IntelligenceCandidateRegisterState;
  onRegister: (request: RegisterIntelligenceCandidateRequest) => void;
}) {
  const [rawExtractedValue, setRawExtractedValue] = useState("");
  const [sourceDocumentReference, setSourceDocumentReference] = useState("");
  const [sourcePageSection, setSourcePageSection] = useState("");
  const [extractionMethod, setExtractionMethod] =
    useState<RegisterIntelligenceCandidateRequest["extraction_method"]>("MANUAL_ENTRY");
  const [lastHandledStatus, setLastHandledStatus] = useState(registerState.status);
  const isLoading = registerState.status === "registering";

  if (registerState.status !== lastHandledStatus) {
    setLastHandledStatus(registerState.status);
    if (registerState.status === "registered") {
      setRawExtractedValue("");
      setSourceDocumentReference("");
      setSourcePageSection("");
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!rawExtractedValue.trim() || !sourceDocumentReference.trim()) return;
    onRegister({
      raw_extracted_value: rawExtractedValue.trim(),
      source_document_reference: sourceDocumentReference.trim(),
      source_page_section: sourcePageSection.trim() || null,
      extraction_method: extractionMethod,
    });
  }

  return (
    <Card>
      <CardTitle>Register Enterprise Intelligence Candidate</CardTitle>
      <CardDescription>
        Capture a raw extracted fact with no matching Canonical Data Element, so it is never
        discarded (WP-14 BA-02, C-090).
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="candidate-raw-value">Raw extracted value</FormLabel>
          <Input
            id="candidate-raw-value"
            value={rawExtractedValue}
            onChange={(event) => setRawExtractedValue(event.target.value)}
            placeholder="e.g. Board independence ratio: 62%"
            required
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="candidate-source-reference">Source document reference</FormLabel>
          <Input
            id="candidate-source-reference"
            value={sourceDocumentReference}
            onChange={(event) => setSourceDocumentReference(event.target.value)}
            placeholder="e.g. governance-report-fy25.pdf"
            required
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="candidate-source-section">Source page/section</FormLabel>
          <Input
            id="candidate-source-section"
            value={sourcePageSection}
            onChange={(event) => setSourcePageSection(event.target.value)}
            placeholder="e.g. p.12"
            disabled={isLoading}
          />
          <FormHelperText>Optional — not required by the governing schema.</FormHelperText>
        </FormField>

        <FormField>
          <FormLabel>Extraction method</FormLabel>
          <div className="flex flex-wrap gap-2">
            {ALLOWED_EXTRACTION_METHODS.map((method) => (
              <Button
                key={method}
                type="button"
                variant={extractionMethod === method ? "primary" : "secondary"}
                onClick={() => setExtractionMethod(method)}
                disabled={isLoading}
              >
                {method}
              </Button>
            ))}
          </div>
          <FormHelperText>
            Automated extraction methods require a live Discovery Provider connection, not built by
            this Business Activity.
          </FormHelperText>
        </FormField>

        <Button
          type="submit"
          disabled={isLoading || !rawExtractedValue.trim() || !sourceDocumentReference.trim()}
        >
          {isLoading && <Spinner className="mr-2" />}
          Register Candidate
        </Button>
      </form>

      {registerState.status === "register-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{registerState.message}</FormBanner>
        </div>
      )}
      {registerState.status === "registered" && (
        <div className="mt-4 space-y-3">
          <FormBanner tone="success">Intelligence candidate registered.</FormBanner>
          <dl className="grid grid-cols-1 gap-x-6 gap-y-3 text-sm sm:grid-cols-2">
            <div>
              <dt className="text-muted-foreground">Candidate ID</dt>
              <dd className="font-mono text-xs text-foreground">{registerState.candidate.unclassified_id}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Resolution status</dt>
              <dd>
                <StatusBadge tone="info">{registerState.candidate.resolution_status}</StatusBadge>
              </dd>
            </div>
            <div className="sm:col-span-2">
              <dt className="text-muted-foreground">Raw extracted value</dt>
              <dd className="text-foreground">{registerState.candidate.raw_extracted_value}</dd>
            </div>
          </dl>
        </div>
      )}
    </Card>
  );
}
