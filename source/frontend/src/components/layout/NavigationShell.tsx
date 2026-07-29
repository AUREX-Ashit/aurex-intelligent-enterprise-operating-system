import Link from "next/link";
import type { ReactNode } from "react";

const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/health", label: "Health" },
  { href: "/person-management", label: "Person Management" },
  { href: "/organization", label: "Organization" },
  { href: "/workspace", label: "Workspace" },
  { href: "/settings", label: "Settings" },
] as const;

/**
 * Top-level navigation shell wrapping every route. Not gated behind
 * authentication — login is not implemented yet (see src/lib/auth-storage.ts).
 */
export function NavigationShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-full flex-col">
      <header className="border-b border-border bg-surface">
        <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-6">
          <Link href="/" className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-full border border-border bg-surface-muted text-sm font-black tracking-tight text-brand-strong">
              AX
            </span>
            <span className="text-lg font-extrabold tracking-tight text-foreground">Aurex</span>
          </Link>

          <nav aria-label="Primary" className="hidden gap-1 sm:flex">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition hover:bg-surface-muted hover:text-foreground"
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl flex-1 px-6 py-8">{children}</main>

      <footer className="border-t border-border-muted px-6 py-4 text-center text-xs text-muted-foreground">
        Aurex Enterprise Operating System
      </footer>
    </div>
  );
}
