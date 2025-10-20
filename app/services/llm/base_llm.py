from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseLLmService(ABC):
    """
    Abstract Base Class for all LLM services (Ollama, OpenAI, Gemini, etc.)
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or "default-model"

    @abstractmethod
    def configure_llm(self, **kwargs) -> Dict[str, Any]:
        """Prepare configuration or payload before making an LLM call."""
        pass

    @abstractmethod
    def make_llm_call(self, prompt: str, **kwargs) -> str:
        """Perform the LLM API call and return the response."""
        pass

    def format_prompt(self, prompt: str) -> str:
        """Optional helper for consistent prompt formatting across LLMs."""
        return prompt.strip()

    def health_check(self) -> bool:
        """Optional: check if the LLM API/service is reachable."""
        return True
