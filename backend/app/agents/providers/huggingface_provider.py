import httpx

from app.agents.providers.base import ModelProvider

_BASE_URL = "https://api-inference.huggingface.co/models"


class HuggingFaceProvider(ModelProvider):
    def test_connection(self) -> None:
        if not self.api_key:
            raise ValueError("Hugging Face API key not configured")
        model = self.model_name or "gpt2"
        response = httpx.get(
            f"{_BASE_URL}/{model}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=10,
        )
        if response.status_code >= 400:
            raise RuntimeError(f"Hugging Face API error: {response.status_code}")

    def complete(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("Hugging Face API key not configured")
        model = self.model_name or "gpt2"
        response = httpx.post(
            f"{_BASE_URL}/{model}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"inputs": prompt},
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data[0]["generated_text"] if isinstance(data, list) else str(data)
