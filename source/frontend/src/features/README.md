# features/

Business Activity feature modules — one subdirectory per capability, each
with its own `components/`, and, where genuinely needed, `state/`
subfolders.

Implemented: `features/auth/` (Platform Administrator login),
`features/identity-access/` (Platform Administrator Identity & Access),
`features/person/` (Person Management — recognize/establish),
`features/organization/` (Organization Management, WP-01 — Establish
Organization only so far; Lifecycle/Search/Audit History land as later
IRA-001 phases).

Not yet implemented: Workspace and Settings still render
`components/layout/PlaceholderPage.tsx` directly from `src/app/`, with
nothing here yet to route to.
