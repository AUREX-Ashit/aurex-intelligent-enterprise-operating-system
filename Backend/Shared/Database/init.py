"""
CorpStage Shared Database Framework - init.py

Delegates to __init__.py definitions to support multiple module import styles
across diverse consumer microservices (AuthService, IngestionService, TenantService, etc.)
"""

from corpstage.backend.shared.database.__init__ import *
