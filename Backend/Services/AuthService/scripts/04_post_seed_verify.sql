-- =============================================================================
-- 04_post_seed_verify.sql
-- CorpStage AuthService — Final Post-Seed Verification
-- =============================================================================
-- PURPOSE
--   Run after 03_seed_r001_data.sql.
--   Validates the complete R-001 schema and seed data state.
--   Every result must match the expected value before the environment
--   is considered ready for AuthService operation.
--
-- HOW TO RUN
--   docker exec -it corpstage-postgres psql -U postgres -d corpstage \
--     -f /path/to/04_post_seed_verify.sql
-- =============================================================================

\echo ''
\echo '======================================='
\echo 'FINAL VERIFICATION'
\echo '======================================='
\echo ''

-- -----------------------------------------------------------------------------
-- CHECK 1: Alembic migration applied
-- Expected: 8fac154e79e2
-- -----------------------------------------------------------------------------
\echo 'CHECK 1: Alembic migration version'
\echo 'Expected: 8fac154e79e2'
SELECT version_num FROM alembic_version;

-- -----------------------------------------------------------------------------
-- CHECK 2: All 8 R-001 tables exist
-- Expected: 8 rows
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 2: All 8 R-001 tables exist'
\echo 'Expected: 8 rows'
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
      'organizations','persons','identities','memberships',
      'roles','permissions','role_permissions','refresh_tokens'
  )
ORDER BY table_name;

-- -----------------------------------------------------------------------------
-- CHECK 3: Seed row counts
-- Expected: roles=6, permissions=12, role_permissions=42
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 3: Seed row counts'
\echo 'Expected: roles=6, permissions=12, role_permissions=42'
SELECT 'roles'            AS table_name, COUNT(*) AS actual, 6  AS expected FROM roles
UNION ALL
SELECT 'permissions',                    COUNT(*),           12             FROM permissions
UNION ALL
SELECT 'role_permissions',               COUNT(*),           42             FROM role_permissions
ORDER BY table_name;

-- -----------------------------------------------------------------------------
-- CHECK 4: Role definitions — codes and is_system_role flag
-- Expected: 6 roles, only PLATFORM_ADMIN has is_system_role=true
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 4: Role definitions'
SELECT
    role_code,
    role_name,
    is_system_role,
    created_at::date AS created_date
FROM roles
ORDER BY role_code;

-- -----------------------------------------------------------------------------
-- CHECK 5: Permission definitions
-- Expected: 12 permissions across 4 domains
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 5: Permission definitions'
SELECT
    permission_code,
    permission_name
FROM permissions
ORDER BY permission_code;

-- -----------------------------------------------------------------------------
-- CHECK 6: Role-permission matrix — counts per role
-- Expected:
--   AUDITOR         4
--   BOARD_MEMBER    4
--   ESG_MANAGER     8
--   ORG_ADMIN      12
--   PLATFORM_ADMIN 12
--   SUPPLIER_ADMIN  2
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 6: Permissions per role'
\echo 'Expected: AUDITOR=4, BOARD_MEMBER=4, ESG_MANAGER=8, ORG_ADMIN=12, PLATFORM_ADMIN=12, SUPPLIER_ADMIN=2'
SELECT
    r.role_code,
    COUNT(rp.id) AS permission_count
FROM roles r
LEFT JOIN role_permissions rp ON rp.role_id = r.id
GROUP BY r.role_code
ORDER BY r.role_code;

-- -----------------------------------------------------------------------------
-- CHECK 7: Full resolved matrix (human-readable)
-- Expected: 42 rows showing role → permission mappings
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 7: Full role-permission matrix'
SELECT
    r.role_code,
    p.permission_code
FROM role_permissions rp
JOIN roles       r ON rp.role_id       = r.id
JOIN permissions p ON rp.permission_id = p.id
ORDER BY r.role_code, p.permission_code;

-- -----------------------------------------------------------------------------
-- CHECK 8: R-001 empty tables (should all be 0 — no application data yet)
-- Expected: 0 rows each
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 8: R-001 tables are empty (no application data yet)'
\echo 'Expected: 0 rows each'
SELECT 'organizations' AS table_name, COUNT(*) AS rows FROM organizations
UNION ALL SELECT 'persons',           COUNT(*) FROM persons
UNION ALL SELECT 'identities',        COUNT(*) FROM identities
UNION ALL SELECT 'memberships',       COUNT(*) FROM memberships
UNION ALL SELECT 'refresh_tokens',    COUNT(*) FROM refresh_tokens
ORDER BY table_name;

-- -----------------------------------------------------------------------------
-- CHECK 9: Reference data untouched
-- Expected: tenants=1, esg_metrics=11, sdg_goals=17
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 9: Pre-existing reference data intact'
\echo 'Expected: tenants=1, esg_metrics=11, sdg_goals=17'
SELECT 'tenants'     AS table_name, COUNT(*) AS rows FROM tenants
UNION ALL
SELECT 'esg_metrics',               COUNT(*)          FROM esg_metrics
UNION ALL
SELECT 'sdg_goals',                 COUNT(*)          FROM sdg_goals
ORDER BY table_name;

-- -----------------------------------------------------------------------------
-- CHECK 10: Dropped legacy tables must not exist
-- Expected: 0 rows
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 10: Legacy tables must not exist'
\echo 'Expected: 0 rows'
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('user_roles');

-- -----------------------------------------------------------------------------
-- CHECK 11: PLATFORM_ADMIN UUID matches seed reference
-- Expected: 9524d250-fe5e-5334-845b-18d547a5b59c
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 11: PLATFORM_ADMIN UUID integrity'
\echo 'Expected: 9524d250-fe5e-5334-845b-18d547a5b59c'
SELECT id, role_code, is_system_role
FROM roles
WHERE role_code = 'PLATFORM_ADMIN';

\echo ''
\echo '======================================='
\echo 'FINAL VERIFICATION COMPLETE'
\echo ''
\echo 'If all 11 checks pass:'
\echo '  - AuthService database is ready'
\echo '  - Start AuthService with JWT_SECRET_KEY set'
\echo '  - Confirm /health returns 200'
\echo '======================================='
