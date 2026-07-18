"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner } from "@/components/ui/Form";
import type { PersonManagementState } from "@/features/person/state/usePersonManagement";

interface RecognizePersonSectionProps {
  state: PersonManagementState;
  onRecognize: (email: string) => void;
}

export function RecognizePersonSection({ state, onRecognize }: RecognizePersonSectionProps) {
  const [email, setEmail] = useState("");
  const isLoading = state.status === "recognizing";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onRecognize(email);
  }

  return (
    <Card>
      <CardTitle>Recognize Existing Person</CardTitle>
      <CardDescription>Check whether a person is already known, by email.</CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 flex items-end gap-3">
        <FormField className="flex-1">
          <FormLabel htmlFor="recognize-email">Email</FormLabel>
          <Input
            id="recognize-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="name@company.com"
            autoComplete="email"
            required
            disabled={isLoading}
          />
        </FormField>

        <Button type="submit" disabled={isLoading || email.length === 0}>
          {isLoading && <Spinner className="mr-2" />}
          Recognize
        </Button>
      </form>

      {state.status === "recognize-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}

      {state.status === "matched" && (
        <div className="mt-4">
          <FormBanner tone="success">✓ Existing Person Found</FormBanner>
        </div>
      )}

      {state.status === "no-candidate" && (
        <div className="mt-4">
          <FormBanner tone="warning">No existing Person found.</FormBanner>
        </div>
      )}
    </Card>
  );
}
