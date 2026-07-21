import { Card, CardTitle } from "@/components/ui/Card";
import { OrganizationDetailsList } from "@/features/organization/components/OrganizationDetailsList";
import type { EstablishOrganizationState } from "@/features/organization/state/useEstablishOrganization";

export function OrganizationResultPanel({ state }: { state: EstablishOrganizationState }) {
  const organization = state.status === "established" ? state.organization : null;

  return (
    <Card>
      <CardTitle>Result</CardTitle>

      {!organization && (
        <p className="mt-2 text-sm text-muted-foreground">Establish an organization to see results here.</p>
      )}

      {organization && <OrganizationDetailsList organization={organization} />}
    </Card>
  );
}
