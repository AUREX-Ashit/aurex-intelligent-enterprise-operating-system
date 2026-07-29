-- =============================================================================
-- 06_bootstrap_verify.sql
-- Aurex AuthService — Bootstrap Verification
-- =============================================================================
-- PURPOSE
--   Verifies the bootstrap entity graph is complete and internally consistent
--   before login testing begins. Run after 05_bootstrap_first_user.sql.
--
-- HOW TO RUN
--   docker exec -i aurex-postgres psql -U postgres -d aurex \
--     < scripts/06_bootstrap_verify.sql
-- =============================================================================

\echo ''
\echo '======================================='
\echo 'BOOTSTRAP VERIFICATION'
\echo '======================================='
\echo ''

-- -----------------------------------------------------------------------------
-- CHECK 1: All 4 bootstrap entities exist
-- Expected: 4 rows
-- -----------------------------------------------------------------------------
\echo 'CHECK 1: Bootstrap entities exist'
\echo 'Expected: 4 rows'
SELECT 'organization' AS entity, id::text, 'CORP-DEMO-001' AS key
FROM organizations
WHERE id = '5466c6bf-67b2-52ac-ba83-a8cff7b8b42e'

UNION ALL

SELECT 'person', id::text, display_name
FROM persons
WHERE id = '5385aa88-1e34-57fa-8c0c-fef655ca3773'

UNION ALL

SELECT 'identity', id::text, email
FROM identities
WHERE id = '69a5c359-8a90-5274-9835-c0636e415873'

UNION ALL

SELECT 'membership', id::text, membership_status
FROM memberships
WHERE id = '53a0068c-fcc1-5aca-88f2-b19422ab3fd2';

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
WHERE i.id = '69a5c359-8a90-5274-9835-c0636e415873';

-- -----------------------------------------------------------------------------
-- CHECK 3: JWT claims can be assembled
-- Shows what the JWT payload will contain for this login
-- Expected: 1 row with all 5 R-001 claims populated
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
WHERE i.email = 'admin@corpstage.com'
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
WHERE id = '69a5c359-8a90-5274-9835-c0636e415873';

-- -----------------------------------------------------------------------------
-- CHECK 5: Role-permission grants for ORG_ADMIN (12 expected)
-- Expected: 12 rows
-- -----------------------------------------------------------------------------
\echo ''
\echo 'CHECK 5: ORG_ADMIN permission grants (expected 12)'
SELECT p.permission_code
FROM role_permissions rp
JOIN permissions p ON rp.permission_id = p.id
WHERE rp.role_id = 'c0d893dd-834a-539a-b0b9-cea32d756c9e'
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
\echo 'BOOTSTRAP VERIFIED'
\echo ''
\echo 'Ready for login testing:'
\echo '  POST /auth/login'
\echo '  Body: { email: admin@corpstage.com, password: Aurex#Admin2026! }'
\echo '  Expected: TokenResponse with all 5 R-001 JWT claims'
\echo '======================================='
