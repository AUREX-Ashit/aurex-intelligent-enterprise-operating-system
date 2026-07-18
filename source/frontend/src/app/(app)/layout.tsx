import type { ReactNode } from "react";
import { NavigationShell } from "@/components/layout/NavigationShell";

/**
 * Chrome for the general (non-admin) application surface. Kept as its own
 * nested layout — rather than folded into the root layout — so the
 * Platform Administrator Workspace (src/app/platform-admin) can mount its
 * own distinct shell (AdminShell) without stacking both navigation chromes
 * on the same page.
 */
export default function AppLayout({ children }: { children: ReactNode }) {
  return <NavigationShell>{children}</NavigationShell>;
}
