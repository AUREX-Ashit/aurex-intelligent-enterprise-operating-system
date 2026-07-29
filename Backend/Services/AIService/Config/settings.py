# config/settings.py
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Platform Core
    platform_name: str = "Aurex"
    environment: str = "development"
    region: str = "centralindia"

    # Database Settings
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "aurex"
    db_user: str = "aurex"
    db_pass: str = "CHANGE_IN_ENVIRONMENT"
    db_pool_size: int = 30
    db_max_overflow: int = 10
    
    # Generated Database URL
    database_url: Optional[str] = None

    # AI Config
    ai_primary_provider: str = "azure_openai"
    ai_endpoint: str = "YOUR_AZURE_OPENAI_ENDPOINT"
    ai_api_version: str = "2024-02-15-preview"
    
    # Selected Models
    primary_llm: str = "gpt-4o"
    lightweight_llm: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-large"

    # Storage and queues
    storage_provider: str = "azure_blob_storage"
    storage_container: str = "aurex-evidence"
    queue_provider: str = "azure_service_bus"

    # Security and MFA
    jwt_secret_key: str = Field(default=...)  # Must come only from env, mandatory!
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60
    tenant_header_name: str = "X-Tenant-ID"

    # Cost standards & Limits
    max_file_size_mb: int = 200
    allowed_extensions: List[str] = ["pdf", "xlsx", "csv", "docx"]

    # AI Governance flags
    hallucination_detection: bool = True
    grounded_responses_only: bool = True
    confidence_scoring_enabled: bool = True
    human_review_required: bool = True

    # Feature Flags
    enable_copilot: bool = True
    enable_rag: bool = True
    enable_financial_intelligence: bool = True
    enable_bulk_validation: bool = True

    class Config:
        env_prefix = "AUREX_"
        case_sensitive = False

    @classmethod
    def load_from_yaml(cls) -> "Settings":
        """Loads default values from platform-config.yaml, allowing system env-vars to override."""
        yaml_content: Dict[str, Any] = {}
        
        # Navigate from config/settings.py to find platform-config.yaml
        config_paths = [
            Path(__file__).parent.parent / "Config" / "platform-config.yaml",
            Path("Config/platform-config.yaml"),
            Path("platform-config.yaml"),
        ]
        
        for p in config_paths:
            if p.exists():
                try:
                    with open(p, "r") as f:
                        yaml_content = yaml.safe_load(f) or {}
                    break
                except Exception:
                    pass

        # Build initial overrides dictionary matching class fields
        init_kwargs = {}

        # Parse platform details
        platform_block = yaml_content.get("platform", {})
        if "name" in platform_block: init_kwargs["platform_name"] = platform_block["name"]
        if "environment" in platform_block: init_kwargs["environment"] = platform_block["environment"]
        if "region" in platform_block: init_kwargs["region"] = platform_block["region"]

        # Parse DB details
        db_block = yaml_content.get("database", {})
        pg_block = db_block.get("postgresql", {}) if db_block else {}
        if pg_block:
            if "host" in pg_block: init_kwargs["db_host"] = pg_block["host"]
            if "port" in pg_block: init_kwargs["db_port"] = pg_block["port"]
            if "database_name" in pg_block: init_kwargs["db_name"] = pg_block["database_name"]
            if "username" in pg_block: init_kwargs["db_user"] = pg_block["username"]
            if "password" in pg_block: init_kwargs["db_pass"] = pg_block["password"]
            if "pool_size" in pg_block: init_kwargs["db_pool_size"] = pg_block["pool_size"]
            if "max_overflow" in pg_block: init_kwargs["db_max_overflow"] = pg_block["max_overflow"]

        # Parse Authentication details & Headers
        auth_block = yaml_content.get("authentication", {})
        jwt_block = auth_block.get("jwt", {}) if auth_block else {}
        if jwt_block:
            if "algorithm" in jwt_block: init_kwargs["jwt_algorithm"] = jwt_block["algorithm"]
            if "access_token_expiry_minutes" in jwt_block: 
                init_kwargs["jwt_expiry_minutes"] = jwt_block["access_token_expiry_minutes"]
        tenant_block = auth_block.get("tenant", {}) if auth_block else {}
        if tenant_block and "header_name" in tenant_block:
            init_kwargs["tenant_header_name"] = tenant_block["header_name"]

        # Parse AI integrations
        ai_block = yaml_content.get("ai", {})
        if ai_block:
            if "primary_provider" in ai_block: init_kwargs["ai_primary_provider"] = ai_block["primary_provider"]
            prov_details = ai_block.get("providers", {}).get(ai_block.get("primary_provider", ""), {})
            if prov_details:
                if "endpoint" in prov_details: init_kwargs["ai_endpoint"] = prov_details["endpoint"]
                if "api_version" in prov_details: init_kwargs["ai_api_version"] = prov_details["api_version"]
                models_block = prov_details.get("models", {})
                if models_block:
                    if "primary_llm" in models_block: init_kwargs["primary_llm"] = models_block["primary_llm"]
                    if "lightweight_llm" in models_block: init_kwargs["lightweight_llm"] = models_block["lightweight_llm"]
                    if "embedding_model" in models_block: init_kwargs["embedding_model"] = models_block["embedding_model"]

        # Ingestion limits
        ingest_block = yaml_content.get("ingestion", {})
        if ingest_block:
            if "max_file_size_mb" in ingest_block: init_kwargs["max_file_size_mb"] = ingest_block["max_file_size_mb"]
            if "allowed_extensions" in ingest_block: init_kwargs["allowed_extensions"] = ingest_block["allowed_extensions"]

        # Feature flags
        feature_block = yaml_content.get("feature_flags", {})
        if feature_block:
            if "enable_copilot" in feature_block: init_kwargs["enable_copilot"] = feature_block["enable_copilot"]
            if "enable_rag" in feature_block: init_kwargs["enable_rag"] = feature_block["enable_rag"]
            if "enable_financial_intelligence" in feature_block: init_kwargs["enable_financial_intelligence"] = feature_block["enable_financial_intelligence"]
            if "enable_bulk_validation" in feature_block: init_kwargs["enable_bulk_validation"] = feature_block["enable_bulk_validation"]

        # Governance
        g_block = yaml_content.get("ai_governance", {})
        if g_block:
            if "hallucination_detection" in g_block: init_kwargs["hallucination_detection"] = g_block["hallucination_detection"]
            if "grounded_responses_only" in g_block: init_kwargs["grounded_responses_only"] = g_block["grounded_responses_only"]
            if "confidence_scoring_enabled" in g_block: init_kwargs["confidence_scoring_enabled"] = g_block["confidence_scoring_enabled"]
            if "human_review_required" in g_block: init_kwargs["human_review_required"] = g_block["human_review_required"]

        # Extract JWT Secret Key directly from Environment only. Throw error if missing.
        jwt_key = os.getenv("AUREX_JWT_SECRET_KEY") or os.getenv("JWT_SECRET_KEY")
        if not jwt_key:
            # Fallback for local simulation or testing so it doesn't instantly block developers,
            # but in production, we fail application startup if missing.
            if os.getenv("AUREX_ENVIRONMENT", "development") == "production":
                raise ValueError("CRITICAL CONFIGURATION ERROR: JWT_SECRET_KEY must be provided via environments!")
            jwt_key = "aurex-development-secret-key-safe-fallback"

        init_kwargs["jwt_secret_key"] = jwt_key

        # Environment variable overrides for DB details (Standard practice)
        db_user = os.getenv("AUREX_DB_USER", init_kwargs.get("db_user", "aurex"))
        db_pass = os.getenv("AUREX_DB_PASS", init_kwargs.get("db_pass", "CHANGE_IN_ENVIRONMENT"))
        db_host = os.getenv("AUREX_DB_HOST", init_kwargs.get("db_host", "localhost"))
        db_port = int(os.getenv("AUREX_DB_PORT", str(init_kwargs.get("db_port", 5432))))
        db_name = os.getenv("AUREX_DB_NAME", init_kwargs.get("db_name", "aurex"))

        # Build Database URL
        # For our scaffolding / SQLite testing base, support sqlite+aiosqlite if specified, otherwise asyncpg
        db_url = os.getenv("AUREX_DATABASE_URL")
        if not db_url:
            if db_pass == "CHANGE_IN_ENVIRONMENT" and os.getenv("AUREX_ENVIRONMENT") != "production":
                # Development safe fallback: SQLite in-memory or file-based for instant testing
                init_kwargs["database_url"] = "sqlite+aiosqlite:///aurex.db"
            else:
                init_kwargs["database_url"] = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        else:
            init_kwargs["database_url"] = db_url

        # Initialize BaseSettings (Pydantic will auto-bind matching fields)
        return cls(**init_kwargs)

try:
    settings = Settings.load_from_yaml()
except Exception as e:
    import sys
    print(f"FAILED TO INITIATE SETTINGS MANAGER: {str(e)}", file=sys.stderr)
    raise e
