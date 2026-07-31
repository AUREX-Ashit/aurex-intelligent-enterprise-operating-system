"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { cn } from "@/lib/utils";
import { WORKSPACES } from "@/config/workspaces";
import type { AdminNavItem } from "@/config/admin-navigation";

interface SearchResult extends AdminNavItem {
  workspaceLabel: string;
}

const ALL_RESULTS: SearchResult[] = WORKSPACES.flatMap((workspace) =>
  workspace.navItems.map((item) => ({ ...item, workspaceLabel: workspace.label })),
);

function search(query: string): SearchResult[] {
  const trimmed = query.trim().toLowerCase();
  if (!trimmed) return ALL_RESULTS;
  return ALL_RESULTS.filter(
    (item) =>
      item.label.toLowerCase().includes(trimmed) ||
      item.description.toLowerCase().includes(trimmed) ||
      item.workspaceLabel.toLowerCase().includes(trimmed),
  );
}

/**
 * Reusable Platform Asset — Global Search. Searches across every
 * Workspace's own navigation destinations (label, description, workspace
 * name) and jumps directly to the selected destination. Scoped to
 * navigation search only: no cross-entity (Organization/Person/etc.)
 * search backend exists yet in any WP-01 through WP-08 API, and inventing
 * one is new architecture this instruction does not authorize
 * (CLAUDE.md §18) — this realizes a genuinely working search capability
 * within that boundary rather than leaving the entry point non-functional
 * (the prior CommandPaletteTrigger's own explicit placeholder state).
 */
export function GlobalSearch({ className }: { className?: string }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const router = useRouter();
  const results = useMemo(() => search(query), [query]);

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setOpen(true);
      }
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, []);

  function close() {
    setOpen(false);
    setQuery("");
  }

  function goTo(href: string) {
    close();
    router.push(href);
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className={cn(
          "inline-flex h-9 items-center gap-2 rounded-md border border-border bg-surface px-3 text-sm text-muted-foreground transition hover:bg-surface-muted",
          className,
        )}
      >
        <span>Search</span>
        <kbd className="rounded border border-border-muted bg-surface-muted px-1.5 py-0.5 text-xs font-semibold">
          ⌘K
        </kbd>
      </button>

      <Modal open={open} onClose={close} title="Search">
        <Input
          autoFocus
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search workspaces and capabilities…"
          aria-label="Global search"
        />

        <div className="mt-4 max-h-80 overflow-y-auto" role="listbox" aria-label="Search results">
          {results.length === 0 ? (
            <p className="py-6 text-center text-sm text-muted-foreground">
              No matches for &ldquo;{query}&rdquo;.
            </p>
          ) : (
            <ul className="space-y-1">
              {results.map((result) => (
                <li key={`${result.workspaceLabel}-${result.slug}`}>
                  <button
                    type="button"
                    role="option"
                    aria-selected="false"
                    onClick={() => goTo(result.href)}
                    className="block w-full rounded-md px-3 py-2 text-left transition hover:bg-surface-muted"
                  >
                    <span className="block text-sm font-semibold text-foreground">{result.label}</span>
                    <span className="block text-xs text-muted-foreground">
                      {result.workspaceLabel} · {result.description}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </Modal>
    </>
  );
}
