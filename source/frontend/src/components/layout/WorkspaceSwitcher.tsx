"use client";

import { useRouter } from "next/navigation";
import { Menu } from "@/components/ui/Menu";
import { WORKSPACES, type Workspace } from "@/config/workspaces";

/**
 * Reusable Platform Asset — lets a persona move between Workspaces
 * (PE-001 Chapter 13) without leaving the shell. Reuses the existing
 * Menu primitive rather than inventing a new dropdown pattern.
 */
export function WorkspaceSwitcher({ activeWorkspace }: { activeWorkspace: Workspace }) {
  const router = useRouter();

  return (
    <Menu
      align="start"
      trigger={
        <span className="inline-flex h-9 items-center gap-2 rounded-md border border-border bg-surface px-3 text-sm font-semibold text-foreground">
          {activeWorkspace.label}
          <span aria-hidden="true" className="text-muted-foreground">
            ▾
          </span>
        </span>
      }
      items={WORKSPACES.map((workspace) => ({
        label: workspace.label,
        tone: "default" as const,
        onSelect: () => router.push(workspace.homeHref),
      }))}
    />
  );
}
