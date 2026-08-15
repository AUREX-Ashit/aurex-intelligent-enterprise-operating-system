"use client";

import { useEffect, useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormHelperText, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { LoadingState } from "@/components/ui/LoadingState";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Table, TableBody, TableCell, TableHead, TableHeaderCell, TableRow } from "@/components/ui/Table";
import type {
  DiscoveryProviderEstablishState,
  DiscoveryProviderListState,
} from "@/features/discovery-provider/state/useDiscoveryProviderManagement";
import {
  DISCOVERY_CADENCES,
  PROVIDER_TYPES_BY_CATEGORY,
  type EstablishDiscoveryProviderRequest,
  type ProviderCategory,
} from "@/types/discovery-provider";

const PROVIDER_CATEGORIES: ProviderCategory[] = ["ENTERPRISE", "EXTERNAL", "REALTIME"];

/**
 * WP-14 BA-01 — Establish Discovery Provider Configuration. Only the
 * fields the backend contract actually accepts (schemas/discovery_provider.py)
 * are collected. `organization_id` is never collected here — derived
 * server-side from the caller's own authenticated session (Charter §11 of
 * WP-11 BA-01's own established precedent, `SearchIndexSection.tsx`).
 * `platform_wide` is not exposed as a form control — mirrors
 * `SearchIndexSection.tsx`'s own identical precedent (always `false` from
 * this form); establishing a platform-wide provider is not part of this
 * Business Activity's own minimum UI scope. `credential_id`/
 * `governing_policy_id` are intentionally not exposed as inputs — both
 * remain nullable, optional backend fields with no physical target table
 * anywhere yet, not a decision this screen makes.
 */
export function DiscoveryProviderSection({
  establishState,
  listState,
  onEstablish,
  onLoad,
}: {
  establishState: DiscoveryProviderEstablishState;
  listState: DiscoveryProviderListState;
  onEstablish: (request: EstablishDiscoveryProviderRequest) => void;
  onLoad: () => void;
}) {
  const [providerName, setProviderName] = useState("");
  const [providerCategory, setProviderCategory] = useState<ProviderCategory>("ENTERPRISE");
  const [providerType, setProviderType] = useState(PROVIDER_TYPES_BY_CATEGORY.ENTERPRISE[0]);
  const [discoveryCadence, setDiscoveryCadence] =
    useState<(typeof DISCOVERY_CADENCES)[number]>("ON_DEMAND");
  const isLoading = establishState.status === "establishing";

  useEffect(() => {
    onLoad();
    // Loads once on mount — onLoad is a stable useCallback identity.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleCategoryChange(category: ProviderCategory) {
    setProviderCategory(category);
    setProviderType(PROVIDER_TYPES_BY_CATEGORY[category][0]);
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onEstablish({
      provider_name: providerName.trim() || null,
      provider_category: providerCategory,
      provider_type: providerType,
      discovery_cadence: discoveryCadence,
      platform_wide: false,
    });
    setProviderName("");
  }

  return (
    <Card>
      <CardTitle>Discovery Provider Configuration</CardTitle>
      <CardDescription>
        Register a governed configuration for one Enterprise Intelligence discovery source, without
        requiring a live connection to it (WP-14 BA-01, C-090).
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="discovery-provider-name">Provider name</FormLabel>
          <Input
            id="discovery-provider-name"
            value={providerName}
            onChange={(event) => setProviderName(event.target.value)}
            placeholder="e.g. Finance SharePoint"
            disabled={isLoading}
          />
          <FormHelperText>Optional — not required by the governing schema.</FormHelperText>
        </FormField>

        <FormField>
          <FormLabel>Provider category</FormLabel>
          <div className="flex flex-wrap gap-2">
            {PROVIDER_CATEGORIES.map((category) => (
              <Button
                key={category}
                type="button"
                variant={providerCategory === category ? "primary" : "secondary"}
                onClick={() => handleCategoryChange(category)}
                disabled={isLoading}
              >
                {category}
              </Button>
            ))}
          </div>
        </FormField>

        <FormField>
          <FormLabel htmlFor="discovery-provider-type">Provider type</FormLabel>
          <select
            id="discovery-provider-type"
            value={providerType}
            onChange={(event) => setProviderType(event.target.value)}
            disabled={isLoading}
            className="h-10 w-full rounded-md border border-border bg-surface px-3 text-sm text-foreground outline-none transition focus:border-brand focus:ring-2 focus:ring-brand/20 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {PROVIDER_TYPES_BY_CATEGORY[providerCategory].map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
          <FormHelperText>Filtered to types valid for the selected category.</FormHelperText>
        </FormField>

        <FormField>
          <FormLabel>Discovery cadence</FormLabel>
          <div className="flex flex-wrap gap-2">
            {DISCOVERY_CADENCES.map((cadence) => (
              <Button
                key={cadence}
                type="button"
                variant={discoveryCadence === cadence ? "primary" : "secondary"}
                onClick={() => setDiscoveryCadence(cadence)}
                disabled={isLoading}
              >
                {cadence}
              </Button>
            ))}
          </div>
        </FormField>

        <Button type="submit" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Discovery Provider
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
            Discovery Provider &ldquo;{establishState.provider.provider_type}&rdquo; established.
          </FormBanner>
        </div>
      )}

      <div className="mt-6">
        <h3 className="text-sm font-semibold text-foreground">Visible Discovery Providers</h3>
        {listState.status === "idle" || listState.status === "loading" ? (
          <LoadingState label="Loading Discovery Providers…" />
        ) : listState.status === "error" ? (
          <div className="mt-3 space-y-3">
            <FormBanner tone="danger">{listState.message}</FormBanner>
            <Button type="button" variant="secondary" onClick={onLoad}>
              Retry
            </Button>
          </div>
        ) : listState.providers.length === 0 ? (
          <p className="py-6 text-center text-sm text-muted-foreground">
            No Discovery Provider has been established yet.
          </p>
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableHeaderCell>Provider</TableHeaderCell>
                <TableHeaderCell>Category</TableHeaderCell>
                <TableHeaderCell>Type</TableHeaderCell>
                <TableHeaderCell>Cadence</TableHeaderCell>
                <TableHeaderCell>Scope</TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {listState.providers.map((provider) => (
                <TableRow key={provider.discovery_provider_id}>
                  <TableCell>{provider.provider_name ?? "—"}</TableCell>
                  <TableCell>{provider.provider_category}</TableCell>
                  <TableCell>{provider.provider_type}</TableCell>
                  <TableCell>{provider.discovery_cadence}</TableCell>
                  <TableCell>
                    <StatusBadge tone={provider.organization_id ? "brand" : "muted"}>
                      {provider.organization_id ? "Tenant-dedicated" : "Platform-wide"}
                    </StatusBadge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </Card>
  );
}
