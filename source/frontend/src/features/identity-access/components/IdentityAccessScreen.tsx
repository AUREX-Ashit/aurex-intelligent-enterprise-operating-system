"use client";

import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";
import { IdentityRecoverySection } from "@/features/identity/components/IdentityRecoverySection";
import { IdentityStatusSection } from "@/features/identity/components/IdentityStatusSection";
import { useIdentityManagement } from "@/features/identity/state/useIdentityManagement";
import { ProfileSummary } from "@/features/identity-access/components/ProfileSummary";
import { UnsupportedCapabilityNotice } from "@/features/identity-access/components/UnsupportedCapabilityNotice";

export function IdentityAccessScreen() {
  const { session } = useAuth();
  const { state, checkStatus, requestRecovery } = useIdentityManagement();
  const personId = session.status === "authenticated" ? session.claims.person_id : null;

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">
          Identity & Access Management
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Authentication session, person recognition, and identity records for the platform.
        </p>
      </div>

      <ProfileSummary />

      <section aria-labelledby="identity-management-heading" className="space-y-6">
        <h2 id="identity-management-heading" className="sr-only">
          Identity Management
        </h2>
        <IdentityStatusSection state={state} onCheckStatus={checkStatus} />
        {personId && (
          <IdentityRecoverySection state={state} personId={personId} onRequestRecovery={requestRecovery} />
        )}
      </section>

      <section aria-labelledby="unsupported-heading" className="space-y-4">
        <h2 id="unsupported-heading" className="text-lg font-bold text-foreground">
          Not Yet Supported
        </h2>
        <p className="text-sm text-muted-foreground">
          The following sub-capabilities have underlying data in AuthService but no API exposes
          them yet, so no screen has been built for them. Implementing them requires backend
          endpoints, not architectural changes.
        </p>

        <UnsupportedCapabilityNotice
          title="Identity Record Detail (View/List)"
          reason="WP-08 added Identity Context status re-confirmation and self-service recovery requests (above), but AuthService's Identity model's own detail fields — identity_type, is_primary, is_verified, and last_login_at — still have no dedicated endpoint to read or list them; PE-001-C001 does not require one (it governs Identity Context, not raw Identity record presentation)."
        />

        <p className="text-sm text-muted-foreground">
          <Link href="/platform-admin/enterprise-administration/person" className="underline">
            Person Management
          </Link>{" "}
          and{" "}
          <Link href="/platform-admin/enterprise-administration/membership" className="underline">
            Membership Management
          </Link>{" "}
          (including cross-organization association via My Membership Portfolio) are now available
          in the Enterprise Administration Workspace — no longer unsupported.
        </p>
      </section>
    </div>
  );
}
