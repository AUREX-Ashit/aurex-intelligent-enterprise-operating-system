import Link from "next/link";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { WORKSPACES } from "@/config/workspaces";

const WORKSPACE_ID = "enterprise-administration";

/**
 * Enterprise Administration Workspace home (PE-001 Chapter 13). Renders
 * navigation into this Workspace's own capability areas — Organizations,
 * Person Management, Membership Management, Enterprise Structure — the
 * same "navigate, don't fabricate data" pattern the Platform Dashboard
 * already established, since no cross-capability aggregate view exists
 * in any WP-01 through WP-08 API.
 */
export default function EnterpriseAdministrationWorkspaceHome() {
  const workspace = WORKSPACES.find((item) => item.id === WORKSPACE_ID)!;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">{workspace.label}</h1>
        <p className="mt-1 text-sm text-muted-foreground">{workspace.description}</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {workspace.navItems.map((item) => (
          <Link key={item.slug} href={item.href}>
            <Card className="h-full transition hover:border-brand">
              <CardTitle>{item.label}</CardTitle>
              <CardDescription>{item.description}</CardDescription>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
