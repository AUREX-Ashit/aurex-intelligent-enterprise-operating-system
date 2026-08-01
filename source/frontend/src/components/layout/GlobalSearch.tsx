"use client";

import {
  useEffect,
  useMemo,
  useState,
  type ChangeEvent as ReactChangeEvent,
  type KeyboardEvent as ReactKeyboardEvent,
} from "react";
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
 * Reusable Platform Asset — Global Search. Realizes DS-001's canonical
 * Command Palette navigation component. Searches across every Workspace's
 * own navigation destinations (label, description, workspace name) and
 * jumps directly to the selected destination. Scoped to navigation search
 * only: no cross-entity (Organization/Person/etc.) search backend exists
 * yet in any WP-01 through WP-08 API, and inventing one is new
 * architecture this instruction does not authorize (CLAUDE.md §18) — this
 * realizes a genuinely working search capability within that boundary
 * rather than leaving the entry point non-functional. Reachable on every
 * viewport (not just ⌘K/Ctrl+K) so it satisfies SD-001 §11's Mobile Is a
 * First-Class Citizen principle.
 */
export function GlobalSearch({ className }: { className?: string }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [highlightedIndex, setHighlightedIndex] = useState(0);
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
    setHighlightedIndex(0);
  }

  function goTo(href: string) {
    close();
    router.push(href);
  }

  function handleQueryChange(event: ReactChangeEvent<HTMLInputElement>) {
    setQuery(event.target.value);
    setHighlightedIndex(0);
  }

  function handleInputKeyDown(event: ReactKeyboardEvent<HTMLInputElement>) {
    if (results.length === 0) return;

    if (event.key === "ArrowDown") {
      event.preventDefault();
      setHighlightedIndex((index) => Math.min(index + 1, results.length - 1));
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      setHighlightedIndex((index) => Math.max(index - 1, 0));
    } else if (event.key === "Enter") {
      const target = results[highlightedIndex];
      if (target) {
        event.preventDefault();
        goTo(target.href);
      }
    }
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
        <kbd className="hidden rounded border border-border-muted bg-surface-muted px-1.5 py-0.5 text-xs font-semibold sm:inline-block">
          ⌘K
        </kbd>
      </button>

      <Modal open={open} onClose={close} title="Search">
        <Input
          autoFocus
          value={query}
          onChange={handleQueryChange}
          onKeyDown={handleInputKeyDown}
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
              {results.map((result, index) => (
                <li key={`${result.workspaceLabel}-${result.slug}`}>
                  <button
                    type="button"
                    role="option"
                    aria-selected={index === highlightedIndex}
                    onClick={() => goTo(result.href)}
                    onMouseEnter={() => setHighlightedIndex(index)}
                    className={cn(
                      "block w-full rounded-md px-3 py-2 text-left transition hover:bg-surface-muted",
                      index === highlightedIndex && "bg-surface-muted",
                    )}
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
