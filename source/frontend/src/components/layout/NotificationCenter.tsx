"use client";

import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

/**
 * Reusable Platform Asset — Notification Area. A fixed, discoverable
 * location for platform notifications, per SD-003 §8 (Notifications,
 * Attention & Cognitive Load Laws). No backend notification source exists
 * yet in any WP-01 through WP-08 API — this component honestly renders
 * an empty state rather than fabricating notification data, and is built
 * as a real, reusable panel (not an inline placeholder) so a future
 * capability only needs to supply data, not rebuild this shell.
 */
export function NotificationCenter() {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") setOpen(false);
    }

    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }

    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [open]);

  return (
    <div ref={containerRef} className="relative inline-block">
      <button
        type="button"
        aria-haspopup="true"
        aria-expanded={open}
        aria-label="Notifications"
        onClick={() => setOpen((current) => !current)}
        className="inline-flex h-9 items-center rounded-md border border-border bg-surface px-3 text-sm text-muted-foreground transition hover:bg-surface-muted"
      >
        Notifications
      </button>

      {open && (
        <div
          role="region"
          aria-label="Notifications"
          className={cn(
            "absolute right-0 z-40 mt-2 w-80 rounded-md border border-border bg-surface p-4 shadow-lg",
          )}
        >
          <h2 className="text-sm font-bold text-foreground">Notifications</h2>
          <p className="mt-2 text-sm text-muted-foreground">
            You&rsquo;re all caught up. Platform notification delivery has no connected source yet
            — this panel is ready to display notifications once a capability publishes them.
          </p>
        </div>
      )}
    </div>
  );
}
