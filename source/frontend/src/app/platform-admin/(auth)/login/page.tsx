import { LoginForm } from "@/features/auth/components/LoginForm";

/**
 * Deliberately outside the (workspace) route group / AdminShell — this
 * page must be reachable without a session, since it's what establishes
 * one. See src/app/platform-admin/(workspace)/layout.tsx for the guard
 * that redirects unauthenticated visitors here.
 */
export default function PlatformAdminLoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-6 py-16">
      <LoginForm />
    </div>
  );
}
