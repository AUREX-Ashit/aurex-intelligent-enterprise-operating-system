"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Menu } from "@/components/ui/Menu";
import { Spinner } from "@/components/ui/Spinner";
import { WORKSPACES, type Workspace } from "@/config/workspaces";
import { ApiError } from "@/lib/api-client";
import { useNotifications } from "@/lib/notifications";
import { getWorkspaceCandidates } from "@/services/workspace-api";

/**
 * WP-09 BA-01 (EX-C008-01/02) candidate-fetch state. The static
 * WORKSPACES config (admin nav-item groupings) remains the actual
 * switchable/navigable list — no PE-001 §13.5 Workspace Type binding
 * exists yet to route per-candidate (Pending Canonical Binding, WP-09
 * charter's own Out of Scope), so it is not replaced. What real data
 * from GET /workspaces/candidates now confirms: whether the caller
 * genuinely holds any active Membership anywhere at all — real
 * information the static config never had (IRA-009 §7's own "fallback/
 * seed only, not the sole source of truth" design).
 */
type CandidateFetchState = "loading" | "loaded" | "error";

/**
 * Reusable Platform Asset — lets a persona move between Workspaces
 * (PE-001 Chapter 13) without leaving the shell. Reuses the existing
 * Menu primitive rather than inventing a new dropdown pattern.
 */
export function WorkspaceSwitcher({ activeWorkspace }: { activeWorkspace: Workspace }) {
  const router = useRouter();
  const { notify } = useNotifications();
  const [fetchState, setFetchState] = useState<CandidateFetchState>("loading");
  const notifiedRef = useRef(false);

  useEffect(() => {
    let cancelled = false;

    getWorkspaceCandidates()
      .then((response) => {
        if (cancelled) return;
        setFetchState("loaded");
        if (response.candidates.length === 0 && !notifiedRef.current) {
          notifiedRef.current = true;
          notify("No active Workspace Memberships were found for your account.", "warning");
        }
      })
      .catch((error) => {
        if (cancelled) return;
        setFetchState("error");
        if (!notifiedRef.current) {
          notifiedRef.current = true;
          const message = error instanceof ApiError ? error.message : "Unable to confirm Workspace access. Showing the last known list.";
          notify(message, "danger");
        }
      });

    return () => {
      cancelled = true;
    };
  }, [notify]);

  return (
    <Menu
      align="start"
      trigger={
        <span className="inline-flex h-9 items-center gap-2 rounded-md border border-border bg-surface px-3 text-sm font-semibold text-foreground">
          {activeWorkspace.label}
          {fetchState === "loading" ? (
            <Spinner className="text-muted-foreground" />
          ) : (
            <span aria-hidden="true" className="text-muted-foreground">
              ▾
            </span>
          )}
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
