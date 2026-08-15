"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { LoadingState } from "@/components/ui/LoadingState";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { KnowledgeAssetRetrieveState } from "@/features/knowledge-asset/state/useKnowledgeAssetManagement";
import type { KnowledgeAssetResponse } from "@/types/knowledge-asset";

/**
 * WP-14 BA-04 — Knowledge Asset status view. Displays only fields the
 * BA-04 API contract actually exposes (schemas/knowledge_asset.py) — no
 * invented status semantics, no lifecycle-transition affordance (Charter
 * §9's own transition graph is deliberately left unresolved and is not
 * built here). Automatically shows the just-established asset; a caller
 * may also look up any other Knowledge Asset id visible to their own
 * Organization via the same GET endpoint (scoped server-side — this
 * screen never lets a caller select or override tenant identity).
 */
const CURATION_STATUS_TONE: Record<string, "info" | "brand" | "success" | "danger" | "muted"> = {
  PROPOSED: "info",
  VALIDATED: "brand",
  ACCEPTED: "success",
  REJECTED: "danger",
  SUPERSEDED: "muted",
};

function KnowledgeAssetDetails({ asset }: { asset: KnowledgeAssetResponse }) {
  return (
    <dl className="grid grid-cols-1 gap-x-6 gap-y-3 text-sm sm:grid-cols-2">
      <div>
        <dt className="text-muted-foreground">Knowledge Asset ID</dt>
        <dd className="font-mono text-xs text-foreground">{asset.knowledge_asset_id}</dd>
      </div>
      <div>
        <dt className="text-muted-foreground">Curation status</dt>
        <dd>
          <StatusBadge tone={CURATION_STATUS_TONE[asset.curation_status] ?? "muted"}>
            {asset.curation_status}
          </StatusBadge>
        </dd>
      </div>
      <div>
        <dt className="text-muted-foreground">Name</dt>
        <dd className="text-foreground">{asset.knowledge_asset_name ?? "—"}</dd>
      </div>
      <div>
        <dt className="text-muted-foreground">Type</dt>
        <dd className="text-foreground">{asset.knowledge_asset_type ?? "—"}</dd>
      </div>
      <div className="sm:col-span-2">
        <dt className="text-muted-foreground">Provenance reference</dt>
        <dd className="text-foreground">{asset.provenance_reference ?? "—"}</dd>
      </div>
      <div>
        <dt className="text-muted-foreground">Active</dt>
        <dd>
          <StatusBadge tone={asset.active_flag ? "success" : "muted"}>
            {asset.active_flag ? "Active" : "Inactive"}
          </StatusBadge>
        </dd>
      </div>
      <div>
        <dt className="text-muted-foreground">Established</dt>
        <dd className="text-foreground">{new Date(asset.created_at).toLocaleString()}</dd>
      </div>
    </dl>
  );
}

export function KnowledgeAssetStatusSection({
  retrieveState,
  onRetrieve,
}: {
  retrieveState: KnowledgeAssetRetrieveState;
  onRetrieve: (knowledgeAssetId: string) => void;
}) {
  const [lookupId, setLookupId] = useState("");
  const isLoading = retrieveState.status === "retrieving";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!lookupId.trim()) return;
    onRetrieve(lookupId.trim());
  }

  return (
    <Card>
      <CardTitle>Knowledge Asset Status</CardTitle>
      <CardDescription>
        View a Knowledge Asset established within your own Organization by its own id — visible to no
        other Organization (WP-14 BA-04, C-091).
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 flex flex-wrap items-end gap-3">
        <FormField className="flex-1 min-w-[16rem]">
          <FormLabel htmlFor="knowledge-asset-lookup-id">Knowledge Asset ID</FormLabel>
          <Input
            id="knowledge-asset-lookup-id"
            value={lookupId}
            onChange={(event) => setLookupId(event.target.value)}
            placeholder="e.g. the id shown after establishing one above"
            disabled={isLoading}
          />
        </FormField>
        <Button type="submit" variant="secondary" disabled={isLoading || lookupId.trim().length === 0}>
          Look up
        </Button>
      </form>

      <div className="mt-6">
        {retrieveState.status === "idle" && (
          <p className="py-6 text-center text-sm text-muted-foreground">
            No Knowledge Asset established or looked up yet.
          </p>
        )}
        {isLoading && <LoadingState label="Loading Knowledge Asset…" />}
        {retrieveState.status === "retrieve-error" && (
          <FormBanner tone="danger">{retrieveState.message}</FormBanner>
        )}
        {retrieveState.status === "retrieved" && <KnowledgeAssetDetails asset={retrieveState.asset} />}
      </div>
    </Card>
  );
}
