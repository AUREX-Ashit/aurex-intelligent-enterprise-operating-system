-- ==============================================================================
-- Aurex Enterprise SaaS Platform - Immutable Master Seed Script
-- Population of standard system roles, security permissions, taxonomy guidelines,
-- ESG Metrics codes (GRI/SASB standards) and United Nations 17 SDGs.
-- ==============================================================================

-- 1. Seed United Nations 17 Sustainable Development Goals (SDGs)
INSERT INTO sdg_goals (id, code, name, description, icon_url) VALUES
(1, 'SDG_01_NO_POVERTY', 'No Poverty', 'End poverty in all its forms everywhere.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-01.jpg'),
(2, 'SDG_02_ZERO_HUNGER', 'Zero Hunger', 'End hunger, achieve food security and improved nutrition and promote sustainable agriculture.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-02.jpg'),
(3, 'SDG_03_GOOD_HEALTH', 'Good Health and Well-being', 'Ensure healthy lives and promote well-being for all at all ages.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-03.jpg'),
(4, 'SDG_04_QUALITY_EDUCATION', 'Quality Education', 'Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-04.jpg'),
(5, 'SDG_05_GENDER_EQUALITY', 'Gender Equality', 'Achieve gender equality and empower all women and girls.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-05.jpg'),
(6, 'SDG_06_CLEAN_WATER', 'Clean Water and Sanitation', 'Ensure availability and sustainable management of water and sanitation for all.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-06.jpg'),
(7, 'SDG_07_AFFORDABLE_ENERGY', 'Affordable and Clean Energy', 'Ensure access to affordable, reliable, sustainable and modern energy for all.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-07.jpg'),
(8, 'SDG_08_DECENT_WORK', 'Decent Work and Economic Growth', 'Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-08.jpg'),
(9, 'SDG_09_INDUSTRY_INNOVATION', 'Industry, Innovation and Infrastructure', 'Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-09.jpg'),
(10, 'SDG_10_REDUCED_INEQUALITIES', 'Reduced Inequalities', 'Reduce inequality within and among countries.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-10.jpg'),
(11, 'SDG_11_SUSTAINABLE_CITIES', 'Sustainable Cities and Communities', 'Make cities and human settlements inclusive, safe, resilient and sustainable.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-11.jpg'),
(12, 'SDG_12_RESPONSIBLE_CONSUMPTION', 'Responsible Consumption and Production', 'Ensure sustainable consumption and production patterns.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-12.jpg'),
(13, 'SDG_13_CLIMATE_ACTION', 'Climate Action', 'Take urgent action to combat climate change and its impacts.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-13.jpg'),
(14, 'SDG_14_LIFE_BELOW_WATER', 'Life Below Water', 'Conserve and sustainably use the oceans, seas and marine resources for sustainable development.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-14.jpg'),
(15, 'SDG_15_LIFE_ON_LAND', 'Life on Land', 'Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-15.jpg'),
(16, 'SDG_16_PEACE_JUSTICE', 'Peace, Justice and Strong Institutions', 'Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-16.jpg'),
(17, 'SDG_17_PARTNERSHIPS', 'Partnerships for the Goals', 'Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development.', 'https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-17.jpg')
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    icon_url = EXCLUDED.icon_url;

-- 2. Seed Standard System Master ESG Metrics Reference Pool (Mapped to GRI index & SASB codes)
INSERT INTO esg_metrics (id, code, name, category, unit, gri_index, sasb_code, description) VALUES
-- Environmental (E) Metrics
(uuid_generate_v4(), 'GHG_SCOPE_1_EMISSIONS', 'Direct Greenhouse Gas (GHG) Emissions (Scope 1)', 'ENVIRONMENTAL', 'MT CO2e', 'GRI 305-1', 'EM-EP-110a.1', 'Direct greenhouse gas emissions from sources corporate-owned or fully controlled (e.g., combustion of fuels, fleet vehicles).'),
(uuid_generate_v4(), 'GHG_SCOPE_2_EMISSIONS', 'Indirect Energy Greenhouse Gas Emissions (Scope 2)', 'ENVIRONMENTAL', 'MT CO2e', 'GRI 305-2', 'EM-EP-110a.2', 'Indirect greenhouse gas emissions from the generation of acquired and consumed electricity, steam, heating, or cooling.'),
(uuid_generate_v4(), 'GHG_SCOPE_3_EMISSIONS', 'Other Indirect Greenhouse Gas Emissions (Scope 3)', 'ENVIRONMENTAL', 'MT CO2e', 'GRI 305-3', 'EM-EP-110a.3', 'All other indirect emissions that occur in the corporate value chain, including both upstream and downstream transitions.'),
(uuid_generate_v4(), 'ENERGY_CONSUMPTION_TOTAL', 'Total Direct Energy Consumption', 'ENVIRONMENTAL', 'MWh', 'GRI 302-1', 'RR-ST-130a.1', 'Total direct thermal and electrical energy consumed across operational boundaries.'),
(uuid_generate_v4(), 'WATER_WITHDRAWAL_TOTAL', 'Total Water Withdrawal Volume', 'ENVIRONMENTAL', 'm3', 'GRI 303-3', 'CG-HP-140a.1', 'Total volume of water drawn from ground, surface, municipal, or third-party facilities.'),
(uuid_generate_v4(), 'WASTE_HAZARDOUS_GENERATED', 'Hazardous Waste Generated Outflows', 'ENVIRONMENTAL', 'MT', 'GRI 306-3', 'IF-WM-150a.1', 'Total mass of hazardous wastes generated inside manufacturing or site operations.'),

-- Social (S) Metrics
(uuid_generate_v4(), 'DIVERSITY_GENDER_RATIO', 'Gender Ratio Representation (Female Participation)', 'ENVIRONMENTAL', 'PERCENT', 'GRI 405-1', 'HC-DY-330a.1', 'Percentage representation of female counterparts in full-time workforce positions.'),
(uuid_generate_v4(), 'WORKFORCE_TURNOVER_RATE', 'Workforce Annual Regretted Turnover Rate', 'SOCIAL', 'PERCENT', 'GRI 401-1', 'SV-ED-230a.1', 'Annual percentage rate describing active personnel resignations or layoffs within monitoring scopes.'),
(uuid_generate_v4(), 'OCCUPATIONAL_INJURY_RATE', 'Occupational Recordable Injury Rate (TRIR)', 'SOCIAL', 'RATIO', 'GRI 403-9', 'EM-EP-320a.1', 'Total Recordable Injury Rate calculated per two hundred thousand cumulative work-hours.'),

-- Governance (G) Metrics
(uuid_generate_v4(), 'BOARD_INDEPENDENCE_RATIO', 'Independent Board Council Percentage', 'GOVERNANCE', 'PERCENT', 'GRI 2-9', 'IF-EU-000a.1', 'Percentage of active Board of Directors recognized as fully independent officers.'),
(uuid_generate_v4(), 'ANTI_CORRUPTION_TRAINING', 'Anti-Corruption Code Alignment Training', 'GOVERNANCE', 'PERCENT', 'GRI 205-2', 'SV-PS-510a.1', 'Percentage of eligible directors, supervisors, and employees trained in anti-corruption guidelines.')
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    unit = EXCLUDED.unit,
    gri_index = EXCLUDED.gri_index,
    sasb_code = EXCLUDED.sasb_code,
    description = EXCLUDED.description;

-- 3. Seed Security Operational Permission Scopes
INSERT INTO permissions (code, name, description) VALUES
('tenant:read', 'Read Tenant Parameters', 'Allows reading parent workspace setups.'),
('tenant:write', 'Write Tenant Parameters', 'Allows setting subdomains and connections.'),
('user:read', 'Read Core Users List', 'Allows view of directory accounts.'),
('user:write', 'Write User Records', 'Allows setting credentials and passwords.'),
('document:read', 'Read Uploaded Files', 'Allows viewing metadata databases.'),
('document:write', 'Write File Payload Storage', 'Allows uploading files into S3 vault storage.'),
('metric:read', 'Read Standard Metrics', 'Allows tracking historical sustainability values.'),
('metric:edit', 'Edit Metric Values', 'Allows modifying captured values.'),
('ai:extract', 'Run Extraction Models', 'Allows invoking Gemini pipelines to target texts.'),
('score:view', 'Read ESG Assessments', 'Allows consulting computed ratings indices.'),
('report:review', 'Review Analytics Reports', 'Allows draft reviews and signing releases.'),
('report:export', 'Sign and Export Audited Disclosures', 'Allows downloading compiled standard PDF disclosure documents.')
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description;

-- 4. Seed Standard Role Archetypes
INSERT INTO roles (name, description) VALUES
('SystemAdmin', 'Global System administrator. Bypasses tenant RLS scopes to manage host metrics and system configs.'),
('TenantAdmin', 'Tenant owner account. Full operational privileges across nested client user directories.'),
('DataIngester', 'Workforce analyst role focused on sustainability document uploads and ESG parameter streams.'),
('ESGEditor', 'Compliance specialist managing ESG metrics, validations, overrides, and report compiles.'),
('Auditor', 'View-only third party audit specialist verifying documentation, validation logs, and history trails.')
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description;

-- 5. Establish Role-Permission Mapping Matrices
-- Clean old mappings to prevent duplicate conflicts
DELETE FROM role_permissions;

DO $$
DECLARE
    role_sys_admin_id UUID;
    role_tenant_admin_id UUID;
    role_ingester_id UUID;
    role_editor_id UUID;
    role_auditor_id UUID;
    
    perm_tenant_r UUID; perm_tenant_w UUID;
    perm_user_r UUID; perm_user_w UUID;
    perm_doc_r UUID; perm_doc_w UUID;
    perm_metric_r UUID; perm_metric_w UUID;
    perm_ai UUID; perm_score UUID;
    perm_report_r UUID; perm_report_w UUID;
BEGIN
    -- Pull IDs safely
    SELECT id INTO role_sys_admin_id FROM roles WHERE name = 'SystemAdmin';
    SELECT id INTO role_tenant_admin_id FROM roles WHERE name = 'TenantAdmin';
    SELECT id INTO role_ingester_id FROM roles WHERE name = 'DataIngester';
    SELECT id INTO role_editor_id FROM roles WHERE name = 'ESGEditor';
    SELECT id INTO role_auditor_id FROM roles WHERE name = 'Auditor';

    SELECT id INTO perm_tenant_r FROM permissions WHERE code = 'tenant:read';
    SELECT id INTO perm_tenant_w FROM permissions WHERE code = 'tenant:write';
    SELECT id INTO perm_user_r FROM permissions WHERE code = 'user:read';
    SELECT id INTO perm_user_w FROM permissions WHERE code = 'user:write';
    SELECT id INTO perm_doc_r FROM permissions WHERE code = 'document:read';
    SELECT id INTO perm_doc_w FROM permissions WHERE code = 'document:write';
    SELECT id INTO perm_metric_r FROM permissions WHERE code = 'metric:read';
    SELECT id INTO perm_metric_w FROM permissions WHERE code = 'metric:edit';
    SELECT id INTO perm_ai FROM permissions WHERE code = 'ai:extract';
    SELECT id INTO perm_score FROM permissions WHERE code = 'score:view';
    SELECT id INTO perm_report_r FROM permissions WHERE code = 'report:review';
    SELECT id INTO perm_report_w FROM permissions WHERE code = 'report:export';

    -- SystemAdmin privileges (Agnostic access)
    INSERT INTO role_permissions (role_id, permission_id) VALUES
    (role_sys_admin_id, perm_tenant_r), (role_sys_admin_id, perm_tenant_w),
    (role_sys_admin_id, perm_user_r), (role_sys_admin_id, perm_user_w);

    -- TenantAdmin privileges (Full localized scope)
    INSERT INTO role_permissions (role_id, permission_id) VALUES
    (role_tenant_admin_id, perm_tenant_r), (role_tenant_admin_id, perm_user_r), (role_tenant_admin_id, perm_user_w),
    (role_tenant_admin_id, perm_doc_r), (role_tenant_admin_id, perm_doc_w),
    (role_tenant_admin_id, perm_metric_r), (role_tenant_admin_id, perm_metric_w),
    (role_tenant_admin_id, perm_ai), (role_tenant_admin_id, perm_score),
    (role_tenant_admin_id, perm_report_r), (role_tenant_admin_id, perm_report_w);

    -- DataIngester privileges
    INSERT INTO role_permissions (role_id, permission_id) VALUES
    (role_ingester_id, perm_doc_r), (role_ingester_id, perm_doc_w),
    (role_ingester_id, perm_metric_r), (role_ingester_id, perm_metric_w);

    -- ESGEditor privileges
    INSERT INTO role_permissions (role_id, permission_id) VALUES
    (role_editor_id, perm_doc_r), (role_editor_id, perm_metric_r), (role_editor_id, perm_metric_w),
    (role_editor_id, perm_ai), (role_editor_id, perm_score),
    (role_editor_id, perm_report_r), (role_editor_id, perm_report_w);

    -- Auditor privileges
    INSERT INTO role_permissions (role_id, permission_id) VALUES
    (role_auditor_id, perm_doc_r), (role_auditor_id, perm_metric_r),
    (role_auditor_id, perm_score), (role_auditor_id, perm_report_r);
END
$$;
