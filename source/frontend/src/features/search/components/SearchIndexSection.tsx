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
import type { IndexEstablishState, IndexListState } from "@/features/search/state/useSearchManagement";
import type { EstablishIndexConfigurationRequest } from "@/types/search";

const RETRIEVAL_MODES: EstablishIndexConfigurationRequest["retrieval_mode"][] = ["HYBRID", "SEMANTIC", "LEXICAL"];

/** WP-11 BA-01 — Establish Enterprise Search Index Configuration. */
export function SearchIndexSection({
  establishState,
  listState,
  onEstablish,
  onLoad,
}: {
  establishState: IndexEstablishState;
  listState: IndexListState;
  onEstablish: (request: EstablishIndexConfigurationRequest) => void;
  onLoad: () => void;
}) {
  const [indexName, setIndexName] = useState("");
  const [embeddingModel, setEmbeddingModel] = useState("text-embedding-3-large");
  const [embeddingDimension, setEmbeddingDimension] = useState("1536");
  const [retrievalMode, setRetrievalMode] = useState<EstablishIndexConfigurationRequest["retrieval_mode"]>("HYBRID");
  const isLoading = establishState.status === "establishing";

  useEffect(() => {
    onLoad();
    // Loads once on mount — onLoad is a stable useCallback identity.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const dimension = Number.parseInt(embeddingDimension, 10);
    if (!indexName.trim() || Number.isNaN(dimension) || dimension <= 0) return;
    onEstablish({
      index_name: indexName.trim(),
      embedding_model: embeddingModel.trim(),
      embedding_dimension: dimension,
      retrieval_mode: retrievalMode,
      platform_wide: false,
    });
    setIndexName("");
  }

  return (
    <Card>
      <CardTitle>Search Index Configuration</CardTitle>
      <CardDescription>
        Establish a real, tenant-scoped Enterprise Search index (WP-11 BA-01, C-093) — the governed
        configuration every query and content registration executes against.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="search-index-name">Index name</FormLabel>
          <Input
            id="search-index-name"
            value={indexName}
            onChange={(event) => setIndexName(event.target.value)}
            placeholder="e.g. enterprise-knowledge-v1"
            required
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="search-embedding-model">Embedding model</FormLabel>
          <Input
            id="search-embedding-model"
            value={embeddingModel}
            onChange={(event) => setEmbeddingModel(event.target.value)}
            required
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="search-embedding-dimension">Embedding dimension</FormLabel>
          <Input
            id="search-embedding-dimension"
            type="number"
            min={1}
            value={embeddingDimension}
            onChange={(event) => setEmbeddingDimension(event.target.value)}
            required
            disabled={isLoading}
          />
          <FormHelperText>Content registered against this index must produce embeddings of this exact dimension.</FormHelperText>
        </FormField>

        <FormField>
          <FormLabel>Retrieval mode</FormLabel>
          <div className="flex flex-wrap gap-2">
            {RETRIEVAL_MODES.map((mode) => (
              <Button
                key={mode}
                type="button"
                variant={retrievalMode === mode ? "primary" : "secondary"}
                onClick={() => setRetrievalMode(mode)}
                disabled={isLoading}
              >
                {mode}
              </Button>
            ))}
          </div>
        </FormField>

        <Button type="submit" disabled={isLoading || indexName.trim().length === 0}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Index
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
            Index &ldquo;{establishState.index.index_name}&rdquo; established — {establishState.index.embedding_dimension}{" "}
            dimensions, {establishState.index.retrieval_mode}.
          </FormBanner>
        </div>
      )}

      <div className="mt-6">
        <h3 className="text-sm font-semibold text-foreground">Visible indexes</h3>
        {listState.status === "idle" || listState.status === "loading" ? (
          <LoadingState label="Loading index configurations…" />
        ) : listState.status === "error" ? (
          <div className="mt-3 space-y-3">
            <FormBanner tone="danger">{listState.message}</FormBanner>
            <Button type="button" variant="secondary" onClick={onLoad}>
              Retry
            </Button>
          </div>
        ) : listState.indexConfigurations.length === 0 ? (
          <p className="py-6 text-center text-sm text-muted-foreground">
            No search index has been established yet — establish one above before registering content.
          </p>
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableHeaderCell>Index name</TableHeaderCell>
                <TableHeaderCell>Scope</TableHeaderCell>
                <TableHeaderCell>Retrieval mode</TableHeaderCell>
                <TableHeaderCell>Dimension</TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {listState.indexConfigurations.map((index) => (
                <TableRow key={index.vector_index_id}>
                  <TableCell>{index.index_name}</TableCell>
                  <TableCell>
                    <StatusBadge tone={index.organization_id ? "brand" : "muted"}>
                      {index.organization_id ? "Tenant-dedicated" : "Platform-wide"}
                    </StatusBadge>
                  </TableCell>
                  <TableCell>{index.retrieval_mode}</TableCell>
                  <TableCell>{index.embedding_dimension}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </Card>
  );
}
