-- =============================================================================
-- 05_bootstrap_first_user.sql
-- CorpStage AuthService — Bootstrap: First Organization, Person, Identity, Membership
-- =============================================================================
-- PURPOSE
--   Creates the minimum R-001 entity graph required to test the login flow
--   end-to-end against a live AuthService instance.
--
--   This script creates:
--     1. Organization     — CorpStage Demo Organization (CORP-DEMO-001)
--     2. Person           — Admin User
--     3. Identity         — admin@corpstage.com / LOCAL credential
--     4. Membership       — Admin User -> Demo Org -> ORG_ADMIN
--
-- CREDENTIALS FOR LOGIN TESTING
--   Email:    admin@corpstage.com
--   Password: CorpStage#Admin2026!
--   Org UUID: 5466c6bf-67b2-52ac-ba83-a8cff7b8b42e
--
-- UUID STRATEGY
--   All bootstrap UUIDs are deterministic (uuid5) with the CorpStage seed
--   namespace. Re-running produces the same UUIDs. ON CONFLICT DO NOTHING
--   makes this script safe to run multiple times.
--
-- UUID REFERENCE
--   Organization:  5466c6bf-67b2-52ac-ba83-a8cff7b8b42e
--   Person:        5385aa88-1e34-57fa-8c0c-fef655ca3773
--   Identity:      69a5c359-8a90-5274-9835-c0636e415873
--   Membership:    53a0068c-fcc1-5aca-88f2-b19422ab3fd2
--   ORG_ADMIN role: c0d893dd-834a-539a-b0b9-cea32d756c9e  (from seed)
--
-- PASSWORD HASH
--   Algorithm: bcrypt, cost factor 12
--   Hash:      $2b$12$BhF.jMSngAwyXAmmREe6BeB53viDBigLvJ7j76pyWHCpq/CvZd7AK
--   Generated: via Python bcrypt.hashpw() — verified round-trip before embedding
--
-- PREREQUISITES
--   - Alembic migration 8fac154e79e2 applied (run: alembic upgrade head)
--   - Seed data applied (run: 03_seed_r001_data.sql)
--   - ORG_ADMIN role exists with UUID c0d893dd-834a-539a-b0b9-cea32d756c9e
--
-- HOW TO RUN
--   docker exec -i corpstage-postgres psql -U postgres -d corpstage \
--     < scripts/05_bootstrap_first_user.sql
-- =============================================================================

\echo ''
\echo '======================================='
\echo 'STEP 5 — BOOTSTRAP FIRST USER'
\echo '======================================='
\echo ''

BEGIN;

-- =============================================================================
-- 1. Organization
-- =============================================================================
\echo 'Creating Organization: CorpStage Demo Organization ...'

INSERT INTO organizations (
    id,
    organization_code,
    organization_name,
    organization_type,
    is_active,
    created_at,
    updated_at
)
VALUES (
    '5466c6bf-67b2-52ac-ba83-a8cff7b8b42e',
    'CORP-DEMO-001',
    'CorpStage Demo Organization',
    'CORPORATE',
    true,
    NOW(),
    NULL
)
ON CONFLICT (organization_code) DO NOTHING;

\echo 'OK: Organization created (or already exists)'

-- =============================================================================
-- 2. Person
-- =============================================================================
\echo 'Creating Person: Admin User ...'

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
    '5385aa88-1e34-57fa-8c0c-fef655ca3773',
    'Admin',
    'User',
    'Admin User',
    true,
    NOW(),
    NULL
)
ON CONFLICT (id) DO NOTHING;

\echo 'OK: Person created (or already exists)'

-- =============================================================================
-- 3. Identity
--    password_hash is a bcrypt cost-12 hash of: CorpStage#Admin2026!
--    Verified round-trip in Python before embedding.
--    is_verified = true: allows immediate login without email verification flow.
-- =============================================================================
\echo 'Creating Identity: admin@corpstage.com (LOCAL) ...'

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
    '69a5c359-8a90-5274-9835-c0636e415873',
    '5385aa88-1e34-57fa-8c0c-fef655ca3773',
    'admin@corpstage.com',
    '$2b$12$BhF.jMSngAwyXAmmREe6BeB53viDBigLvJ7j76pyWHCpq/CvZd7AK',
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
-- 4. Membership
--    Links: Admin User -> CorpStage Demo Org -> ORG_ADMIN
--    is_primary = true: this is the person's default organization.
--    membership_status = ACTIVE: immediately accessible after login.
--    role_id references ORG_ADMIN from 03_seed_r001_data.sql.
-- =============================================================================
\echo 'Creating Membership: Admin User -> Demo Org -> ORG_ADMIN ...'

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
    '53a0068c-fcc1-5aca-88f2-b19422ab3fd2',
    '5385aa88-1e34-57fa-8c0c-fef655ca3773',
    '5466c6bf-67b2-52ac-ba83-a8cff7b8b42e',
    'c0d893dd-834a-539a-b0b9-cea32d756c9e',  -- ORG_ADMIN from seed
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
\echo '  Email:    admin@corpstage.com'
\echo '  Password: CorpStage#Admin2026!'
\echo '  Org UUID: 5466c6bf-67b2-52ac-ba83-a8cff7b8b42e'
\echo '  Role:     ORG_ADMIN'
\echo ''
\echo 'Run 06_bootstrap_verify.sql to confirm.'
\echo '======================================='
