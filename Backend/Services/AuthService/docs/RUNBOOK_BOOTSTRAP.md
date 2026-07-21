# Runbook: AuthService Platform Bootstrap (WP-00)

Governing work package: AUREX Platform Administrator Implementation Roadmap, WP-00 (Platform Bootstrap).
Owning service: AuthService. Owning team: see `OPERATIONAL_OWNERSHIP.md`.

## Purpose

Bootstrap seeds the platform's foundational, tenant-independent data — the 6 canonical
Roles, 12 canonical Permissions, their 42 Role-Permission grants, the CORP-DEMO-001
demonstration Organization, and the two bootstrap Identities (Demo Admin, Platform
Administrator) — so a freshly-provisioned environment has a Platform Administrator who
can log in and begin operating the platform. Without it, `/ready` reports
`bootstrap_not_applied` and the platform cannot be used.

The operation is idempotent: running it any number of times after the first has no
effect (`total_created == 0` on every subsequent run). It is safe to include in every
deployment pipeline run unconditionally.

## When bootstrap runs

- **Automatically**, as a CI/CD pipeline stage (`.github/workflows/authservice-ci.yml`,
  job `bootstrap`) against every environment's database as part of deployment, per
  IMP-CICD-002 (seed data execution must be an automated, idempotent pipeline stage,
  never a manually-run script).
- **Manually**, only for local development or incident recovery, via the procedure below.

## Manual invocation

```bash
cd Backend/Services/AuthService
export DATABASE_URL="postgresql+asyncpg://<user>:<password>@<host>:5432/<db>"
export JWT_SECRET_KEY="<any non-empty value; unused by bootstrap itself>"
python -m scripts.run_bootstrap
```

Exit code `0` indicates success (whether or not any rows were created). Exit code `1`
indicates failure — see Troubleshooting.

## Verifying bootstrap succeeded

```bash
curl -s https://<authservice-host>/ready
```

- `200 {"status": "ready", "bootstrap": "complete", ...}` — bootstrap has run.
- `503 {"status": "not_ready", "reason": "bootstrap_not_applied"}` — bootstrap has not
  run yet; run it manually or re-trigger the deployment pipeline.
- `503 {"status": "not_ready", "reason": "database_unreachable"}` — this is a database
  connectivity problem, not a bootstrap problem; do not re-run bootstrap.

## Demo credentials seeded by bootstrap

| Identity | Email | Role | Purpose |
|---|---|---|---|
| Platform Administrator | `platform.admin@corpstage.com` | PLATFORM_ADMIN | Platform-level operations, no Organization membership required |
| Demo Admin | `admin@corpstage.com` | ORG_ADMIN | CORP-DEMO-001 demonstration Organization admin |

Passwords are the pre-established values from
`scripts/05_bootstrap_first_user.sql` / `scripts/07_bootstrap_platform_admin.sql` — the
bcrypt hashes were ported verbatim into `scripts/bootstrap_data.py`. These hashes are
**public** (visible in source and in this document).

### Production safeguard (IC-001 M1)

When `ENVIRONMENT=production` (or `prod`), bootstrap refuses to seed either identity
using the built-in public hash and raises `RuntimeError` instead. To bootstrap a
production environment, supply real, rotated password hashes via:

```bash
export ENVIRONMENT="production"
export BOOTSTRAP_ADMIN_PASSWORD_HASH="<bcrypt hash of a real Demo Admin password>"
export BOOTSTRAP_PLATFORM_ADMIN_PASSWORD_HASH="<bcrypt hash of a real Platform Administrator password>"
python -m scripts.run_bootstrap
```

In any other `ENVIRONMENT` value (default `development`), the built-in hashes are used
unless these overrides are set — matching the existing `FF_<FLAG_NAME>`/`DATABASE_URL`
override pattern already used throughout `config.py`.

## Rollback strategy

Bootstrap has no destructive rollback path by design — rolling back would mean deleting
the Platform Administrator's own login, which would lock operators out of the platform.
Instead:

1. **Bad bootstrap data (wrong seed values):** fix `scripts/bootstrap_data.py`, then
   manually correct the affected rows via SQL (`UPDATE`) or the standard Role/
   Organization/Person management Business Activities once WP-01/WP-06 are live.
   Bootstrap itself will not overwrite rows that already exist.
2. **Bootstrap ran against the wrong database:** restore the target database from its
   most recent pre-bootstrap backup per the platform's standard database restore
   procedure. Bootstrap's own inserts are ordinary transactional rows with no
   irreversible side effects (no external calls, no file writes).
3. **Feature flags rolled out incorrectly:** flip the flag's `enabled` value (or narrow
   its `organizations` allowlist) in `Config/platform-config.yaml`, or set the
   `FF_<FLAG_NAME>` environment variable override, and redeploy — no data rollback
   required, since flags gate behavior, not data.

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| `scripts.run_bootstrap` exits 1 | Database unreachable, or `DATABASE_URL` unset | Verify `DATABASE_URL` and network/database availability |
| `scripts.run_bootstrap` exits 1 with "Refusing to bootstrap ... in a production environment" | `ENVIRONMENT=production` and no `BOOTSTRAP_ADMIN_PASSWORD_HASH`/`BOOTSTRAP_PLATFORM_ADMIN_PASSWORD_HASH` override set | Set both override env vars to real, rotated bcrypt hashes (see "Production safeguard" above) |
| `scripts.run_bootstrap` exits 0 immediately, `total_created` is 0 on a fresh DB | Migrations not yet applied (`alembic upgrade head` not run) | Apply migrations first, then re-run bootstrap |
| `/ready` stuck at `bootstrap_not_applied` after a successful-looking bootstrap run | Bootstrap ran against a different database than the one AuthService is now reading from | Confirm both point at the same `DATABASE_URL` |
| Bootstrap audit log missing | Check `authservice.audit` logger output for `PLATFORM_BOOTSTRAP` entries at the environment's configured log level | Structured audit/event/metric emission is via `observability.py`; confirm log aggregation is capturing the `authservice.*` logger namespace |
