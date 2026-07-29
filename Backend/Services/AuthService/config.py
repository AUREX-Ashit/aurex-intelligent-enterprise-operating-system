import os
import logging
from typing import Any, Dict, List, Optional
import yaml

logger = logging.getLogger(__name__)

class Settings:
    """
    Platform-wide configuration loader for all Aurex services.
    Loads values from Config/platform-config.yaml with modern system overrides.
    """
    def __init__(self) -> None:
        self.database_url: Optional[str] = None
        self.jwt_algorithm: str = "HS256"
        self.access_token_expiry_minutes: int = 60
        self.refresh_token_expiry_days: int = 7

        # Dynamic CORS values
        self.cors_origins: List[str] = ["https://corpstage.com"]
        self.cors_credentials: bool = True
        self.cors_methods: List[str] = ["*"]
        self.cors_headers: List[str] = ["*"]

        # Feature flags (WP-00) — {flag_name: {"enabled": bool, "organizations": [str, ...] | None}}
        self.feature_flags: Dict[str, Dict[str, Any]] = {}

        # Bootstrap (WP-00) — enables/disables the idempotent seed stage
        self.bootstrap_enabled: bool = True

        # Environment (WP-00 remediation, IC-001 M1) — gates whether
        # bootstrap may seed built-in demo credentials as-is. Defaults to
        # "development"; only ENVIRONMENT=production (or "prod") is treated
        # as production. See services/bootstrap_service.py.
        self.environment: str = "development"

        # Parse from Config/platform-config.yaml
        self._load_from_yaml()

        # Apply system environment overrides
        self._load_from_env()

    def _load_from_yaml(self) -> None:
        """
        Locates and resolves platform-config.yaml.
        Prioritizes the Config/ directory location.
        """
        possible_paths = [
            os.path.join(os.getcwd(), "Config", "platform-config.yaml"),
            os.path.join(os.getcwd(), "platform-config.yaml"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "Config", "platform-config.yaml"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "platform-config.yaml"),
        ]

        resolved_path = None
        for path in possible_paths:
            if os.path.exists(path):
                resolved_path = path
                break

        if not resolved_path:
            logger.warning("No configuration file found in any searched directory paths.")
            return

        try:
            with open(resolved_path, "r") as f:
                config_data = yaml.safe_load(f)
                if not config_data:
                    return

                # Read Database Section
                if "database" in config_data and config_data["database"]:
                    db_cfg = config_data["database"]
                    if db_cfg.get("url"):
                        self.database_url = db_cfg["url"]
                    elif all(db_cfg.get(k) for k in ("host", "port", "database_name", "username")):
                        self.database_url = (
                            f"postgresql+asyncpg://{db_cfg['username']}:{db_cfg.get('password', '')}"
                            f"@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['database_name']}"
                        )

                # Read Authentication Parameters Section
                if "auth" in config_data and config_data["auth"]:
                    auth_cfg = config_data["auth"]
                    if "jwt_algorithm" in auth_cfg:
                        self.jwt_algorithm = str(auth_cfg["jwt_algorithm"])
                    if "access_token_expiry_minutes" in auth_cfg:
                        self.access_token_expiry_minutes = int(auth_cfg["access_token_expiry_minutes"])
                    if "refresh_token_expiry_days" in auth_cfg:
                        self.refresh_token_expiry_days = int(auth_cfg["refresh_token_expiry_days"])

                # Read CORS Network parameters
                if "cors" in config_data and config_data["cors"]:
                    cors_cfg = config_data["cors"]
                    if "allow_origins" in cors_cfg:
                        self.cors_origins = cors_cfg["allow_origins"]
                    if "allow_credentials" in cors_cfg:
                        self.cors_credentials = bool(cors_cfg["allow_credentials"])
                    if "allow_methods" in cors_cfg:
                        self.cors_methods = cors_cfg["allow_methods"]
                    if "allow_headers" in cors_cfg:
                        self.cors_headers = cors_cfg["allow_headers"]

                # Read Feature Flags Section (WP-00)
                if "feature_flags" in config_data and config_data["feature_flags"]:
                    self.feature_flags = dict(config_data["feature_flags"])

                # Read Bootstrap Section (WP-00)
                if "bootstrap" in config_data and config_data["bootstrap"]:
                    bootstrap_cfg = config_data["bootstrap"]
                    if "enabled" in bootstrap_cfg:
                        self.bootstrap_enabled = bool(bootstrap_cfg["enabled"])

                logger.info(f"Configurations parsed successfully from {resolved_path}")
        except Exception as e:
            logger.warning(f"Failed to read settings from {resolved_path}: {e}")

    def _load_from_env(self) -> None:
        """
        Applies environment overrides on top of standard configuration properties.
        """
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            self.database_url = db_url

        algorithm = os.getenv("JWT_ALGORITHM")
        if algorithm:
            self.jwt_algorithm = algorithm

        access_expiry = os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES")
        if access_expiry is not None:
            try:
                self.access_token_expiry_minutes = int(access_expiry)
            except ValueError:
                pass

        refresh_expiry = os.getenv("REFRESH_TOKEN_EXPIRY_DAYS")
        if refresh_expiry is not None:
            try:
                self.refresh_token_expiry_days = int(refresh_expiry)
            except ValueError:
                pass

        # Network CORS configurations override
        env_origins = os.getenv("CORS_ALLOW_ORIGINS")
        if env_origins:
            self.cors_origins = [o.strip() for o in env_origins.split(",") if o.strip()]

        env_credentials = os.getenv("CORS_ALLOW_CREDENTIALS")
        if env_credentials is not None:
            self.cors_credentials = env_credentials.lower() in ("true", "1", "yes", "on")

        env_methods = os.getenv("CORS_ALLOW_METHODS")
        if env_methods:
            self.cors_methods = [m.strip() for m in env_methods.split(",") if m.strip()]

        env_headers = os.getenv("CORS_ALLOW_HEADERS")
        if env_headers:
            self.cors_headers = [h.strip() for h in env_headers.split(",") if h.strip()]

        # Feature flag overrides: FF_<FLAG_NAME>=true|false, e.g. FF_IDENTITY_AUTH_V1=false.
        # Only toggles the "enabled" bit for an already-declared flag; does not declare new ones.
        for flag_name in list(self.feature_flags.keys()):
            env_key = f"FF_{flag_name.upper()}"
            env_value = os.getenv(env_key)
            if env_value is not None:
                self.feature_flags[flag_name]["enabled"] = env_value.lower() in ("true", "1", "yes", "on")

        env_bootstrap = os.getenv("BOOTSTRAP_ENABLED")
        if env_bootstrap is not None:
            self.bootstrap_enabled = env_bootstrap.lower() in ("true", "1", "yes", "on")

        env_environment = os.getenv("ENVIRONMENT")
        if env_environment:
            self.environment = env_environment.lower()

    @property
    def jwt_secret_key(self) -> str:
        """
        Retrieves JWT_SECRET_KEY exclusively from environment variables.
        Guarantees no fallbacks to yaml configuration for key secrets.
        """
        secret = os.getenv("JWT_SECRET_KEY")
        if not secret:
            raise RuntimeError(
                "JWT_SECRET_KEY environment variable is not defined. "
                "For security reasons, this setting must be provided strictly via environment."
            )
        return secret


# Instantiated Singleton Configuration Loader
settings = Settings()
