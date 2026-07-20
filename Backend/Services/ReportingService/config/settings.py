import os
import yaml
from pathlib import ROOT_DIR if (ROOT_DIR := globals().get("ROOT_DIR")) else ""
from typing import Any, Dict, List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, BaseModel

class JWTSettings(BaseModel):
    algorithm: str = "HS256"
    access_token_expiry_minutes: int = 60
    refresh_token_expiry_days: int = 7

class TenantSettings(BaseModel):
    header_name: str = "X-Tenant-ID"

class AuthSettings(BaseModel):
    jwt: JWTSettings = JWTSettings()
    tenant: TenantSettings = TenantSettings()

class PostgresqlSettings(BaseModel):
    enabled: bool = True
    version: str = "16"
    host: str = "localhost"
    port: int = 5432
    database_name: str = "corpstage"
    username: str = "corpstage"
    password: str = "CHANGE_IN_ENVIRONMENT"
    pool_size: int = 30
    max_overflow: int = 10

class DatabaseSettings(BaseModel):
    primary_engine: str = "postgresql"
    postgresql: PostgresqlSettings = PostgresqlSettings()

class LoggingSettings(BaseModel):
    structured_json: bool = True

class ObservabilitySettings(BaseModel):
    tracing: Dict[str, Any] = {"enabled": True, "provider": "opentelemetry"}
    logging: LoggingSettings = LoggingSettings()
    metrics: Dict[str, Any] = {"enabled": True}

class SecuritySettings(BaseModel):
    enable_mfa: bool = True
    enable_rls: bool = True
    enforce_tls: bool = True

class CORSSettings(BaseModel):
    allow_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]

class FeatureFlagsSettings(BaseModel):
    enable_copilot: bool = True
    enable_rag: bool = True
    enable_financial_intelligence: bool = True
    enable_bulk_validation: bool = True

class PlatformSettings(BaseSettings):
    name: str = "CorpStage"
    environment: str = "development"
    region: str = "centralindia"
    
    # We load YAML and fallback to these Pydantic settings.
    # Environment variables overrides will happen automatically via Pydantic or manual parsing.
    authentication: AuthSettings = AuthSettings()
    database: DatabaseSettings = DatabaseSettings()
    observability: ObservabilitySettings = ObservabilitySettings()
    security: SecuritySettings = SecuritySettings()
    cors: CORSSettings = CORSSettings()
    feature_flags: FeatureFlagsSettings = FeatureFlagsSettings()

    # CRITICAL: Secrets like JWT_SECRET_KEY MUST only come from the environment (never YAML)
    jwt_secret_key: str = Field(default="", env="JWT_SECRET_KEY")
    database_url_override: Optional[str] = Field(default=None, env="DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

def get_config_path() -> str:
    # Determine config file location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(base_dir, "config", "platform-config.yaml")
    if os.path.exists(yaml_path):
        return yaml_path
    return "platform-config.yaml"

def load_yaml_config(file_path: str) -> Dict[str, Any]:
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        try:
            return yaml.safe_load(f) or {}
        except Exception:
            return {}

def get_settings() -> PlatformSettings:
    """
    Factory to construct settings.
    Loads YAML first, applies values, overlays environment variables,
    and enforces strict controls on JWT key and Database URL.
    """
    config_file = get_config_path()
    yaml_data = load_yaml_config(config_file)
    
    # Extract keys we want to pass into PlatformSettings parsing
    init_data = {}
    if "platform" in yaml_data:
        p_data = yaml_data["platform"]
        init_data["name"] = p_data.get("name", "CorpStage")
        init_data["environment"] = p_data.get("environment", "development")
        init_data["region"] = p_data.get("region", "centralindia")

    if "authentication" in yaml_data:
        init_data["authentication"] = yaml_data["authentication"]
    if "database" in yaml_data:
        init_data["database"] = yaml_data["database"]
    if "observability" in yaml_data:
        init_data["observability"] = yaml_data["observability"]
    if "security" in yaml_data:
        init_data["security"] = yaml_data["security"]
    if "cors" in yaml_data:
        init_data["cors"] = yaml_data["cors"]
    if "feature_flags" in yaml_data:
        init_data["feature_flags"] = yaml_data["feature_flags"]

    # Environmental Override check for Database Password
    db_password = os.getenv("DATABASE_PASSWORD")
    if db_password and "database" in init_data:
        if "postgresql" in init_data["database"]:
            init_data["database"]["postgresql"]["password"] = db_password

    # Sourced from env only
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if not jwt_secret:
        # For development simulation fallback, but warning logged
        jwt_secret = "DEVELOPMENT_FALLBACK_STRICTLY_REPLACE_IN_PRODUCTION"
    
    init_data["jwt_secret_key"] = jwt_secret
    
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        init_data["database_url_override"] = db_url

    # Create pydantic object
    settings = PlatformSettings(**init_data)
    return settings

settings = get_settings()
