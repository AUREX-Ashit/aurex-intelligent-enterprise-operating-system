/**
 * Workspace Model (PE-001 Chapter 13). A Workspace is an experience
 * boundary, not an implementation boundary (13.1): it groups the
 * Enterprise Experiences relevant to one persona-facing area of the
 * platform behind a Workspace Switcher, while every Workspace continues
 * to render through the same Platform Administrator Workspace shell
 * (AdminShell) and the same DS-001 navigation components.
 *
 * Does not replace or duplicate `admin-navigation.ts` — every existing
 * `AdminNavItem` (including its `href`, so no existing route or bookmark
 * changes) is reused here, only regrouped into named Workspaces per
 * PE-001 §13.5's own canonical categories (Platform, Enterprise
 * Administration; the remaining categories — Operational, Executive,
 * Collaboration, Intelligence — are not realized by any chartered
 * capability yet and are not invented here). "Identity & Security" is
 * this Work Package's own capability-grouping label for the Platform
 * workspace's own security-adjacent capabilities (C-001/C-002/C-003),
 * not a new PE-001 category.
 */
import { ADMIN_NAV_ITEMS, ADMIN_WORKSPACE_ROOT, type AdminNavItem } from "@/config/admin-navigation";

export interface Workspace {
  id: string;
  label: string;
  description: string;
  homeHref: string;
  navItems: AdminNavItem[];
}

const ENTERPRISE_ADMINISTRATION_SLUGS = [
  "organizations",
  "person-management-admin",
  "membership-management",
  "enterprise-structure",
];
const IDENTITY_SECURITY_SLUGS = [
  "identity-access",
  "roles-permissions",
  "domain-permissions",
  "access-evaluation",
];

function itemsFor(slugs: string[]): AdminNavItem[] {
  return ADMIN_NAV_ITEMS.filter((item) => slugs.includes(item.slug));
}

const enterpriseAdministrationItems = itemsFor(ENTERPRISE_ADMINISTRATION_SLUGS);
const identitySecurityItems = itemsFor(IDENTITY_SECURITY_SLUGS);
const claimedSlugs = new Set([...ENTERPRISE_ADMINISTRATION_SLUGS, ...IDENTITY_SECURITY_SLUGS]);
const platformItems = ADMIN_NAV_ITEMS.filter((item) => !claimedSlugs.has(item.slug));

export const WORKSPACES: Workspace[] = [
  {
    id: "platform",
    label: "Platform",
    description: "Platform-wide administration and configuration.",
    homeHref: ADMIN_WORKSPACE_ROOT,
    navItems: platformItems,
  },
  {
    id: "enterprise-administration",
    label: "Enterprise Administration",
    description: "Organizations, people, memberships, and enterprise structure.",
    homeHref: "/platform-admin/enterprise-administration",
    navItems: enterpriseAdministrationItems,
  },
  {
    id: "identity-security",
    label: "Identity & Security",
    description: "Identities, roles, permissions, and access evaluation.",
    homeHref: "/platform-admin/identity-access",
    navItems: identitySecurityItems,
  },
];

export const DEFAULT_WORKSPACE_ID = "platform";

export function workspaceForPathname(pathname: string): Workspace {
  const byHomeHref = WORKSPACES.find((workspace) => workspace.homeHref === pathname);
  if (byHomeHref) return byHomeHref;

  // Match against the most specific (longest) href, not the first workspace
  // whose navItems happen to contain a matching prefix — the Platform
  // workspace's own dashboard item (href "/platform-admin") is a string
  // prefix of every route in the app, so a first-match-wins scan would
  // always resolve to Platform.
  let best: { workspace: Workspace; href: string } | null = null;
  for (const workspace of WORKSPACES) {
    for (const item of workspace.navItems) {
      if (pathname.startsWith(item.href) && (!best || item.href.length > best.href.length)) {
        best = { workspace, href: item.href };
      }
    }
  }
  return best?.workspace ?? WORKSPACES.find((workspace) => workspace.id === DEFAULT_WORKSPACE_ID)!;
}

export function workspaceById(id: string): Workspace {
  return WORKSPACES.find((workspace) => workspace.id === id) ?? WORKSPACES[0];
}
