import os
from typing import List, Optional
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class PlatformConfig(BaseModel):
    name: str = "CorpStage"
    environment: str = "development"
    region: str = "centralindia"

class ProviderConfig(BaseModel):
    enabled: bool = False
    region: str = "centralindia"

class CloudConfig(BaseModel):
    primary_provider: str = "azure"
    providers: dict = {}

class ModelSpec(BaseModel):
    primary_llm: str = "gpt-4o"
    lightweight_llm: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-large"

class AzureOpenAIConfig(BaseModel):
    enabled: bool = True
    endpoint: str = "YOUR_AZURE_OPENAI_ENDPOINT"
    api_version: str = "2024-02-15-preview"
    models: ModelSpec = ModelSpec()

class AIProviders(BaseModel):
    azure_openai: AzureOpenAIConfig = AzureOpenAIConfig()
    claude: dict = {"enabled": False}
    gemini: dict = {"enabled": False}

class AIConfig(BaseModel):
    primary_provider: str = "azure_openai"
    providers: AIProviders = AIProviders()

class JWTConfig(BaseModel):
    algorithm: str = "HS256"
    access_token_expiry_minutes: int = 60
    refresh_token_expiry_days: int = 7

class TenantHeaderConfig(BaseModel):
    header_name: str = "X-Tenant-ID"

class AuthConfig(BaseModel):
    jwt: JWTConfig = JWTConfig()
    tenant: TenantHeaderConfig = TenantHeaderConfig()

class PostgresConfig(BaseModel):
    enabled: bool = True
    version: str = "16"
    host: str = "localhost"
    port: int = 5432
    database_name: str = "corpstage"
    username: str = "corpstage"
    password: str = "CHANGE_IN_ENVIRONMENT"
    pool_size: int = 30
    max_overflow: int = 10

class DatabaseConfig(BaseModel):
    primary_engine: str = "postgresql"
    postgresql: PostgresConfig = PostgresConfig()

class CorsConfig(BaseModel):
    allow_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]

class SecurityConfig(BaseModel):
    enable_mfa: bool = True
    enable_rls: bool = True
    enforce_tls: bool = True

class FeatureFlags(BaseModel):
    enable_copilot: bool = True
    enable_rag: bool = True
    enable_financial_intelligence: bool = True
    enable_bulk_validation: bool = True


class Settings(BaseSettings):
    """
    Production-grade Settings using Pydantic Settings.
    Initializes values from platform-config.yaml and allows overrides via ENV variables.
    """
    model_config = SettingsConfigDict(
        env_prefix="CORPSTAGE_",
        env_nested_delimiter="__",
        extra="ignore"
    )

    platform: PlatformConfig = PlatformConfig()
    cloud: CloudConfig = CloudConfig()
    ai: AIConfig = AIConfig()
    authentication: AuthConfig = AuthConfig()
    database: DatabaseConfig = DatabaseConfig()
    cors: CorsConfig = CorsConfig()
    security: SecurityConfig = SecurityConfig()
    feature_flags: FeatureFlags = FeatureFlags()

    @classmethod
    def load_from_yaml(cls, yaml_path: str = None) -> "Settings":
        """
        Loads platform-config.yaml and instantiates Settings with high priority to environment overrides.
        """
        if not yaml_path:
            # Look in standard locations
            possible_paths = [
                "config/platform-config.yaml",
                "platform-config.yaml",
                "/app/config/platform-config.yaml",
                "TenantService/config/platform-config.yaml"
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    yaml_path = path
                    break

        yaml_data = {}
        if yaml_path and os.path.exists(yaml_path):
            try:
                with open(yaml_path, 'r') as f:
                    yaml_data = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Failed to load configuration from {yaml_path}: {e}")

        # Instantiate from dict loaded from YAML, Pydantic automatically lets Environment overrides take precedence
        return cls(**yaml_data)

    @property
    def database_url(self) -> str:
        """
        Generates highly detailed Async PostgreSQL database URL.
        """
        pg = self.database.postgresql
        # Standard asyncpg driver for SQLAlchemy
        return f"postgresql+asyncpg://{pg.username}:{pg.password}@{pg.host}:{pg.port}/{pg.database_name}"

# Global singleton configuration initialization
settings = Settings.load_from_yaml()
