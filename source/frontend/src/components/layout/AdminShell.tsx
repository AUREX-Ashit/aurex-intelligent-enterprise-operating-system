"use client";

import { useEffect, useState, type ReactNode } from "react";
import { useRouter, usePathname } from "next/navigation";
import { Sidebar } from "@/components/ui/Sidebar";
import { LoadingState } from "@/components/ui/LoadingState";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { GlobalHeader } from "@/components/layout/GlobalHeader";
import { useAuth } from "@/hooks/useAuth";
import { workspaceForPathname } from "@/config/workspaces";

const LOGIN_ROUTE = "/platform-admin/login";
const PLATFORM_ADMIN_ROLE = "PLATFORM_ADMIN";

function AccessDenied({ roleCode, onSignOut }: { roleCode: string; onSignOut: () => void }) {
  const router = useRouter();

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-6">
      <Card className="max-w-md text-center">
        <CardTitle>Access denied</CardTitle>
        <CardDescription>
          The Platform Administrator Workspace requires the {PLATFORM_ADMIN_ROLE} role. Your
          current role is {roleCode}.
        </CardDescription>
        <Button
          className="mt-6"
          variant="secondary"
          onClick={() => {
            onSignOut();
            router.replace(LOGIN_ROUTE);
          }}
        >
          Sign out
        </Button>
      </Card>
    </div>
  );
}

/**
 * AUREX Enterprise Shell — Application Shell. Composes the Sidebar
 * (Workspace Navigation) and GlobalHeader (Workspace Switcher, breadcrumb,
 * Global Search, Notification Area, User Menu) around every
 * /platform-admin/(workspace) route, driven by the active Workspace
 * (PE-001 Chapter 13) resolved from the current path. Single place session
 * (useAuth) and role gating happen for that route group — individual
 * pages never re-implement either. Reusable across every Workspace, not
 * tied to any one capability or Work Package.
 */
export function AdminShell({ children }: { children: ReactNode }) {
  const { session, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  useEffect(() => {
    if (session.status === "unauthenticated") {
      router.replace(LOGIN_ROUTE);
    }
  }, [session.status, router]);

  if (session.status === "loading" || session.status === "unauthenticated") {
    return <LoadingState fullScreen />;
  }

  const { claims } = session;

  if (claims.role_code !== PLATFORM_ADMIN_ROLE) {
    return <AccessDenied roleCode={claims.role_code} onSignOut={logout} />;
  }

  const activeWorkspace = workspaceForPathname(pathname);

  const activeItem =
    activeWorkspace.navItems.find((item) => item.href === pathname) ??
    activeWorkspace.navItems.find((item) => item.href === activeWorkspace.homeHref);

  const breadcrumbItems =
    !activeItem || activeItem.href === activeWorkspace.homeHref
      ? [{ label: activeWorkspace.label }]
      : [{ label: activeWorkspace.label, href: activeWorkspace.homeHref }, { label: activeItem.label }];

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar
        items={activeWorkspace.navItems}
        mobileOpen={mobileNavOpen}
        onClose={() => setMobileNavOpen(false)}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <GlobalHeader
          onOpenNav={() => setMobileNavOpen(true)}
          mobileNavOpen={mobileNavOpen}
          activeWorkspace={activeWorkspace}
          breadcrumbItems={breadcrumbItems}
          claims={claims}
          onSignOut={logout}
        />
        <main className="flex-1 px-4 py-8 sm:px-6">{children}</main>
      </div>
    </div>
  );
}
