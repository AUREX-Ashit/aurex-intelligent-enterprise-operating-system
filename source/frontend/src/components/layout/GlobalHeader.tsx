"use client";

import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { GlobalSearch } from "@/components/layout/GlobalSearch";
import { NotificationCenter } from "@/components/layout/NotificationCenter";
import { UserMenu } from "@/components/layout/UserMenu";
import { WorkspaceSwitcher } from "@/components/layout/WorkspaceSwitcher";
import type { Workspace } from "@/config/workspaces";
import type { AuthClaims } from "@/types/auth";

/**
 * Reusable Platform Asset — Global Header. Composes the Workspace
 * Switcher, breadcrumb, Global Search, Notification Area, and User Menu
 * into the single header row every Workspace shell shares. Extracted from
 * AdminShell's own previously-inline header so it is not tied exclusively
 * to any one Workspace or Work Package.
 */
export function GlobalHeader({
  onOpenNav,
  activeWorkspace,
  breadcrumbItems,
  claims,
  onSignOut,
}: {
  onOpenNav: () => void;
  activeWorkspace: Workspace;
  breadcrumbItems: { label: string; href?: string }[];
  claims: AuthClaims;
  onSignOut: () => void;
}) {
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

      <div className="hidden items-center gap-4 sm:flex">
        <WorkspaceSwitcher activeWorkspace={activeWorkspace} />
        <Breadcrumb items={breadcrumbItems} />
      </div>

      <div className="ml-auto flex items-center gap-2">
        <GlobalSearch className="hidden md:inline-flex" />
        <NotificationCenter />
        <UserMenu claims={claims} onSignOut={onSignOut} />
      </div>
    </header>
  );
}
