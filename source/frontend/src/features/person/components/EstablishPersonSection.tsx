"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner } from "@/components/ui/Form";
import type { PersonManagementState } from "@/features/person/state/usePersonManagement";
import type { EstablishPersonRequest } from "@/types/person";

interface EstablishPersonSectionProps {
  state: PersonManagementState;
  email: string;
  onEstablish: (fields: Omit<EstablishPersonRequest, "email">) => void;
}

export function EstablishPersonSection({ state, email, onEstablish }: EstablishPersonSectionProps) {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [displayName, setDisplayName] = useState("");
  const isLoading = state.status === "establishing";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onEstablish({ first_name: firstName, last_name: lastName, display_name: displayName });
  }

  return (
    <Card>
      <CardTitle>Establish Person</CardTitle>
      <CardDescription>
        No existing person matches <span className="font-semibold text-foreground">{email}</span>.
        Provide the minimal facts to establish one.
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel htmlFor="establish-first-name">First Name</FormLabel>
          <Input
            id="establish-first-name"
            value={firstName}
            onChange={(event) => setFirstName(event.target.value)}
            required
            minLength={1}
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="establish-last-name">Last Name</FormLabel>
          <Input
            id="establish-last-name"
            value={lastName}
            onChange={(event) => setLastName(event.target.value)}
            required
            minLength={1}
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="establish-display-name">Display Name</FormLabel>
          <Input
            id="establish-display-name"
            value={displayName}
            onChange={(event) => setDisplayName(event.target.value)}
            required
            minLength={1}
            disabled={isLoading}
          />
        </FormField>

        <FormField>
          <FormLabel htmlFor="establish-email">Email</FormLabel>
          <Input
            id="establish-email"
            type="email"
            value={email}
            readOnly
            disabled
            className="bg-surface-muted text-muted-foreground"
          />
        </FormField>

        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Person
        </Button>
      </form>

      {state.status === "establish-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}
    </Card>
  );
}
