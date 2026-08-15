"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormHelperText, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import type { KnowledgeAssetEstablishState } from "@/features/knowledge-asset/state/useKnowledgeAssetManagement";
import type { EstablishKnowledgeAssetRequest } from "@/types/knowledge-asset";

/**
 * WP-14 BA-04 — Establish Knowledge Asset. Only the fields the backend
 * contract actually accepts (schemas/knowledge_asset.py) are collected.
 * `organization_id` is never collected here — it is derived server-side
 * from the caller's own authenticated session, never supplied by the
 * user (Charter §6/§11; mirrors establish_configuration's own precedent).
 * `source_ingestion_id`/`confidence_rule_id` are intentionally not
 * exposed as inputs — both remain nullable, optional backend fields with
 * no physical target table anywhere yet (Charter §16), not a decision
 * this screen makes.
 */
export function EstablishKnowledgeAssetSection({
  establishState,
  onEstablish,
}: {
  establishState: KnowledgeAssetEstablishState;
  onEstablish: (request: EstablishKnowledgeAssetRequest) => void;
}) {
  const [knowledgeAssetName, setKnowledgeAssetName] = useState("");
  const [knowledgeAssetType, setKnowledgeAssetType] = useState("");
  const [provenanceReference, setProvenanceReference] = useState("");
  const [lastHandledStatus, setLastHandledStatus] = useState(establishState.status);
  const isLoading = establishState.status === "establishing";

  // Fields are cleared only once establishment actually succeeds (F2
  // remediation) — derived during render, not in an effect, so a failed
  // submission's entered values survive untouched for the caller to
  // correct and resubmit without retyping everything.
  if (establishState.status !== lastHandledStatus) {
    setLastHandledStatus(establishState.status);
    if (establishState.status === "established") {
      setKnowledgeAssetName("");
      setKnowledgeAssetType("");
      setProvenanceReference("");
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!provenanceReference.trim()) return;
    onEstablish({
      knowledge_asset_name: knowledgeAssetName.trim() || null,
      knowledge_asset_type: knowledgeAssetType.trim() || null,
      provenance_reference: provenanceReference.trim(),
    });
  }

  return (
    <Card>
      <CardTitle>Establish Knowledge Asset</CardTitle>
      <CardDescription>
        Curate a Signal into a governed Knowledge Asset, carrying Provenance from first existence (WP-14
        BA-04, C-091).
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="knowledge-asset-name">Knowledge Asset name</FormLabel>
          <Input
            id="knowledge-asset-name"
            value={knowledgeAssetName}
            onChange={(event) => setKnowledgeAssetName(event.target.value)}
            placeholder="e.g. Board Independence Ratio — FY25"
            disabled={isLoading}
          />
          <FormHelperText>Optional — not required by the governing schema.</FormHelperText>
        </FormField>

        <FormField>
          <FormLabel htmlFor="knowledge-asset-type">Knowledge Asset type</FormLabel>
          <Input
            id="knowledge-asset-type"
            value={knowledgeAssetType}
            onChange={(event) => setKnowledgeAssetType(event.target.value)}
            placeholder="e.g. fact, relationship, summary, narrative-fragment"
            disabled={isLoading}
          />
          <FormHelperText>Optional — not required by the governing schema.</FormHelperText>
        </FormField>

        <FormField>
          <FormLabel htmlFor="knowledge-asset-provenance">Provenance reference</FormLabel>
          <Input
            id="knowledge-asset-provenance"
            value={provenanceReference}
            onChange={(event) => setProvenanceReference(event.target.value)}
            placeholder="e.g. governance-report-fy25.pdf#p12"
            required
            disabled={isLoading}
          />
          <FormHelperText>
            Mandatory — &ldquo;no Knowledge Asset without Provenance&rdquo; (EIA-001 Vol. I §7.3).
          </FormHelperText>
        </FormField>

        <Button type="submit" disabled={isLoading || provenanceReference.trim().length === 0}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Knowledge Asset
        </Button>
      </form>

      {establishState.status === "establish-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{establishState.message}</FormBanner>
        </div>
      )}
      {establishState.status === "established" && (
        <div className="mt-4">
          <FormBanner tone="success">
            Knowledge Asset established — status {establishState.asset.curation_status}. See Status
            below.
          </FormBanner>
        </div>
      )}
    </Card>
  );
}
