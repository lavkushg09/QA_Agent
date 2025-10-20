import os
import requests
from dotenv import load_dotenv
from .base_llm import BaseLLmService
load_dotenv()


class OllamaLLm(BaseLLmService):
    def __init__(self, ollama_url: str = None):
        super().__init__()
        self.ollama_url = ollama_url or os.getenv(
            "O_LLAMA_URL", "http://localhost:11434/api/generate"
        )

    def configure_llm(self, model_name: str = "llama3", stream: bool = False) -> dict:
        """Configure LLM parameters."""
        return {
            "model": model_name,
            "stream": stream,
        }

    def make_llm_call(self, prompt: str, model_name: str = "llama3") -> str:
        """Make a call to the Ollama local server."""
        payload = self.configure_llm(model_name)
        payload["prompt"] = prompt.strip()
        try:
            print(f"{self.ollama_url} xxxxx")
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama API call failed: {e}")
