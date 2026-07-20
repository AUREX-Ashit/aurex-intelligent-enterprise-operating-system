-- =============================================================================
-- 00_preflight_check.sql
-- CorpStage AuthService — Option B Pre-flight Verification
-- =============================================================================
-- PURPOSE
--   Run this script FIRST, before any drops or migrations.
--   Every result must match the expected values in the comments.
--   Abort the entire sequence if ANY result differs.
--
-- HOW TO RUN
--   docker exec -it corpstage-postgres psql -U postgres -d corpstage \
--     -f /path/to/00_preflight_check.sql
-- =============================================================================

\echo ''
\echo '======================================='
\echo 'PRE-FLIGHT CHECK — AuthService Option B'
\echo '======================================='
\echo ''

-- -----------------------------------------------------------------------------
-- CHECK 1: PostgreSQL version
-- Expected: PostgreSQL 16.x
-- -----------------------------------------------------------------------------
\echo 'CHECK 1: PostgreSQL version'
SELECT version();

-- -----------------------------------------------------------------------------
-- CHECK 2: Current database
-- Expected: corpstage
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 2: Current database'
SELECT current_database(), current_user;

-- -----------------------------------------------------------------------------
-- CHECK 3: Exact row counts — tables being dropped
-- Expected:
--   roles             5
--   permissions      12
--   role_permissions 30
--   user_roles        0
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 3: Row counts — tables being dropped'
\echo 'Expected: roles=5, permissions=12, role_permissions=30, user_roles=0'
SELECT 'roles'            AS table_name, COUNT(*) AS actual_rows, 5  AS expected FROM roles
UNION ALL
SELECT 'permissions',                    COUNT(*),                12             FROM permissions
UNION ALL
SELECT 'role_permissions',               COUNT(*),                30             FROM role_permissions
UNION ALL
SELECT 'user_roles',                     COUNT(*),                0              FROM user_roles
ORDER BY table_name;

-- -----------------------------------------------------------------------------
-- CHECK 4: Tables NOT being dropped — must remain untouched
-- Expected:
--   users             0
--   tenants           1
--   esg_metrics      11
--   sdg_goals        17
--   all others        0
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 4: Row counts — tables NOT being dropped'
\echo 'Expected: users=0, tenants=1, esg_metrics=11, sdg_goals=17, all others=0'
SELECT 'users'             AS table_name, COUNT(*) AS rows FROM users
UNION ALL SELECT 'tenants',              COUNT(*) FROM tenants
UNION ALL SELECT 'esg_metrics',          COUNT(*) FROM esg_metrics
UNION ALL SELECT 'sdg_goals',            COUNT(*) FROM sdg_goals
UNION ALL SELECT 'sdg_mappings',         COUNT(*) FROM sdg_mappings
UNION ALL SELECT 'audit_logs',           COUNT(*) FROM audit_logs
UNION ALL SELECT 'documents',            COUNT(*) FROM documents
UNION ALL SELECT 'document_metadata',    COUNT(*) FROM document_metadata
UNION ALL SELECT 'document_versions',    COUNT(*) FROM document_versions
UNION ALL SELECT 'esg_metric_values',    COUNT(*) FROM esg_metric_values
UNION ALL SELECT 'extractions',          COUNT(*) FROM extractions
UNION ALL SELECT 'reports',              COUNT(*) FROM reports
UNION ALL SELECT 'report_versions',      COUNT(*) FROM report_versions
UNION ALL SELECT 'scores',               COUNT(*) FROM scores
UNION ALL SELECT 'validations',          COUNT(*) FROM validations
ORDER BY table_name;

-- -----------------------------------------------------------------------------
-- CHECK 5: Alembic version table must NOT exist (no prior migrations)
-- Expected: ERROR — relation "alembic_version" does not exist
--   (If this returns a row, a prior migration has been applied — STOP)
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 5: Alembic version state'
\echo 'Expected: ERROR — alembic_version does not exist'
SELECT EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public'
    AND   table_name   = 'alembic_version'
) AS alembic_version_exists;
-- Expected: false

-- -----------------------------------------------------------------------------
-- CHECK 6: R-001 target tables must NOT yet exist
-- Expected: 0 rows — none of these tables exist yet
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 6: R-001 target tables must not exist yet'
\echo 'Expected: 0 rows'
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
      'organizations','persons','identities','memberships','refresh_tokens'
  );

-- -----------------------------------------------------------------------------
-- CHECK 7: FK dependencies on tables being dropped
-- Expected output matches the known dependency map
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 7: FK dependencies on tables being dropped'
SELECT
    tc.table_name        AS dependent_table,
    kcu.column_name      AS fk_column,
    ccu.table_name       AS references_table,
    rc.delete_rule       AS on_delete
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema   = kcu.table_schema
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema   = tc.table_schema
JOIN information_schema.referential_constraints rc
    ON rc.constraint_name    = tc.constraint_name
    AND rc.constraint_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND ccu.table_name IN ('roles','permissions','role_permissions')
ORDER BY references_table, dependent_table;
-- Expected:
--   role_permissions | permission_id | permissions      | CASCADE
--   role_permissions | role_id       | roles            | CASCADE
--   user_roles       | role_id       | roles            | CASCADE

\echo ''
\echo '======================================='
\echo 'PRE-FLIGHT COMPLETE'
\echo 'Review all results before proceeding.'
\echo 'Abort if any CHECK differs from expected.'
\echo '======================================='
