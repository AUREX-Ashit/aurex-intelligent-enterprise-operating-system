# features/

Business Activity feature modules — one subdirectory per capability, each
with its own `components/`, and, where genuinely needed, `state/`
subfolders.

Implemented: `features/auth/` (Platform Administrator login),
`features/identity-access/` (Platform Administrator Identity & Access),
`features/person/` (Person Management — recognize/establish).

Not yet implemented: Organization, Workspace, and Settings still render
`components/layout/PlaceholderPage.tsx` directly from `src/app/`, with
nothing here yet to route to.
