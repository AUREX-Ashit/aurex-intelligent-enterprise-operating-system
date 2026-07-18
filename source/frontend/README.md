# CorpStage Frontend

Canonical frontend foundation for the CorpStage Enterprise Operating
System, at `source/frontend`. Next.js (App Router) + TypeScript + Tailwind
CSS.

This is a **foundation**, not a finished application: it establishes
routing, layout, theming, the API client, and a shared UI component set.
No Business Activity is implemented here — routes other than Health render
an empty placeholder (`src/components/layout/PlaceholderPage.tsx`) until
implemented separately.

## Getting Started

```bash
npm install
cp .env.example .env.local   # adjust NEXT_PUBLIC_AUTH_SERVICE_URL if needed
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Scripts

| Script | Purpose |
|---|---|
| `npm run dev` | Start the development server |
| `npm run build` | Production build |
| `npm run start` | Serve a production build |
| `npm run lint` | ESLint |
| `npm run format` | Format with Prettier |
| `npm run format:check` | Check formatting without writing |

## Structure

```
src/
  app/          Routes (Next.js App Router) — layout, error/loading/not-found, pages
  components/
    ui/         Shared, generic UI primitives (Button, Input, Card, Modal, Table, Form)
    layout/     Application-level layout (NavigationShell, PlaceholderPage)
  features/     Reserved for future Business Activity feature modules (currently empty)
  hooks/        Generic, reusable React hooks (no Business Activity logic)
  lib/          Core infrastructure — config, logger, notifications, api-client, auth-storage, utils
  services/     Backend-domain API wrappers built on lib/api-client (e.g. health-service.ts)
  types/        Shared, backend-mirroring TypeScript types
  styles/       Design tokens (theme.css)
```

## Backend

Talks to AuthService (`NEXT_PUBLIC_AUTH_SERVICE_URL`, default
`http://localhost:8000`). See `src/lib/api-client.ts` for the request
layer and `src/lib/config.ts` for environment resolution.

Authentication infrastructure (`src/lib/auth-storage.ts`, `src/types/auth.ts`,
`setAuthTokenProvider` in `api-client.ts`) is prepared but not wired to any
login flow — login is a separate, not-yet-implemented Business Activity.

## Routes

| Route | Status |
|---|---|
| `/` | Home |
| `/health` | Live — calls AuthService `GET /health` |
| `/person-management` | Placeholder |
| `/organization` | Placeholder |
| `/workspace` | Placeholder |
| `/settings` | Placeholder |
