import { StatusBadge } from "@/components/ui/StatusBadge";
import type { OrganizationResponse } from "@/types/organization";

/**
 * Pure presentational definition-list for an OrganizationResponse.
 * Extracted from OrganizationResultPanel (BA-01) so BA-02's View
 * Organization flow renders the same fields the same way, rather than
 * duplicating the markup.
 */
export function OrganizationDetailsList({ organization }: { organization: OrganizationResponse }) {
  return (
    <dl className="mt-4 grid grid-cols-[140px_1fr] gap-y-3 text-sm">
      <dt className="font-semibold text-muted-foreground">Organization ID</dt>
      <dd className="text-foreground">{organization.id}</dd>

      <dt className="font-semibold text-muted-foreground">Code</dt>
      <dd className="text-foreground">{organization.organization_code}</dd>

      <dt className="font-semibold text-muted-foreground">Name</dt>
      <dd className="text-foreground">{organization.organization_name}</dd>

      <dt className="font-semibold text-muted-foreground">Type</dt>
      <dd className="text-foreground">{organization.organization_type}</dd>

      <dt className="font-semibold text-muted-foreground">Description</dt>
      <dd className="text-foreground">{organization.description ?? "—"}</dd>

      <dt className="font-semibold text-muted-foreground">Status</dt>
      <dd>
        <StatusBadge tone={organization.status === "ACTIVE" ? "success" : "warning"}>
          {organization.status}
        </StatusBadge>
      </dd>
    </dl>
  );
}
