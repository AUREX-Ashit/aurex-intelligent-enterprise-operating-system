"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormField, FormLabel, FormBanner } from "@/components/ui/Form";
import { useLogin } from "@/features/auth/state/useLogin";

export function LoginForm() {
  const { state, submit, selectOrganization } = useLogin();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const isSubmitting = state.status === "submitting";
  const isSelectingOrganization = state.status === "selecting-organization";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    submit(email, password);
  }

  return (
    <Card className="w-full max-w-sm">
      <CardTitle>Platform Administrator</CardTitle>
      <CardDescription>Sign in to access the administrator workspace.</CardDescription>

      {!isSelectingOrganization && (
        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <FormField>
            <FormLabel htmlFor="login-email">Email</FormLabel>
            <Input
              id="login-email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="name@corpstage.com"
              autoComplete="email"
              required
              disabled={isSubmitting}
            />
          </FormField>

          <FormField>
            <FormLabel htmlFor="login-password">Password</FormLabel>
            <Input
              id="login-password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete="current-password"
              required
              minLength={8}
              disabled={isSubmitting}
            />
          </FormField>

          {state.status === "error" && <FormBanner tone="danger">{state.message}</FormBanner>}

          <Button
            type="submit"
            className="w-full"
            disabled={isSubmitting || email.length === 0 || password.length < 8}
          >
            {isSubmitting && <Spinner className="mr-2" />}
            Sign in
          </Button>
        </form>
      )}

      {isSelectingOrganization && (
        <div className="mt-6 space-y-3">
          <FormBanner tone="info">This account belongs to more than one organization.</FormBanner>

          <div className="space-y-2">
            {state.organizations.map((organization) => (
              <button
                key={organization.organization_id}
                type="button"
                onClick={() => selectOrganization(organization.organization_id)}
                className="flex w-full items-center justify-between rounded-md border border-border bg-surface px-4 py-3 text-left text-sm font-medium text-foreground transition hover:border-brand hover:bg-surface-muted"
              >
                <span>{organization.organization_name}</span>
                <span className="text-xs font-semibold text-muted-foreground">
                  {organization.role_code}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}
