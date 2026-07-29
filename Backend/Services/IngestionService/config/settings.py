import os
import yaml
from pathlib import Path
from typing import List, Optional
from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class IngestionLimits(BaseSettings):
    max_file_size_mb: int = 200
    allowed_extensions: List[str] = ["pdf", "xlsx", "csv", "docx"]

class DatabaseConfig(BaseSettings):
    primary_engine: str = "postgresql"
    host: str = "localhost"
    port: int = 5432
    database_name: str = "aurex"
    username: str = "aurex"
    password: Optional[str] = None
    pool_size: int = 30
    max_overflow: int = 10
    url: Optional[str] = None  # Full Postgres connection URL (overridden by env)

class JWTConfig(BaseSettings):
    algorithm: str = "HS256"
    access_token_expiry_minutes: int = 60
    refresh_token_expiry_days: int = 7
    header_name: str = "X-Tenant-ID"

class StorageConfig(BaseSettings):
    primary_provider: str = "azure_blob_storage"
    azure_container: str = "aurex-evidence"

class OCRConfig(BaseSettings):
    primary_provider: str = "azure_document_intelligence"
    azure_model: str = "prebuilt-layout"

class QueueConfig(BaseSettings):
    primary_provider: str = "azure_service_bus"

class Settings(BaseSettings):
    # App Settings
    app_name: str = "Aurex Ingestion Service"
    environment: str = "development"
    region: str = "centralindia"
    debug: bool = False
    
    # Ingestion Limits
    ingestion: IngestionLimits = Field(default_factory=IngestionLimits)

    # Auth and Tenancy
    auth: JWTConfig = Field(default_factory=JWTConfig)
    
    # Secrets & Engine Connections (Strict Environment Overrides only)
    # JWT_SECRET_KEY must never come from config file, strictly environment
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    
    # Database Settings
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # Storage details
    storage: StorageConfig = Field(default_factory=StorageConfig)
    
    # OCR configurations
    ocr: OCRConfig = Field(default_factory=OCRConfig)
    
    # Queue references
    queues: QueueConfig = Field(default_factory=QueueConfig)

    # Standard configuration source management
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True
    )

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret(cls, token_val: str) -> str:
        if not token_val or token_val == "CHANGE_IN_ENVIRONMENT" or len(token_val) < 16:
            raise ValueError("JWT_SECRET_KEY is unconfigured or too weak. Must be active Environment variable of length >= 16.")
        return token_val

    @field_validator("database")
    @classmethod
    def validate_database_url(cls, db_cfg: DatabaseConfig) -> DatabaseConfig:
        # Check if DATABASE_URL or database.url has been specified in environment
        # Under async SQL Alchemy, must prefix with postgresql+asyncpg://
        env_db_url = os.getenv("DATABASE_URL")
        if env_db_url:
            db_cfg.url = env_db_url
        
        if not db_cfg.url:
            # Fallback construct it if details are present in environment or YAML config
            pw = os.getenv("DATABASE_PASSWORD") or db_cfg.password
            if not pw or pw == "CHANGE_IN_ENVIRONMENT":
                raise ValueError("Postgres Database password must be supplied in environment variables via DATABASE_PASSWORD or DATABASE_URL.")
            db_cfg.url = f"postgresql+asyncpg://{db_cfg.username}:{pw}@{db_cfg.host}:{db_cfg.port}/{db_cfg.database_name}"
        
        # Ensure it is asyncpg active
        if db_cfg.url.startswith("postgresql://"):
            db_cfg.url = db_cfg.url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif not db_cfg.url.startswith("postgresql+asyncpg://"):
            raise ValueError("Database URL scheme must be compliant as active postgresql+asyncpg:// endpoint.")
            
        return db_cfg


def load_from_yaml_and_env() -> Settings:
    """
    Initializes system config starting from Config/platform-config.yaml,
    then layered and overridden with explicit standard Environment Variables.
    """
    yaml_config = {}
    
    # Resolve platform-config.yaml
    possible_yaml_paths = [
        Path("/Aurex/Config/platform-config.yaml"),
        Path(__file__).parents[2] / "Config" / "platform-config.yaml",
        Path(__file__).parents[3] / "Config" / "platform-config.yaml",
        Path("platform-config.yaml")
    ]
    
    resolved_yaml = None
    for p in possible_yaml_paths:
        if p.exists():
            resolved_yaml = p
            break
            
    if resolved_yaml:
        try:
            with open(resolved_yaml, "r") as f:
                yaml_data = yaml.safe_load(f)
                if isinstance(yaml_data, dict):
                    yaml_config = yaml_data
        except Exception as e:
            print(f"Warning: Failed to read platform-config.yaml: {e}")
            
    # Extract details safely from YAML data representation
    platform_data = yaml_config.get("platform", {})
    db_yaml = yaml_config.get("database", {})
    pg_yaml = db_yaml.get("postgresql", {}) if db_yaml.get("primary_engine") == "postgresql" else {}
    auth_yaml = yaml_config.get("authentication", {})
    jwt_yaml = auth_yaml.get("jwt", {})
    tenant_yaml = auth_yaml.get("tenant", {})
    storage_yaml = yaml_config.get("storage", {})
    az_blob = storage_yaml.get("azure_blob_storage", {}) if storage_yaml.get("primary_provider") == "azure_blob_storage" else {}
    ocr_yaml = yaml_config.get("ocr", {})
    az_ocr = ocr_yaml.get("azure_document_intelligence", {}) if ocr_yaml.get("primary_provider") == "azure_document_intelligence" else {}
    queue_yaml = yaml_config.get("queues", {})
    ingestion_limit_yaml = yaml_config.get("ingestion", {})
    
    # Build a combined dictionary prioritizing Environment variables
    combined_setup = {
        "app_name": os.getenv("APP_NAME") or platform_data.get("name") or "Aurex Ingestion Service",
        "environment": os.getenv("ENVIRONMENT") or platform_data.get("environment") or "development",
        "region": os.getenv("REGION") or platform_data.get("region") or "centralindia",
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "jwt_secret_key": os.getenv("JWT_SECRET_KEY"),  # mandatory in env
        
        "auth": {
            "algorithm": os.getenv("JWT_ALGORITHM") or jwt_yaml.get("algorithm") or "HS256",
            "access_token_expiry_minutes": int(os.getenv("JWT_ACCESS_EXPIRY_MINUTES") or jwt_yaml.get("access_token_expiry_minutes") or 60),
            "refresh_token_expiry_days": int(os.getenv("JWT_REFRESH_EXPIRY_DAYS") or jwt_yaml.get("refresh_token_expiry_days") or 7),
            "header_name": os.getenv("TENANT_HEADER_NAME") or tenant_yaml.get("header_name") or "X-Tenant-ID",
        },
        
        "database": {
            "primary_engine": os.getenv("DATABASE_ENGINE") or db_yaml.get("primary_engine") or "postgresql",
            "host": os.getenv("DATABASE_HOST") or pg_yaml.get("host") or "localhost",
            "port": int(os.getenv("DATABASE_PORT") or pg_yaml.get("port") or 5432),
            "database_name": os.getenv("DATABASE_NAME") or pg_yaml.get("database_name") or "aurex",
            "username": os.getenv("DATABASE_USERNAME") or pg_yaml.get("username") or "aurex",
            "password": os.getenv("DATABASE_PASSWORD") or pg_yaml.get("password"),
            "pool_size": int(os.getenv("DATABASE_POOL_SIZE") or pg_yaml.get("pool_size") or 30),
            "max_overflow": int(os.getenv("DATABASE_MAX_OVERFLOW") or pg_yaml.get("max_overflow") or 10),
            "url": os.getenv("DATABASE_URL")
        },
        
        "storage": {
            "primary_provider": os.getenv("STORAGE_PROVIDER") or storage_yaml.get("primary_provider") or "azure_blob_storage",
            "azure_container": os.getenv("AZURE_STORAGE_CONTAINER") or az_blob.get("container") or "aurex-evidence",
        },
        
        "ocr": {
            "primary_provider": os.getenv("OCR_PROVIDER") or ocr_yaml.get("primary_provider") or "azure_document_intelligence",
            "azure_model": os.getenv("AZURE_OCR_MODEL") or az_ocr.get("model") or "prebuilt-layout",
        },
        
        "queues": {
            "primary_provider": os.getenv("QUEUE_PROVIDER") or queue_yaml.get("primary_provider") or "azure_service_bus",
        },
        
        "ingestion": {
            "max_file_size_mb": int(os.getenv("INGESTION_MAX_FILE_SIZE_MB") or ingestion_limit_yaml.get("max_file_size_mb") or 200),
            "allowed_extensions": ingestion_limit_yaml.get("allowed_extensions") or ["pdf", "xlsx", "csv", "docx"]
        }
    }
    
    try:
        # Instantiate and validate
        return Settings(**combined_setup)
    except ValidationError as e:
        print("\n" + "="*80)
        print("CRITICAL: Aurex IngestionService startup blocked! Mandatory configuration missing.")
        print(f"Details: {e}")
        print("Please configure active Environment variables for required parameters like JWT_SECRET_KEY and DB constraints.")
        print("="*80 + "\n")
        raise SystemExit(1)

# Singleton application-wide configuration loader
settings = load_from_yaml_and_env()
