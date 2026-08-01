"use client";

import { useRef, useState, type KeyboardEvent, type ReactNode } from "react";
import { useOverlay } from "@/hooks/useOverlay";
import { cn } from "@/lib/utils";

export interface MenuItem {
  label: string;
  onSelect: () => void;
  tone?: "default" | "danger";
}

/**
 * DS-001 Navigation Components — Menu. A trigger that opens a small
 * anchored panel of actions (used for the Workspace Switcher and Profile
 * Menu). Closes on Escape and outside click, traps and restores focus
 * (via the shared useOverlay hook), and supports Up/Down/Home/End
 * navigation between items per the WAI-ARIA menu pattern that its own
 * `role="menu"`/`role="menuitem"` markup implies.
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
  const panelRef = useRef<HTMLDivElement>(null);

  useOverlay({
    open,
    onClose: () => setOpen(false),
    containerRef,
    trapRef: panelRef,
    closeOnOutsideClick: true,
  });

  function handlePanelKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    const itemButtons = Array.from(
      event.currentTarget.querySelectorAll<HTMLButtonElement>('[role="menuitem"]'),
    );
    if (itemButtons.length === 0) return;
    const currentIndex = itemButtons.indexOf(document.activeElement as HTMLButtonElement);

    if (event.key === "ArrowDown") {
      event.preventDefault();
      itemButtons[(currentIndex + 1) % itemButtons.length]?.focus();
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      itemButtons[(currentIndex - 1 + itemButtons.length) % itemButtons.length]?.focus();
    } else if (event.key === "Home") {
      event.preventDefault();
      itemButtons[0]?.focus();
    } else if (event.key === "End") {
      event.preventDefault();
      itemButtons[itemButtons.length - 1]?.focus();
    }
  }

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
          ref={panelRef}
          role="menu"
          tabIndex={-1}
          onKeyDown={handlePanelKeyDown}
          className={cn(
            "absolute z-40 mt-2 min-w-[12rem] rounded-md border border-border bg-surface p-1 shadow-lg outline-none",
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
