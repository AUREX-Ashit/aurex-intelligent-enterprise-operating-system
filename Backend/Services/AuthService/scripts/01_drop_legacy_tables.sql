-- =============================================================================
-- 01_drop_legacy_tables.sql
-- Aurex AuthService — Option B: Drop Legacy Tables
-- =============================================================================
-- PURPOSE
--   Drop the 4 legacy tables that conflict with or are superseded by the
--   R-001 schema. Run ONLY after 00_preflight_check.sql passes all checks.
--
-- DATA LOSS SUMMARY
--   roles             5 rows — seed data, recreated in R-001 format
--   permissions      12 rows — seed data, recreated in R-001 format
--   role_permissions 30 rows — seed data, recreated in R-001 format
--   user_roles        0 rows — empty, superseded by R-001 memberships table
--   ALL OTHER TABLES: untouched
--
-- DROP ORDER
--   FK-safe explicit order. Each table is dropped before its referenced table.
--   1. user_roles       — references roles (CASCADE), users (CASCADE), tenants (RESTRICT)
--   2. role_permissions — references roles (CASCADE), permissions (CASCADE)
--   3. roles            — no remaining FK dependents after steps 1-2
--   4. permissions      — no remaining FK dependents after steps 1-2
--
-- HOW TO RUN
--   docker exec -it aurex-postgres psql -U postgres -d aurex \
--     -f /path/to/01_drop_legacy_tables.sql
-- =============================================================================

\echo ''
\echo '======================================='
\echo 'STEP 1 — DROP LEGACY TABLES'
\echo '======================================='
\echo ''

BEGIN;

-- ---------------------------------------------------------------------------
-- 1. user_roles
--    Rows: 0  |  Superseded by: R-001 memberships
--    References: roles (CASCADE), users (CASCADE), tenants (RESTRICT)
-- ---------------------------------------------------------------------------
\echo 'Dropping user_roles ...'
DROP TABLE user_roles;
\echo 'OK: user_roles dropped'

-- ---------------------------------------------------------------------------
-- 2. role_permissions
--    Rows: 30 (seed data)  |  Recreated by: 03_seed_r001_data.sql
--    References: roles (CASCADE), permissions (CASCADE)
-- ---------------------------------------------------------------------------
\echo 'Dropping role_permissions ...'
DROP TABLE role_permissions;
\echo 'OK: role_permissions dropped'

-- ---------------------------------------------------------------------------
-- 3. roles
--    Rows: 5 (seed data)  |  Recreated by: 03_seed_r001_data.sql (R-001 schema)
--    No FK dependents remain after steps 1 and 2.
-- ---------------------------------------------------------------------------
\echo 'Dropping roles ...'
DROP TABLE roles;
\echo 'OK: roles dropped'

-- ---------------------------------------------------------------------------
-- 4. permissions
--    Rows: 12 (seed data)  |  Recreated by: 03_seed_r001_data.sql (R-001 schema)
--    No FK dependents remain after steps 1 and 2.
-- ---------------------------------------------------------------------------
\echo 'Dropping permissions ...'
DROP TABLE permissions;
\echo 'OK: permissions dropped'

COMMIT;

\echo ''
\echo '======================================='
\echo 'STEP 1 COMPLETE — 4 tables dropped'
\echo 'Run 02_post_drop_verify.sql to confirm.'
\echo '======================================='
