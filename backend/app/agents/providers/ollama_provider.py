import httpx

from app.agents.providers.base import ModelProvider
from app.core.config import settings


class OllamaProvider(ModelProvider):
    def test_connection(self) -> None:
        response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=5)
        response.raise_for_status()

    def complete(self, prompt: str) -> str:
        response = httpx.post(
            f"{settings.ollama_base_url}/api/generate",
            json={"model": self.model_name or "llama3.2", "prompt": prompt, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["response"]
