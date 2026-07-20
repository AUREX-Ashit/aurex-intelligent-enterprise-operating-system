import { PersonManagementScreen } from "@/features/person/components/PersonManagementScreen";
import { ProfileSummary } from "@/features/identity-access/components/ProfileSummary";
import { UnsupportedCapabilityNotice } from "@/features/identity-access/components/UnsupportedCapabilityNotice";

export function IdentityAccessScreen() {
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

      <section aria-labelledby="person-management-heading" className="space-y-6">
        <h2 id="person-management-heading" className="sr-only">
          Person Management
        </h2>
        <PersonManagementScreen />
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
          title="Identity Management"
          reason="AuthService's Identity model records identity_type, is_primary, is_verified, and last_login_at, but no endpoint reads or lists Identity records — only login and refresh (which return JWT claims, not the full record)."
        />
        <UnsupportedCapabilityNotice
          title="Membership Management"
          reason="AuthService's Membership model records membership_status, is_primary, and joined_at per person/organization/role, but no endpoint reads, lists, or manages Membership records."
        />
        <UnsupportedCapabilityNotice
          title="Organization Association"
          reason="Beyond the current organization_id carried in the session's JWT claims (shown above), no endpoint lists a person's full set of organization memberships outside of the multi-organization login flow."
        />
      </section>
    </div>
  );
}
