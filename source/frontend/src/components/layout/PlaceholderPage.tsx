import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { PageHeader } from "@/components/ui/PageHeader";
import { StatusBadge } from "@/components/ui/StatusBadge";

/**
 * Shared shell for routes that exist (so navigation and routing are real)
 * but have no functionality yet. Each route using this renders no
 * capability-specific content — this component carries no Business
 * Activity logic itself.
 */
export function PlaceholderPage({ title, description }: { title: string; description: string }) {
  return (
    <div className="space-y-6">
      <PageHeader title={title} description={description} />

      <Card className="max-w-md">
        <CardTitle className="flex items-center gap-2">
          {title}
          <StatusBadge tone="muted">Coming soon</StatusBadge>
        </CardTitle>
        <CardDescription>This section has not been implemented yet.</CardDescription>
      </Card>
    </div>
  );
}
