import { Card, CardTitle } from "@/components/ui/Card";
import { StatusBadge } from "@/components/ui/StatusBadge";
import type { EstablishOrganizationState } from "@/features/organization/state/useEstablishOrganization";

export function OrganizationResultPanel({ state }: { state: EstablishOrganizationState }) {
  const organization = state.status === "established" ? state.organization : null;

  return (
    <Card>
      <CardTitle>Result</CardTitle>

      {!organization && (
        <p className="mt-2 text-sm text-muted-foreground">Establish an organization to see results here.</p>
      )}

      {organization && (
        <dl className="mt-4 grid grid-cols-[140px_1fr] gap-y-3 text-sm">
          <dt className="font-semibold text-muted-foreground">Organization ID</dt>
          <dd className="text-foreground">{organization.id}</dd>

          <dt className="font-semibold text-muted-foreground">Code</dt>
          <dd className="text-foreground">{organization.organization_code}</dd>

          <dt className="font-semibold text-muted-foreground">Name</dt>
          <dd className="text-foreground">{organization.organization_name}</dd>

          <dt className="font-semibold text-muted-foreground">Type</dt>
          <dd className="text-foreground">{organization.organization_type}</dd>

          <dt className="font-semibold text-muted-foreground">Status</dt>
          <dd>
            <StatusBadge tone={organization.status === "ACTIVE" ? "success" : "warning"}>
              {organization.status}
            </StatusBadge>
          </dd>
        </dl>
      )}
    </Card>
  );
}
