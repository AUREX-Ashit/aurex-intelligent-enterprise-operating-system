"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";

export interface MenuItem {
  label: string;
  onSelect: () => void;
  tone?: "default" | "danger";
}

/**
 * DS-001 Navigation Components — Menu. A trigger that opens a small
 * anchored panel of actions (used for the Profile Menu). Closes on
 * Escape and on outside click, consistent with Modal's Escape handling.
 */
export function Menu({
  trigger,
  items,
  align = "end",
}: {
  trigger: ReactNode;
  items: MenuItem[];
  align?: "start" | "end";
}) {
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
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={() => setOpen((current) => !current)}
        className="inline-flex items-center rounded-md"
      >
        {trigger}
      </button>

      {open && (
        <div
          role="menu"
          className={cn(
            "absolute z-40 mt-2 min-w-[12rem] rounded-md border border-border bg-surface p-1 shadow-lg",
            align === "end" ? "right-0" : "left-0",
          )}
        >
          {items.map((item) => (
            <button
              key={item.label}
              type="button"
              role="menuitem"
              onClick={() => {
                setOpen(false);
                item.onSelect();
              }}
              className={cn(
                "block w-full rounded-md px-3 py-2 text-left text-sm font-medium transition hover:bg-surface-muted",
                item.tone === "danger" ? "text-danger" : "text-foreground",
              )}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
