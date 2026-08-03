"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { SearchQueryState } from "@/features/search/state/useSearchManagement";
import type { ExecuteSearchRequest } from "@/types/search";

/**
 * WP-11 BA-02 — Execute Enterprise Search. The platform's first "ask a
 * question, get a cited answer" experience — narrow (only content
 * explicitly registered via BA-03 is searchable), disclosed as narrow.
 */
export function ExecuteSearchSection({
  state,
  onSearch,
}: {
  state: SearchQueryState;
  onSearch: (request: ExecuteSearchRequest) => void;
}) {
  const [query, setQuery] = useState("");
  const [indexName, setIndexName] = useState("");
  const isLoading = state.status === "searching";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!query.trim()) return;
    onSearch({ query: query.trim(), index_name: indexName.trim() || null, top_k: 5 });
  }

  return (
    <Card>
      <CardTitle>Ask Enterprise Search</CardTitle>
      <CardDescription>
        Ask a question across content registered via Enterprise Search (WP-11 BA-02, C-093) and receive
        evidence-cited results.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4" role="search">
        <FormField>
          <FormLabel htmlFor="search-query">Question</FormLabel>
          <Input
            id="search-query"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="e.g. What were our Scope 1 emissions?"
            required
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="search-index-target">Index (optional)</FormLabel>
          <Input
            id="search-index-target"
            value={indexName}
            onChange={(event) => setIndexName(event.target.value)}
            placeholder="Omit to use your own default index, if exactly one exists"
            disabled={isLoading}
          />
        </FormField>

        <Button type="submit" disabled={isLoading || query.trim().length === 0}>
          {isLoading && <Spinner className="mr-2" />}
          Search
        </Button>
      </form>

      {state.status === "search-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}

      {state.status === "searched" && (
        <div className="mt-6 space-y-3">
          {state.response.results.length === 0 ? (
            <p className="py-6 text-center text-sm text-muted-foreground">
              {state.response.message ?? "No matching references found."}
            </p>
          ) : (
            state.response.results.map((result) => (
              <div key={result.document_chunk_id} className="rounded-md border border-border p-4">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm text-foreground">{result.citation}</p>
                  <StatusBadge tone="muted">score {result.score.toFixed(2)}</StatusBadge>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </Card>
  );
}
