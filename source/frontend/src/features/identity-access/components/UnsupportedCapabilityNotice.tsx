import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { StatusBadge } from "@/components/ui/StatusBadge";

/**
 * Reports, rather than hides or fakes, a sub-capability that has no
 * backing API today. Used for Identity Management, Membership
 * Management, and Organization Association — each has real underlying
 * data (see AuthService's Identity/Membership models) but no endpoint
 * exposes it, so no screen is built for it.
 */
export function UnsupportedCapabilityNotice({
  title,
  reason,
}: {
  title: string;
  reason: string;
}) {
  return (
    <Card>
      <div className="flex items-start justify-between gap-4">
        <CardTitle>{title}</CardTitle>
        <StatusBadge tone="muted">Not available</StatusBadge>
      </div>
      <CardDescription>{reason}</CardDescription>
    </Card>
  );
}
