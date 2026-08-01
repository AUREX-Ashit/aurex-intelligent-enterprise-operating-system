"use client";

import Link from "next/link";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { PageHeader } from "@/components/ui/PageHeader";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { useAuth } from "@/hooks/useAuth";
import { ADMIN_NAV_ITEMS, ADMIN_WORKSPACE_ROOT } from "@/config/admin-navigation";

/**
 * Platform Dashboard — the workspace landing page. This phase establishes
 * the shell only: it does not aggregate live platform data (no backend
 * API exists yet for a cross-tenant administrator dashboard — see the
 * shell's compliance report), so it renders navigation into every
 * administrator feature area rather than fabricated metrics.
 */
export default function PlatformDashboardPage() {
  const { session } = useAuth();
  const roleCode = session.status === "authenticated" ? session.claims.role_code : null;

  const featureAreas = ADMIN_NAV_ITEMS.filter((item) => item.href !== ADMIN_WORKSPACE_ROOT);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Platform Dashboard"
        description={`Platform Administrator Workspace${roleCode ? ` — signed in as ${roleCode}` : ""}.`}
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {featureAreas.map((item) => (
          <Link key={item.slug} href={item.href}>
            <Card className="h-full transition hover:border-brand">
              <CardTitle className="flex items-center justify-between gap-2">
                {item.label}
                <StatusBadge tone="muted">Coming soon</StatusBadge>
              </CardTitle>
              <CardDescription>{item.description}</CardDescription>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
