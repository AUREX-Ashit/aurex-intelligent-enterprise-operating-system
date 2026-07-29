import uuid
import pytest
from fastapi.testclient import TestClient
from main import app
from config.settings import Settings

client = TestClient(app)


def test_root_endpoint():
    """
    Ensures primary index endpoint is online and returns platform stats.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "Aurex"
    assert data["service"] == "TenantService"
    assert "active_features" in data


def test_health_check_endpoint():
    """
    Ensures platform health returns success and confirms sub-system connections.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "ai_gateway" in data


def test_tenant_creation():
    """
    Verifies simple tenant CRUD works correctly.
    """
    payload = {
        "name": "Acme Widgets Inc",
        "domain": "acme.corpstage.com",
        "subscription_tier": "enterprise",
        "admin_email": "admin@acme.com",
        "admin_name": "Acme Admin",
        "config": {
            "theme": "dark",
            "allowed_domains": ["acme.com", "acme-portal.com"],
            "ai_settings": {"rag_enabled": True},
            "security_policies": {"mfa_required": True}
        }
    }
    response = client.post("/tenant/create", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Acme Widgets Inc"
    assert data["is_active"] is True
    assert "id" in data
    assert data["config"]["theme"] == "dark"


def test_tenant_onboarding():
    """
    Validates atomic onboarding workflows.
    """
    payload = {
        "company_name": "Stark Industries",
        "domain": "stark.corpstage.com",
        "admin_email": "tony@stark.com",
        "admin_name": "Tony Stark",
        "subscription_tier": "unlimited",
        "theme_preference": "light"
    }
    response = client.post("/tenant/onboard", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "tenant_id" in data
    assert "admin_user_id" in data


def test_tenant_users_header_required():
    """
    Assures X-Tenant-ID header checking. 400 Bad Request if missing.
    """
    response = client.get("/tenant/users")
    assert response.status_code == 400
    assert response.json()["detail"] == "Header 'X-Tenant-ID' is required for this operation."


def test_tenant_users_with_header():
    """
    Checks if users list are context filters when header is supplied.
    """
    mock_tenant_id = str(uuid.uuid4())
    headers = {"X-Tenant-ID": mock_tenant_id}
    response = client.get("/tenant/users", headers=headers)
    assert response.status_code == 200
    
    users = response.json()
    assert len(users) == 2
    for user in users:
        assert user["tenant_id"] == mock_tenant_id
        assert "email" in user
        assert "full_name" in user


def test_settings_overrides():
    """
    Validates Pydantic settings loading and fallback values.
    """
    test_settings = Settings()
    assert test_settings.platform.name == "Aurex"
    assert test_settings.database.postgresql.database_name == "aurex"
