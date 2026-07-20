"""
CorpStage Shared Configuration Framework - init.py

Delegates to __init__.py definitions to support multiple module import styles
across diverse consumer microservices (AuthService, IngestionService, TenantService, etc.)
"""

from corpstage.backend.shared.config.__init__ import *
