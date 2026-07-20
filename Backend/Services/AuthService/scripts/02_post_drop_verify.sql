-- =============================================================================
-- 02_post_drop_verify.sql
-- CorpStage AuthService — Post-Drop Verification
-- =============================================================================
-- PURPOSE
--   Run after 01_drop_legacy_tables.sql.
--   Confirm the 4 tables are gone and no other data was affected.
--   Proceed to Alembic migration only after this script produces clean results.
--
-- HOW TO RUN
--   docker exec -it corpstage-postgres psql -U postgres -d corpstage \
--     -f /path/to/02_post_drop_verify.sql
-- =============================================================================

\echo ''
\echo '======================================='
\echo 'POST-DROP VERIFICATION'
\echo '======================================='
\echo ''

-- -----------------------------------------------------------------------------
-- CHECK 1: Dropped tables must not exist
-- Expected: 0 rows
-- -----------------------------------------------------------------------------
\echo 'CHECK 1: Dropped tables must not exist'
\echo 'Expected: 0 rows'
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('roles','permissions','role_permissions','user_roles');

-- -----------------------------------------------------------------------------
-- CHECK 2: Remaining tables (15 expected)
-- Expected: 15 tables
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 2: Remaining tables in public schema'
\echo 'Expected: 15 tables'
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- -----------------------------------------------------------------------------
-- CHECK 3: Reference data intact
-- Expected: tenants=1, esg_metrics=11, sdg_goals=17
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 3: Reference data intact'
\echo 'Expected: tenants=1, esg_metrics=11, sdg_goals=17'
SELECT 'tenants'     AS table_name, COUNT(*) AS rows FROM tenants
UNION ALL
SELECT 'esg_metrics',               COUNT(*)          FROM esg_metrics
UNION ALL
SELECT 'sdg_goals',                 COUNT(*)          FROM sdg_goals
ORDER BY table_name;

-- -----------------------------------------------------------------------------
-- CHECK 4: No FK references to dropped tables remain
-- Expected: 0 rows
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 4: No remaining FK references to dropped tables'
\echo 'Expected: 0 rows'
SELECT
    tc.table_name     AS dependent_table,
    ccu.table_name    AS references_table
FROM information_schema.table_constraints tc
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema   = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND ccu.table_name IN ('roles','permissions','role_permissions','user_roles');

\echo ''
\echo '======================================='
\echo 'POST-DROP VERIFICATION COMPLETE'
\echo 'If all checks pass: run Alembic migration'
\echo 'then proceed to 03_seed_r001_data.sql'
\echo '======================================='
