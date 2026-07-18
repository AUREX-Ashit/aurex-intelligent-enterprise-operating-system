"use client";

import { useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { cn } from "@/lib/utils";

/**
 * DS-001 Navigation Components — Command Palette. Explicitly a
 * non-functional placeholder for this phase of the Platform Administrator
 * Workspace: it opens and closes (reusing the existing Modal primitive)
 * but performs no search or command execution.
 */
export function CommandPaletteTrigger({ className }: { className?: string }) {
  const [open, setOpen] = useState(false);

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
        <span>Command palette</span>
        <kbd className="rounded border border-border-muted bg-surface-muted px-1.5 py-0.5 text-xs font-semibold">
          ⌘K
        </kbd>
      </button>

      <Modal open={open} onClose={() => setOpen(false)} title="Command Palette">
        <p className="text-sm text-muted-foreground">
          Command palette search is not implemented yet. This entry point exists so the
          Platform Administrator Workspace shell is complete and future capability work has a
          fixed, discoverable location to wire into.
        </p>
      </Modal>
    </>
  );
}
