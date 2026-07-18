"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect } from "react";
import { cn } from "@/lib/utils";

export interface SidebarNavItem {
  slug: string;
  label: string;
  href: string;
}

/**
 * DS-001 Navigation Components — Sidebar. Persistent left navigation for
 * the Platform Administrator Workspace. On small viewports it renders as
 * an off-canvas panel (SD-001 §11 Mobile & Multi-Device Principles)
 * toggled by AdminShell, with a backdrop that closes it on outside click
 * or Escape.
 */
export function Sidebar({
  items,
  mobileOpen,
  onClose,
}: {
  items: SidebarNavItem[];
  mobileOpen: boolean;
  onClose: () => void;
}) {
  const pathname = usePathname();

  useEffect(() => {
    if (!mobileOpen) return;

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") onClose();
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [mobileOpen, onClose]);

  return (
    <>
      {mobileOpen && (
        <div
          role="presentation"
          aria-hidden="true"
          onClick={onClose}
          className="fixed inset-0 z-20 bg-black/40 sm:hidden"
        />
      )}

      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-30 w-64 shrink-0 overflow-y-auto border-r border-border bg-surface transition-transform duration-200 sm:static sm:z-auto sm:translate-x-0",
          mobileOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <nav aria-label="Platform Administrator" className="space-y-1 p-4">
          {items.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.slug}
                href={item.href}
                onClick={onClose}
                aria-current={isActive ? "page" : undefined}
                className={cn(
                  "block rounded-md px-3 py-2 text-sm font-medium transition",
                  isActive
                    ? "bg-brand/10 text-brand-strong"
                    : "text-muted-foreground hover:bg-surface-muted hover:text-foreground",
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </aside>
    </>
  );
}
