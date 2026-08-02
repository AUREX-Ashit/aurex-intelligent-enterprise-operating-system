"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner } from "@/components/ui/Form";
import { LoadingState } from "@/components/ui/LoadingState";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Table, TableBody, TableCell, TableHead, TableHeaderCell, TableRow } from "@/components/ui/Table";
import type { ConfigurationEntriesState } from "@/features/configuration/state/useConfigurationManagement";

export function ConfigurationEntriesSection({
  state,
  onLoad,
}: {
  state: ConfigurationEntriesState;
  onLoad: () => void;
}) {
  useEffect(() => {
    onLoad();
    // Loads once on mount — onLoad is a stable useCallback identity.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Card>
      <CardTitle>Established Configuration</CardTitle>
      <CardDescription>Every currently-active Configuration override for your Organization, across all facets.</CardDescription>

      <div className="mt-4">
        {state.status === "idle" || state.status === "loading" ? (
          <LoadingState label="Loading established Configuration…" />
        ) : state.status === "error" ? (
          <div className="space-y-3">
            <FormBanner tone="danger">{state.message}</FormBanner>
            <Button type="button" variant="secondary" onClick={onLoad}>
              Retry
            </Button>
          </div>
        ) : state.entries.length === 0 ? (
          <p className="py-8 text-center text-sm text-muted-foreground">
            No Configuration has been established yet — every facet resolves to its platform default.
          </p>
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableHeaderCell>Facet</TableHeaderCell>
                <TableHeaderCell>Key</TableHeaderCell>
                <TableHeaderCell>Value</TableHeaderCell>
                <TableHeaderCell>Version</TableHeaderCell>
                <TableHeaderCell>Effective From</TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {state.entries.map((entry) => (
                <TableRow key={entry.id}>
                  <TableCell>
                    <StatusBadge tone="brand">{entry.facet}</StatusBadge>
                  </TableCell>
                  <TableCell>{entry.key}</TableCell>
                  <TableCell>{String(entry.value)}</TableCell>
                  <TableCell>{entry.version}</TableCell>
                  <TableCell>{new Date(entry.effective_from).toLocaleString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </Card>
  );
}
