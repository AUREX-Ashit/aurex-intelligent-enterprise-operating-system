/**
 * Platform Administrator Workspace navigation. Static configuration, not
 * backend-driven metadata: SD-001-018 ("Navigation Is Metadata") calls for
 * tenant-level navigation metadata, but no navigation-metadata entity or
 * API exists yet in any backend service. This is a documented, temporary
 * deviation — see the shell's compliance report — not a silent violation.
 *
 * The Platform Dashboard is the workspace's landing page
 * (/platform-admin) rather than a sibling route; every other area below
 * is a distinct route rendering a placeholder until its own backend
 * capability exists.
 */
export interface AdminNavItem {
  slug: string;
  label: string;
  description: string;
  href: string;
}

export const ADMIN_WORKSPACE_ROOT = "/platform-admin";

export const ADMIN_NAV_ITEMS: AdminNavItem[] = [
  {
    slug: "dashboard",
    label: "Platform Dashboard",
    description: "Platform-wide administrator overview.",
    href: "/platform-admin",
  },
  {
    slug: "platform-governance",
    label: "Platform Governance",
    description: "Platform-level governance controls.",
    href: "/platform-admin/platform-governance",
  },
  {
    slug: "identity-access",
    label: "Identity & Access Management",
    description: "Identities, memberships, roles, and permissions.",
    href: "/platform-admin/identity-access",
  },
  {
    slug: "organizations",
    label: "Organization Management",
    description: "Tenant organizations across the platform.",
    href: "/platform-admin/organizations",
  },
  {
    slug: "person-management-admin",
    label: "Person Management",
    description: "Recognize, establish, and understand authoritative Person Context.",
    href: "/platform-admin/enterprise-administration/person",
  },
  {
    slug: "membership-management",
    label: "Membership Management",
    description: "Establish, understand, and maintain Membership Context.",
    href: "/platform-admin/enterprise-administration/membership",
  },
  {
    slug: "enterprise-structure",
    label: "Enterprise Structure",
    description: "Establish and view organization nodes.",
    href: "/platform-admin/enterprise-administration/structure",
  },
  {
    slug: "roles-permissions",
    label: "Roles & Permissions",
    description: "Establish and view business and system roles.",
    href: "/platform-admin/identity-security/roles",
  },
  {
    slug: "domain-permissions",
    label: "Domain Permissions",
    description: "Understand domain permission grants.",
    href: "/platform-admin/identity-security/domain-permissions",
  },
  {
    slug: "access-evaluation",
    label: "Access Evaluation",
    description: "Evaluate access requests and review outcomes.",
    href: "/platform-admin/identity-security/access-evaluation",
  },
  {
    slug: "subscriptions",
    label: "Subscription & Commercial Management",
    description: "Subscriptions, plans, and commercial terms.",
    href: "/platform-admin/subscriptions",
  },
  {
    slug: "workflows",
    label: "Workflow Administration",
    description: "Platform workflow configuration.",
    href: "/platform-admin/workflows",
  },
  {
    slug: "design-system",
    label: "AUREX Design System Administration",
    description: "Design tokens, themes, and components.",
    href: "/platform-admin/design-system",
  },
  {
    slug: "ai-administration",
    label: "AI Administration",
    description: "AI providers, models, and processing configuration.",
    href: "/platform-admin/ai-administration",
  },
  {
    slug: "enterprise-intelligence",
    label: "Enterprise Intelligence Administration",
    description: "Enterprise Intelligence configuration.",
    href: "/platform-admin/enterprise-intelligence",
  },
  {
    slug: "integrations",
    label: "Integration Administration",
    description: "External system integrations.",
    href: "/platform-admin/integrations",
  },
  {
    slug: "security",
    label: "Security Administration",
    description: "Platform security policies.",
    href: "/platform-admin/security",
  },
  {
    slug: "monitoring",
    label: "Monitoring & Operations",
    description: "Platform health and operations.",
    href: "/platform-admin/monitoring",
  },
  {
    slug: "notifications",
    label: "Notification Management",
    description: "Platform notification configuration.",
    href: "/platform-admin/notifications",
  },
  {
    slug: "audit-compliance",
    label: "Audit & Compliance",
    description: "Audit trails and compliance review.",
    href: "/platform-admin/audit-compliance",
  },
  {
    slug: "data-administration",
    label: "Data Administration",
    description: "Platform data ingestion and management.",
    href: "/platform-admin/data-administration",
  },
  {
    slug: "system-configuration",
    label: "System Configuration",
    description: "Platform and tenant configuration.",
    href: "/platform-admin/system-configuration",
  },
  {
    slug: "devops",
    label: "DevOps & Platform Operations",
    description: "Deployment and platform operations.",
    href: "/platform-admin/devops",
  },
  {
    slug: "reporting-analytics",
    label: "Reporting & Analytics",
    description: "Enterprise reports and analytics.",
    href: "/platform-admin/reporting-analytics",
  },
  {
    slug: "support",
    label: "Support Administration",
    description: "Platform support operations.",
    href: "/platform-admin/support",
  },
  {
    slug: "developer",
    label: "Developer Administration",
    description: "Developer tools and API access.",
    href: "/platform-admin/developer",
  },
  {
    slug: "governance",
    label: "Governance",
    description: "Enterprise governance oversight.",
    href: "/platform-admin/governance",
  },
];
