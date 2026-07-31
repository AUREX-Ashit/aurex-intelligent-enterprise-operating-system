"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormLabel, FormHelperText } from "@/components/ui/Form";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { useEvaluateAccess } from "@/features/access-evaluation/state/useEvaluateAccess";
import type { DomainPermissionLevel } from "@/types/domain-permission";

const PERMISSION_LEVELS: DomainPermissionLevel[] = [
  "VIEW",
  "ENTER",
  "EDIT",
  "REVIEW",
  "APPROVE",
  "ASSIGN",
  "DELEGATE",
  "ADMIN",
];

export function AccessEvaluationScreen() {
  const { state, evaluate } = useEvaluateAccess();
  const [membershipId, setMembershipId] = useState("");
  const [domainId, setDomainId] = useState("");
  const [permissionLevel, setPermissionLevel] = useState<DomainPermissionLevel>("VIEW");
  const isLoading = state.status === "evaluating";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    evaluate({ membership_id: membershipId, domain_id: domainId, permission_level: permissionLevel });
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Access Evaluation</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Evaluate access for a governed request (C-002).
        </p>
      </div>

      <Card>
        <CardTitle>Evaluate Access</CardTitle>
        <CardDescription>
          Produces an Unresolved or Deferred Access Evaluation Outcome only — a genuine
          Permitted/Denied determination requires a production Access resolver not yet authorized
          (WP-05, minimum scope). Preserve/Expire Scope, Detect Context Change, and Hand-off
          Rejection are not yet surfaced in this Workspace.
        </CardDescription>

        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <FormField>
              <FormLabel htmlFor="ae-membership-id">Membership ID</FormLabel>
              <Input
                id="ae-membership-id"
                value={membershipId}
                onChange={(event) => setMembershipId(event.target.value)}
                required
                disabled={isLoading}
              />
            </FormField>

            <FormField>
              <FormLabel htmlFor="ae-domain-id">Domain ID</FormLabel>
              <Input
                id="ae-domain-id"
                value={domainId}
                onChange={(event) => setDomainId(event.target.value)}
                required
                disabled={isLoading}
              />
            </FormField>
          </div>

          <FormField>
            <FormLabel>Permission Level Requested</FormLabel>
            <div className="flex flex-wrap gap-2">
              {PERMISSION_LEVELS.map((level) => (
                <Button
                  key={level}
                  type="button"
                  variant={permissionLevel === level ? "primary" : "secondary"}
                  onClick={() => setPermissionLevel(level)}
                  disabled={isLoading}
                >
                  {level}
                </Button>
              ))}
            </div>
            <FormHelperText>
              A recorded outcome is always Unresolved or Deferred, never Permitted or Denied — a
              request that would require a Permitted/Denied determination is rejected instead of
              recording an outcome (see below).
            </FormHelperText>
          </FormField>

          <Button type="submit" disabled={isLoading}>
            {isLoading && <Spinner className="mr-2" />}
            Evaluate Access
          </Button>
        </form>

        {state.status === "error" && (
          <div className="mt-4">
            <FormBanner tone="danger">
              {state.isNotImplemented
                ? "This request would require a Permitted or Denied determination, which this environment does not yet resolve. Try a Membership or Domain combination that resolves to Unresolved or Deferred instead."
                : state.message}
            </FormBanner>
          </div>
        )}

        {state.status === "evaluated" && (
          <dl className="mt-4 grid grid-cols-[160px_1fr] gap-y-3 text-sm">
            <dt className="font-semibold text-muted-foreground">Outcome</dt>
            <dd>
              <StatusBadge tone="warning">{state.outcome.outcome_type}</StatusBadge>
            </dd>

            <dt className="font-semibold text-muted-foreground">Validity</dt>
            <dd className="text-foreground">{state.outcome.validity_status}</dd>

            <dt className="font-semibold text-muted-foreground">Reason</dt>
            <dd className="text-foreground">{state.outcome.reason}</dd>
          </dl>
        )}
      </Card>
    </div>
  );
}
