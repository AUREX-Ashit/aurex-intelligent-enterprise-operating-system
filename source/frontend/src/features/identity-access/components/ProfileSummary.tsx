"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { useAuth } from "@/hooks/useAuth";
import type { AuthClaims } from "@/types/auth";

function formatExpiry(exp: number | undefined): string {
  if (!exp) return "Unknown";
  const remainingMs = exp * 1000 - Date.now();
  if (remainingMs <= 0) return "Expired";
  const minutes = Math.round(remainingMs / 60000);
  return minutes < 1 ? "Less than a minute" : `${minutes} minute${minutes === 1 ? "" : "s"}`;
}

const CLAIM_ROWS: { label: string; key: keyof AuthClaims }[] = [
  { label: "Person ID", key: "person_id" },
  { label: "Identity ID", key: "identity_id" },
  { label: "Organization ID", key: "organization_id" },
  { label: "Membership ID", key: "membership_id" },
];

/**
 * View Profile — the only Profile data available is what R-001's JWT
 * claims carry (person_id, identity_id, organization_id, membership_id,
 * role_code). No GET /person/{id} or similar profile-read endpoint
 * exists, so display name and email are not shown here; "Edit supported
 * fields" is not implemented for the same reason — no update endpoint
 * exists for any of these claims.
 */
export function ProfileSummary() {
  const { session, logout } = useAuth();
  const router = useRouter();

  if (session.status !== "authenticated") return null;
  const { claims } = session;

  return (
    <Card>
      <div className="flex items-start justify-between gap-4">
        <div>
          <CardTitle>My Profile</CardTitle>
          <CardDescription>Current session, from the signed access token.</CardDescription>
        </div>
        <StatusBadge tone="brand">{claims.role_code}</StatusBadge>
      </div>

      <dl className="mt-4 grid grid-cols-1 gap-y-3 text-sm sm:grid-cols-[160px_1fr]">
        {CLAIM_ROWS.map((row) => (
          <div key={row.key} className="contents">
            <dt className="font-semibold text-muted-foreground">{row.label}</dt>
            <dd className="break-all text-foreground">{claims[row.key]}</dd>
          </div>
        ))}

        <dt className="font-semibold text-muted-foreground">Role</dt>
        <dd className="text-foreground">{claims.role_code}</dd>

        <dt className="font-semibold text-muted-foreground">Session expires in</dt>
        <dd className="text-foreground">{formatExpiry(claims.exp)}</dd>
      </dl>

      <Button
        className="mt-6"
        variant="secondary"
        onClick={() => {
          logout();
          router.replace("/platform-admin/login");
        }}
      >
        Sign out
      </Button>
    </Card>
  );
}
