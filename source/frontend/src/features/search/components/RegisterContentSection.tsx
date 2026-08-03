"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormHelperText, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import type { RegisterContentState } from "@/features/search/state/useSearchManagement";
import type { RegisterContentRequest } from "@/types/search";

/** WP-11 BA-03 — Register Enterprise Search Content (deliberately narrow: pre-extracted text only, IRA-011 §4.2). */
export function RegisterContentSection({
  state,
  onRegister,
}: {
  state: RegisterContentState;
  onRegister: (request: RegisterContentRequest) => void;
}) {
  const [indexName, setIndexName] = useState("");
  const [text, setText] = useState("");
  const [evidenceSource, setEvidenceSource] = useState("");
  const [fileReference, setFileReference] = useState("");
  const isLoading = state.status === "registering";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!indexName.trim() || !text.trim()) return;
    onRegister({
      index_name: indexName.trim(),
      text: text.trim(),
      evidence_source: evidenceSource.trim() || null,
      file_reference: fileReference.trim() || null,
    });
    setText("");
  }

  return (
    <Card>
      <CardTitle>Register Searchable Content</CardTitle>
      <CardDescription>
        Registers a text passage as searchable evidence under an established index (WP-11 BA-03). Accepts
        pre-extracted text only — no file upload or document ingestion in this release.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="register-index-name">Target index</FormLabel>
          <Input
            id="register-index-name"
            value={indexName}
            onChange={(event) => setIndexName(event.target.value)}
            placeholder="Index name established above"
            required
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="register-text">Text passage</FormLabel>
          <textarea
            id="register-text"
            className="w-full rounded-md border border-border bg-surface px-3 py-2 text-sm text-foreground"
            rows={4}
            value={text}
            onChange={(event) => setText(event.target.value)}
            required
            disabled={isLoading}
          />
          <FormHelperText>The passage becomes searchable — split into fixed-size chunks, no configurable strategy this release.</FormHelperText>
        </FormField>

        <FormField>
          <FormLabel htmlFor="register-source">Evidence source</FormLabel>
          <Input
            id="register-source"
            value={evidenceSource}
            onChange={(event) => setEvidenceSource(event.target.value)}
            placeholder="e.g. Annual Governance Report FY25"
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="register-locator">File reference</FormLabel>
          <Input
            id="register-locator"
            value={fileReference}
            onChange={(event) => setFileReference(event.target.value)}
            placeholder="A locator string — not a file upload"
            disabled={isLoading}
          />
        </FormField>

        <Button type="submit" disabled={isLoading || !indexName.trim() || !text.trim()}>
          {isLoading && <Spinner className="mr-2" />}
          Register Content
        </Button>
      </form>

      {state.status === "register-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}
      {state.status === "registered" && (
        <div className="mt-4">
          <FormBanner tone="success">
            Registered {state.result.chunk_count} chunk(s) as searchable content.
          </FormBanner>
        </div>
      )}
    </Card>
  );
}
