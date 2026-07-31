"use client";

import { useRouter } from "next/navigation";
import { Menu } from "@/components/ui/Menu";
import type { AuthClaims } from "@/types/auth";

const LOGIN_ROUTE = "/platform-admin/login";

/**
 * Reusable Platform Asset — User Menu. Extracted from AdminShell's own
 * previously-inline profile menu so any current or future Workspace shell
 * can reuse the identical sign-out affordance without re-implementing it.
 */
export function UserMenu({ claims, onSignOut }: { claims: AuthClaims; onSignOut: () => void }) {
  const router = useRouter();

  return (
    <Menu
      trigger={
        <span className="inline-flex h-9 items-center rounded-md border border-border bg-surface px-3 text-sm font-semibold text-foreground">
          {claims.role_code}
        </span>
      }
      items={[
        {
          label: "Sign out",
          tone: "danger",
          onSelect: () => {
            onSignOut();
            router.replace(LOGIN_ROUTE);
          },
        },
      ]}
    />
  );
}
