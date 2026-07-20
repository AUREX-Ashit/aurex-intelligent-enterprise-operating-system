"""
CorpStage Shared Configuration Framework - Config Loader Module.

This is the main entry point and orchestrator. It loads YAML, overlays
environment overrides, validates required inputs, processes JWT validation,
and maps the structures into the SettingsManager for typed access.
"""

import os
import logging
from typing import Dict, Any, Optional

from corpstage.backend.shared.config.exceptions import (
    ConfigError,
    YAMLValidationError,
    MissingRequiredValueError
)
from corpstage.backend.shared.config.yaml_parser import YAMLParser
from corpstage.backend.shared.config.environment_manager import EnvironmentManager
from corpstage.backend.shared.config.settings_manager import SettingsManager, SettingsNode

# Set up logging for CorpStage Shared Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("CorpStage.Config.Loader")


class ConfigLoader:
    """
    Coordination layer that manages the configuration lifecycle from file discovery,
    YAML compilation, environmental overlays, runtime validation, and globally available settings distribution.
    """

    DEFAULT_CONFIG_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "platform-config.yaml"
    )

    @staticmethod
    def initialize(
        service_name: str,
        config_file_path: Optional[str] = None
    ) -> SettingsNode:
        """
        Coordinates the compilation, override resolution, and validation of CorpStage
        configuration properties, committing them into a frozen, typed representation.
        
        Args:
            service_name: Name of the application startup service (e.g., 'AuthService', 'AIService').
            config_file_path: Alternative YAML configuration path. Defaults to local directory yaml.
            
        Returns:
            SettingsNode: Loaded and validation-verified configuration interface.
            
        Raises:
            ConfigError: When configuration parsing or integrity verification fails.
        """
        logger.info(f"Initializing CorpStage Share Configuration Framework for service: [{service_name}]")

        path_to_load = config_file_path or ConfigLoader.DEFAULT_CONFIG_PATH
        logger.info(f"Loading base platform configuration values from: {path_to_load}")

        # 1. Read Base Config File
        base_raw = YAMLParser.load_file(path_to_load)

        # 2. Get and Apply Environment Overrides
        overrides = EnvironmentManager.get_overrides()
        if overrides:
            logger.info("Found active CORPSTAGE_ environment variables. Applying overrides...")
            logger.debug(f"Environment overrides detected: {list(overrides.keys())}")
            final_raw = EnvironmentManager.apply_overrides(base_raw, overrides)
        else:
            logger.info("No environment overrides detected. Using YAML definitions.")
            final_raw = base_raw

        # 3. Enforce and Validate JWT and Secrets
        logger.info("Enforcing corporate security, credential extraction, and environment validation rules...")
        final_raw = EnvironmentManager.enforce_secrets(final_raw)

        # 4. Run Structural Validations for Core Architecture and Service-specific bounds
        ConfigLoader._validate_structure(final_raw, service_name)

        # 5. Populate Global Settings Manager
        settings = SettingsManager.load_from_dict(final_raw)
        logger.info(f"CorpStage configuration successfully initialized. Unified settings frozen and ready.")
        
        return settings

    @classmethod
    def _validate_structure(cls, config: Dict[str, Any], service_name: str) -> None:
        """
        Runs comprehensive checks on structural segments to maintain fail-fast guarantees.
        """
        # A. Common structural nodes
        required_keys = ["platform", "cloud", "security", "observability", "database"]
        for rk in required_keys:
            if rk not in config:
                raise YAMLValidationError(
                    f"Config integrity check failed: missing required root node '{rk}'."
                )

        # B. Platform Node Checks
        platform = config.get("platform", {})
        if not platform.get("name") or not platform.get("environment"):
            raise YAMLValidationError(
                "Config integrity check failed: platform attributes (name, environment) must be configured."
            )

        # C. Database safeguards
        db = config.get("database", {})
        primary_engine = db.get("primary_engine")
        if primary_engine and primary_engine not in db:
            raise YAMLValidationError(
                f"Config integrity check failed: database engine '{primary_engine}' is set as "
                f"primary, but engine details for '{primary_engine}' are not defined in the structure."
            )

        # D. Service Specific validation (Multi-service tailoring)
        if service_name == "AuthService":
            # Must have authentication properties
            auth = config.get("authentication", {})
            jwt = auth.get("jwt", {})
            if not jwt.get("algorithm") or not jwt.get("access_token_expiry_minutes"):
                raise YAMLValidationError(
                    "Service integrity boundary failure: AuthService requires a complete 'authentication.jwt' configuration block."
                )

        elif service_name == "AIService":
            # Must have AI properties configured
            ai = config.get("ai", {})
            if not ai.get("primary_provider") or "providers" not in ai:
                raise YAMLValidationError(
                    "Service integrity boundary failure: AIService requires a valid 'ai' and family provider configuration."
                )

        elif service_name == "IngestionService":
            # File ingestion details must exist
            ingestion = config.get("ingestion", {})
            if not ingestion.get("max_file_size_mb") or not ingestion.get("allowed_extensions"):
                raise YAMLValidationError(
                    "Service integrity boundary failure: IngestionService requires 'ingestion.max_file_size_mb' and validation types."
                )
