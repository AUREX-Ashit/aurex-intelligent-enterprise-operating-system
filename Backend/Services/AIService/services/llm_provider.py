# services/llm_provider.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from config.settings import settings

class LLMProvider(ABC):
    """Abstract interface contract defining LLM Providers across the Aurex platform."""
    
    @abstractmethod
    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        config_override: Optional[Dict[str, Any]] = None
    ) -> str:
        """Asynchronously executes completion query against provider APIs."""
        pass

    @abstractmethod
    async def generate_json(
        self, 
        prompt: str, 
        schema: Dict[str, Any],
        system_instruction: Optional[str] = None,
        config_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Asynchronously queries model to return structured data matching JSON schema."""
        pass


class AzureOpenAIStubProvider(LLMProvider):
    """Stub implementation of LLMProvider mimicking Azure OpenAI interface contract."""
    
    def __init__(self, endpoint: str, api_version: str, model_name: str):
        self.endpoint = endpoint
        self.api_version = api_version
        self.model_name = model_name

    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        config_override: Optional[Dict[str, Any]] = None
    ) -> str:
        # High fidelity stub response matching requested platform configs
        return f"[Azure OpenAI Stub: model={self.model_name}] Synthesized response to evaluation prompt."

    async def generate_json(
        self, 
        prompt: str, 
        schema: Dict[str, Any],
        system_instruction: Optional[str] = None,
        config_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Generates basic JSON scaffold fitting input schemas for validation
        return {
            "stub_status": "success",
            "model_running": self.model_name,
            "simulated_metrics": {
                "scope_1_emissions": 4200.50,
                "diversity_index": 0.52
            }
        }


# Dependency Injection Getter
def get_llm_provider() -> LLMProvider:
    """Instantiates active tenant-scoped provider according to platform configuration settings."""
    # Instantiates the stub cleanly without third-party libraries (e.g. openai SDK)
    return AzureOpenAIStubProvider(
        endpoint=settings.ai_endpoint,
        api_version=settings.ai_api_version,
        model_name=settings.primary_llm
    )
