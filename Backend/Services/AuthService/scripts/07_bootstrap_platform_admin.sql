-- =============================================================================
-- 07_bootstrap_platform_admin.sql
-- Aurex AuthService — Bootstrap: Platform Administrator Person, Identity, Membership
-- =============================================================================
-- PURPOSE
--   Creates the minimum R-001 entity graph required to test a PLATFORM_ADMIN
--   login end-to-end against a live AuthService instance, exactly as
--   05_bootstrap_first_user.sql does for ORG_ADMIN.
--
--   Unlike 05_bootstrap_first_user.sql, this script does NOT create a new
--   Organization: PLATFORM_ADMIN is a system-level role that operates across
--   all organization boundaries (see 03_seed_r001_data.sql's PLATFORM_ADMIN
--   comment), so the Membership below simply reuses the existing Aurex
--   Demo Organization created by 05_bootstrap_first_user.sql. No schema, no
--   role, and no permission is created — only data, into tables that already
--   exist.
--
--   This script creates:
--     1. Person           — Platform Admin User
--     2. Identity         — platform.admin@corpstage.com / LOCAL credential
--     3. Membership        — Platform Admin User -> Demo Org -> PLATFORM_ADMIN
--
-- CREDENTIALS FOR LOGIN TESTING
--   Email:    platform.admin@corpstage.com
--   Password: Aurex#PlatformAdmin2026!
--   Org UUID: 5466c6bf-67b2-52ac-ba83-a8cff7b8b42e   (from 05_bootstrap_first_user.sql)
--
-- UUID STRATEGY
--   All bootstrap UUIDs are deterministic (uuid5) with the Aurex seed
--   namespace. Re-running produces the same UUIDs. ON CONFLICT DO NOTHING
--   makes this script safe to run multiple times.
--
-- UUID REFERENCE
--   Person:              1ac94f77-f5fc-5ce9-9c4e-1d01d59ed6b2
--   Identity:             4663ad18-6b14-5dd1-84c0-dbce51714d5f
--   Membership:           231190bc-dc3f-58d3-88c3-a4832ca62c89
--   Organization (reused): 5466c6bf-67b2-52ac-ba83-a8cff7b8b42e  (from 05_bootstrap_first_user.sql)
--   PLATFORM_ADMIN role:  9524d250-fe5e-5334-845b-18d547a5b59c  (from 03_seed_r001_data.sql)
--
-- PASSWORD HASH
--   Algorithm: bcrypt, cost factor 12
--   Hash:      $2b$12$IGo4i.zyAUgt2lyGul.LauAUOD1.6F.1LZfhtyrPYV/LKd1Jp4BCC
--   Generated: via Python bcrypt.hashpw() — verified round-trip before embedding
--
-- PREREQUISITES
--   - Alembic migration 8fac154e79e2 applied (run: alembic upgrade head)
--   - Seed data applied (run: 03_seed_r001_data.sql)
--   - PLATFORM_ADMIN role exists with UUID 9524d250-fe5e-5334-845b-18d547a5b59c
--   - Aurex Demo Organization exists (run: 05_bootstrap_first_user.sql)
--
-- HOW TO RUN
--   docker exec -i aurex-postgres psql -U postgres -d aurex \
--     < scripts/07_bootstrap_platform_admin.sql
-- =============================================================================

\echo ''
\echo '======================================='
\echo 'STEP 7 — BOOTSTRAP PLATFORM ADMINISTRATOR'
\echo '======================================='
\echo ''

BEGIN;

-- =============================================================================
-- 1. Person
-- =============================================================================
\echo 'Creating Person: Platform Admin User ...'

INSERT INTO persons (
    id,
    first_name,
    last_name,
    display_name,
    is_active,
    created_at,
    updated_at
)
VALUES (
    '1ac94f77-f5fc-5ce9-9c4e-1d01d59ed6b2',
    'Platform',
    'Admin',
    'Platform Admin User',
    true,
    NOW(),
    NULL
)
ON CONFLICT (id) DO NOTHING;

\echo 'OK: Person created (or already exists)'

-- =============================================================================
-- 2. Identity
--    password_hash is a bcrypt cost-12 hash of: Aurex#PlatformAdmin2026!
--    Verified round-trip in Python before embedding.
--    is_verified = true: allows immediate login without email verification flow.
-- =============================================================================
\echo 'Creating Identity: platform.admin@corpstage.com (LOCAL) ...'

INSERT INTO identities (
    id,
    person_id,
    email,
    password_hash,
    identity_type,
    is_primary,
    is_verified,
    last_login_at,
    created_at,
    updated_at
)
VALUES (
    '4663ad18-6b14-5dd1-84c0-dbce51714d5f',
    '1ac94f77-f5fc-5ce9-9c4e-1d01d59ed6b2',
    'platform.admin@corpstage.com',
    '$2b$12$IGo4i.zyAUgt2lyGul.LauAUOD1.6F.1LZfhtyrPYV/LKd1Jp4BCC',
    'LOCAL',
    true,
    true,
    NULL,
    NOW(),
    NULL
)
ON CONFLICT (email) DO NOTHING;

\echo 'OK: Identity created (or already exists)'

-- =============================================================================
-- 3. Membership
--    Links: Platform Admin User -> Aurex Demo Org -> PLATFORM_ADMIN
--    Reuses the Organization created by 05_bootstrap_first_user.sql — no new
--    Organization is created here (PLATFORM_ADMIN operates across all
--    organization boundaries; it does not require an org of its own).
--    is_primary = true: this is the person's default organization.
--    membership_status = ACTIVE: immediately accessible after login.
--    role_id references PLATFORM_ADMIN from 03_seed_r001_data.sql.
-- =============================================================================
\echo 'Creating Membership: Platform Admin User -> Demo Org -> PLATFORM_ADMIN ...'

INSERT INTO memberships (
    id,
    person_id,
    organization_id,
    role_id,
    membership_status,
    is_primary,
    joined_at,
    created_at,
    updated_at
)
VALUES (
    '231190bc-dc3f-58d3-88c3-a4832ca62c89',
    '1ac94f77-f5fc-5ce9-9c4e-1d01d59ed6b2',
    '5466c6bf-67b2-52ac-ba83-a8cff7b8b42e',          -- Aurex Demo Org from 05
    '9524d250-fe5e-5334-845b-18d547a5b59c',          -- PLATFORM_ADMIN from seed
    'ACTIVE',
    true,
    NOW(),
    NOW(),
    NULL
)
ON CONFLICT (person_id, organization_id) DO NOTHING;

\echo 'OK: Membership created (or already exists)'

COMMIT;

\echo ''
\echo '======================================='
\echo 'BOOTSTRAP COMPLETE'
\echo ''
\echo 'Login credentials:'
\echo '  Email:    platform.admin@corpstage.com'
\echo '  Password: Aurex#PlatformAdmin2026!'
\echo '  Org UUID: 5466c6bf-67b2-52ac-ba83-a8cff7b8b42e'
\echo '  Role:     PLATFORM_ADMIN'
\echo ''
\echo 'Verification queries follow below.'
\echo '======================================='

-- =============================================================================
-- VERIFICATION
-- Styled after 06_bootstrap_verify.sql, scoped to the Platform Administrator
-- entities created above. Read-only — safe to re-run any time.
-- =============================================================================

\echo ''
\echo '======================================='
\echo 'PLATFORM ADMINISTRATOR BOOTSTRAP VERIFICATION'
\echo '======================================='
\echo ''

-- -----------------------------------------------------------------------------
-- CHECK 1: All 3 bootstrap entities exist
-- Expected: 3 rows
-- -----------------------------------------------------------------------------
\echo 'CHECK 1: Bootstrap entities exist'
\echo 'Expected: 3 rows'
SELECT 'person' AS entity, id::text, display_name AS key
FROM persons
WHERE id = '1ac94f77-f5fc-5ce9-9c4e-1d01d59ed6b2'

UNION ALL

SELECT 'identity', id::text, email
FROM identities
WHERE id = '4663ad18-6b14-5dd1-84c0-dbce51714d5f'

UNION ALL

SELECT 'membership', id::text, membership_status
FROM memberships
WHERE id = '231190bc-dc3f-58d3-88c3-a4832ca62c89';

-- -----------------------------------------------------------------------------
-- CHECK 2: Full entity chain — resolved join
-- Verifies FK integrity: identity -> person -> membership -> org -> role
-- Expected: 1 row
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 2: Full entity chain (R-001 login path)'
\echo 'Expected: 1 row'
SELECT
    i.email,
    p.display_name,
    o.organization_name,
    o.organization_code,
    r.role_code,
    m.membership_status,
    m.is_primary,
    i.is_verified,
    i.identity_type
FROM identities  i
JOIN persons     p ON i.person_id       = p.id
JOIN memberships m ON m.person_id       = p.id
JOIN organizations o ON m.organization_id = o.id
JOIN roles       r ON m.role_id         = r.id
WHERE i.id = '4663ad18-6b14-5dd1-84c0-dbce51714d5f';

-- -----------------------------------------------------------------------------
-- CHECK 3: JWT claims can be assembled
-- Shows what the JWT payload will contain for this login
-- Expected: 1 row with all 5 R-001 claims populated, role_code = PLATFORM_ADMIN
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 3: R-001 JWT claims (what the token will contain)'
SELECT
    p.id         AS person_id,
    i.id         AS identity_id,
    o.id         AS organization_id,
    m.id         AS membership_id,
    r.role_code
FROM identities  i
JOIN persons     p ON i.person_id        = p.id
JOIN memberships m ON m.person_id        = p.id
JOIN organizations o ON m.organization_id = o.id
JOIN roles       r ON m.role_id          = r.id
WHERE i.email = 'platform.admin@corpstage.com'
  AND m.membership_status = 'ACTIVE';

-- -----------------------------------------------------------------------------
-- CHECK 4: Identity is verified and has a LOCAL password hash
-- Expected: is_verified=true, has_password=true, identity_type=LOCAL
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 4: Identity state'
SELECT
    email,
    identity_type,
    is_primary,
    is_verified,
    (password_hash IS NOT NULL AND password_hash != '') AS has_password_hash
FROM identities
WHERE id = '4663ad18-6b14-5dd1-84c0-dbce51714d5f';

-- -----------------------------------------------------------------------------
-- CHECK 5: Role-permission grants for PLATFORM_ADMIN (12 expected)
-- Expected: 12 rows
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 5: PLATFORM_ADMIN permission grants (expected 12)'
SELECT p.permission_code
FROM role_permissions rp
JOIN permissions p ON rp.permission_id = p.id
WHERE rp.role_id = '9524d250-fe5e-5334-845b-18d547a5b59c'
ORDER BY p.permission_code;

-- -----------------------------------------------------------------------------
-- CHECK 6: No orphan foreign keys
-- Expected: 0 rows for each
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 6: No orphan FK references'
SELECT 'orphan identities (no person)' AS check_name, COUNT(*) AS count
FROM identities i
LEFT JOIN persons p ON i.person_id = p.id
WHERE p.id IS NULL

UNION ALL

SELECT 'orphan memberships (no person)', COUNT(*)
FROM memberships m
LEFT JOIN persons p ON m.person_id = p.id
WHERE p.id IS NULL

UNION ALL

SELECT 'orphan memberships (no org)', COUNT(*)
FROM memberships m
LEFT JOIN organizations o ON m.organization_id = o.id
WHERE o.id IS NULL

UNION ALL

SELECT 'orphan memberships (no role)', COUNT(*)
FROM memberships m
LEFT JOIN roles r ON m.role_id = r.id
WHERE r.id IS NULL;
-- Expected: 0 for all

\echo ''
\echo '======================================='
\echo 'PLATFORM ADMINISTRATOR BOOTSTRAP VERIFIED'
\echo ''
\echo 'Ready for login testing:'
\echo '  POST /auth/login'
\echo '  Body: { email: platform.admin@corpstage.com, password: Aurex#PlatformAdmin2026! }'
\echo '  Expected: TokenResponse with all 5 R-001 JWT claims, role_code = PLATFORM_ADMIN'
\echo '======================================='
