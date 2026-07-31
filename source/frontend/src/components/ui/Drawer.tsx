"use client";

import { useEffect, type ReactNode } from "react";
import { cn } from "@/lib/utils";

export interface DrawerProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
  className?: string;
}

/**
 * DS-001 Navigation/Overlay Components — Drawer. A slide-in side panel for
 * detail/quick-view content that doesn't warrant a full navigation away
 * from the current list or screen. Mirrors Modal's own escape/backdrop
 * pattern exactly (same event-handling shape, same z-index layer) rather
 * than inventing a new overlay convention.
 */
export function Drawer({ open, onClose, title, children, className }: DrawerProps) {
  useEffect(() => {
    if (!open) return;

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") onClose();
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      role="presentation"
      className="fixed inset-0 z-50 flex justify-end bg-black/40"
      onClick={onClose}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        onClick={(event) => event.stopPropagation()}
        className={cn(
          "flex h-full w-full max-w-md flex-col overflow-y-auto border-l border-border bg-surface p-6 shadow-lg",
          className,
        )}
      >
        {title && <h2 className="mb-4 text-lg font-bold text-foreground">{title}</h2>}
        {children}
      </div>
    </div>
  );
}
