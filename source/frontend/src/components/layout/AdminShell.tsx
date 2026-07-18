"use client";

import { useEffect, useState, type ReactNode } from "react";
import { useRouter, usePathname } from "next/navigation";
import { Sidebar } from "@/components/ui/Sidebar";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { Menu } from "@/components/ui/Menu";
import { CommandPaletteTrigger } from "@/components/ui/CommandPalette";
import { Modal } from "@/components/ui/Modal";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";
import { ADMIN_NAV_ITEMS, ADMIN_WORKSPACE_ROOT } from "@/config/admin-navigation";
import type { AuthClaims } from "@/types/auth";

const LOGIN_ROUTE = "/platform-admin/login";
const PLATFORM_ADMIN_ROLE = "PLATFORM_ADMIN";

function FullPageLoading() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background text-muted-foreground">
      <Spinner className="mr-2 h-5 w-5" />
      <span className="text-sm font-medium">Loading…</span>
    </div>
  );
}

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

function NotificationsTrigger() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="Notifications"
        className="inline-flex h-9 items-center rounded-md border border-border bg-surface px-3 text-sm text-muted-foreground transition hover:bg-surface-muted"
      >
        Notifications
      </button>

      <Modal open={open} onClose={() => setOpen(false)} title="Notifications">
        <p className="text-sm text-muted-foreground">
          Platform notification delivery is not implemented yet. This entry point exists so the
          shell is complete and Notification Management (see the workspace navigation) has a
          fixed, discoverable location to wire into.
        </p>
      </Modal>
    </>
  );
}

function AdminHeader({
  onOpenNav,
  breadcrumbItems,
  claims,
  onSignOut,
}: {
  onOpenNav: () => void;
  breadcrumbItems: { label: string; href?: string }[];
  claims: AuthClaims;
  onSignOut: () => void;
}) {
  const router = useRouter();

  return (
    <header className="flex h-16 shrink-0 items-center gap-4 border-b border-border bg-surface px-4 sm:px-6">
      <button
        type="button"
        onClick={onOpenNav}
        aria-label="Open navigation"
        className="inline-flex h-9 items-center rounded-md border border-border px-3 text-sm text-foreground sm:hidden"
      >
        Menu
      </button>

      <Breadcrumb items={breadcrumbItems} className="hidden sm:flex" />

      <div className="ml-auto flex items-center gap-2">
        <input
          type="search"
          disabled
          placeholder="Search (coming soon)"
          aria-label="Global search"
          className="hidden h-9 w-56 rounded-md border border-border bg-surface px-3 text-sm text-foreground placeholder:text-muted disabled:cursor-not-allowed disabled:opacity-60 md:block"
        />

        <CommandPaletteTrigger className="hidden md:inline-flex" />
        <NotificationsTrigger />

        <Menu
          trigger={
            <span className="inline-flex h-9 items-center rounded-md border border-border bg-surface px-3 text-sm font-semibold text-foreground">
              {claims.role_code}
            </span>
          }
          items={[
            {
              label: "Sign out",
              tone: "danger",
              onSelect: () => {
                onSignOut();
                router.replace(LOGIN_ROUTE);
              },
            },
          ]}
        />
      </div>
    </header>
  );
}

/**
 * Application Shell for the Platform Administrator Workspace. Composes
 * the DS-001 Navigation Components (Sidebar, Breadcrumb, Menu, Command
 * Palette) around every /platform-admin/(workspace) route, and is the
 * single place session (useAuth) and role gating happen for that route
 * group — individual pages never re-implement either.
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
    return <FullPageLoading />;
  }

  const { claims } = session;

  if (claims.role_code !== PLATFORM_ADMIN_ROLE) {
    return <AccessDenied roleCode={claims.role_code} onSignOut={logout} />;
  }

  const activeItem =
    ADMIN_NAV_ITEMS.find((item) => item.href === pathname) ??
    ADMIN_NAV_ITEMS.find((item) => item.href === ADMIN_WORKSPACE_ROOT)!;

  const breadcrumbItems =
    activeItem.href === ADMIN_WORKSPACE_ROOT
      ? [{ label: activeItem.label }]
      : [{ label: "Platform Dashboard", href: ADMIN_WORKSPACE_ROOT }, { label: activeItem.label }];

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar items={ADMIN_NAV_ITEMS} mobileOpen={mobileNavOpen} onClose={() => setMobileNavOpen(false)} />

      <div className="flex min-w-0 flex-1 flex-col">
        <AdminHeader
          onOpenNav={() => setMobileNavOpen(true)}
          breadcrumbItems={breadcrumbItems}
          claims={claims}
          onSignOut={logout}
        />
        <main className="flex-1 px-4 py-8 sm:px-6">{children}</main>
      </div>
    </div>
  );
}
