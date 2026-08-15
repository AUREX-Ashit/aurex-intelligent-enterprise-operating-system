"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormHelperText, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { IntelligenceCandidateResolveState } from "@/features/intelligence-candidate/state/useIntelligenceCandidateManagement";
import { RESOLUTION_OUTCOMES, type ResolveIntelligenceCandidateRequest } from "@/types/intelligence-candidate";

/**
 * WP-14 BA-03 — Resolve Enterprise Intelligence Candidate (Convergence
 * Decision). Only the fields the backend contract actually accepts
 * (schemas/unclassified_intelligence.py::ResolveIntelligenceCandidateRequest)
 * are collected. `organization_id` is never collected here — derived
 * server-side from the caller's own authenticated session.
 *
 * Resolves a candidate by its own id, entered directly — there is no
 * browsable resolution queue here. `IRA-014 §6` BA-03's own Frontend/UX
 * row names "a resolution queue," but its own "APIs/services required"
 * row names only the resolve endpoint, no list/GET — building a real
 * queue would require an API surface `IRA-014` never authorizes anywhere
 * for this Business Activity. This screen implements the minimum
 * defensible reading (resolve-by-id, mirroring `KnowledgeAssetStatusSection`'s
 * own established "look up by id" precedent), and this gap is explicitly
 * disclosed — not silently resolved by inventing a new endpoint.
 *
 * Gate 2 V&V remediation, Finding 2: the confirmation state now surfaces
 * `same_organization_duplicate_customer_metric_id` — a real backend signal
 * (Gate 1 Finding 2's own corrected surface for a same-Organization Tenant
 * CDE name duplicate) that was computed and returned by the API but never
 * displayed here. `semantic_match_result_metric_id` remains intentionally
 * unread by this component — it is contractually reserved for a Global
 * `metric_registry` match this implementation can never produce (see the
 * service module's own docstring) and is always `null`; displaying it
 * would show nothing meaningful and risk being read as "no Global match
 * exists," which this implementation cannot actually determine.
 */
export function ResolveIntelligenceCandidateSection({
  resolveState,
  onResolve,
}: {
  resolveState: IntelligenceCandidateResolveState;
  onResolve: (unclassifiedId: string, request: ResolveIntelligenceCandidateRequest) => void;
}) {
  const [unclassifiedId, setUnclassifiedId] = useState("");
  const [outcome, setOutcome] = useState<(typeof RESOLUTION_OUTCOMES)[number]>("NEW_CDE_CREATED");
  const [metricId, setMetricId] = useState("");
  const [metricName, setMetricName] = useState("");
  const [metricCode, setMetricCode] = useState("");
  const [unitOfMeasure, setUnitOfMeasure] = useState("");
  const isLoading = resolveState.status === "resolving";

  const canSubmit =
    unclassifiedId.trim().length > 0 &&
    (outcome === "DISCARDED" ||
      (outcome === "MAPPED_TO_EXISTING" && metricId.trim().length > 0) ||
      (outcome === "NEW_CDE_CREATED" && metricName.trim().length > 0 && metricCode.trim().length > 0));

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) return;
    const request: ResolveIntelligenceCandidateRequest =
      outcome === "MAPPED_TO_EXISTING"
        ? { outcome, metric_id: metricId.trim() }
        : outcome === "NEW_CDE_CREATED"
          ? {
              outcome,
              metric_name: metricName.trim(),
              metric_code: metricCode.trim(),
              unit_of_measure: unitOfMeasure.trim() || null,
            }
          : { outcome };
    onResolve(unclassifiedId.trim(), request);
  }

  return (
    <Card>
      <CardTitle>Resolve Intelligence Candidate</CardTitle>
      <CardDescription>
        Resolve a pending candidate to exactly one outcome — mapped to an existing Canonical Data
        Element, a new one created, or discarded (WP-14 BA-03, C-090).
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="resolve-candidate-id">Candidate ID</FormLabel>
          <Input
            id="resolve-candidate-id"
            value={unclassifiedId}
            onChange={(event) => setUnclassifiedId(event.target.value)}
            placeholder="e.g. the id shown after registering a candidate"
            required
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel>Outcome</FormLabel>
          <div className="flex flex-wrap gap-2">
            {RESOLUTION_OUTCOMES.map((value) => (
              <Button
                key={value}
                type="button"
                variant={outcome === value ? "primary" : "secondary"}
                onClick={() => setOutcome(value)}
                disabled={isLoading}
              >
                {value}
              </Button>
            ))}
          </div>
        </FormField>

        {outcome === "MAPPED_TO_EXISTING" && (
          <FormField>
            <FormLabel htmlFor="resolve-metric-id">Existing metric ID</FormLabel>
            <Input
              id="resolve-metric-id"
              value={metricId}
              onChange={(event) => setMetricId(event.target.value)}
              required
              disabled={isLoading}
            />
          </FormField>
        )}

        {outcome === "NEW_CDE_CREATED" && (
          <>
            <FormField>
              <FormLabel htmlFor="resolve-metric-name">Metric name</FormLabel>
              <Input
                id="resolve-metric-name"
                value={metricName}
                onChange={(event) => setMetricName(event.target.value)}
                placeholder="e.g. Board Independence Ratio"
                required
                disabled={isLoading}
              />
            </FormField>
            <FormField>
              <FormLabel htmlFor="resolve-metric-code">Metric code</FormLabel>
              <Input
                id="resolve-metric-code"
                value={metricCode}
                onChange={(event) => setMetricCode(event.target.value)}
                placeholder="e.g. BOARD_INDEPENDENCE_RATIO"
                required
                disabled={isLoading}
              />
            </FormField>
            <FormField>
              <FormLabel htmlFor="resolve-unit-of-measure">Unit of measure</FormLabel>
              <Input
                id="resolve-unit-of-measure"
                value={unitOfMeasure}
                onChange={(event) => setUnitOfMeasure(event.target.value)}
                placeholder="e.g. %"
                disabled={isLoading}
              />
              <FormHelperText>Optional.</FormHelperText>
            </FormField>
          </>
        )}

        <Button type="submit" disabled={isLoading || !canSubmit}>
          {isLoading && <Spinner className="mr-2" />}
          Resolve Candidate
        </Button>
      </form>

      {resolveState.status === "resolve-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{resolveState.message}</FormBanner>
        </div>
      )}
      {resolveState.status === "resolved" && (
        <div className="mt-4 space-y-3">
          <FormBanner tone="success">Candidate resolved.</FormBanner>
          <dl className="grid grid-cols-1 gap-x-6 gap-y-3 text-sm sm:grid-cols-2">
            <div>
              <dt className="text-muted-foreground">Resolution status</dt>
              <dd>
                <StatusBadge tone="info">{resolveState.result.resolution_status}</StatusBadge>
              </dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Semantic Matching attempted</dt>
              <dd className="text-foreground">
                {resolveState.result.semantic_match_attempted_flag === null
                  ? "—"
                  : resolveState.result.semantic_match_attempted_flag
                    ? "Yes"
                    : "No"}
              </dd>
            </div>
            {resolveState.result.resolved_customer_metric_id && (
              <div className="sm:col-span-2">
                <dt className="text-muted-foreground">New Customer Metric ID</dt>
                <dd className="font-mono text-xs text-foreground">
                  {resolveState.result.resolved_customer_metric_id}
                </dd>
              </div>
            )}
            {resolveState.result.same_organization_duplicate_customer_metric_id && (
              <div className="sm:col-span-2 space-y-2">
                <dt className="text-muted-foreground">Same-Organization Duplicate Candidate</dt>
                <dd>
                  <FormBanner tone="warning">
                    A Customer Metric with this name already exists in your own Organization. This is
                    a same-Organization duplicate signal, distinct from a Global canonical library
                    match (Semantic Matching cannot see the Global library in this implementation —
                    see the newly created CDE below, which was still created as requested).
                  </FormBanner>
                  <span className="mt-1 block font-mono text-xs text-foreground">
                    {resolveState.result.same_organization_duplicate_customer_metric_id}
                  </span>
                </dd>
              </div>
            )}
            {resolveState.result.evidence_id && (
              <div className="sm:col-span-2">
                <dt className="text-muted-foreground">Evidence ID</dt>
                <dd className="font-mono text-xs text-foreground">{resolveState.result.evidence_id}</dd>
              </div>
            )}
          </dl>
        </div>
      )}
    </Card>
  );
}
