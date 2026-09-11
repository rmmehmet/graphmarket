from anthropic import Anthropic

from app.agents.providers.base import ModelProvider


class AnthropicProvider(ModelProvider):
    def _client(self) -> Anthropic:
        if not self.api_key:
            raise ValueError("Anthropic API key not configured")
        return Anthropic(api_key=self.api_key)

    def test_connection(self) -> None:
        client = self._client()
        client.messages.create(
            model=self.model_name or "claude-3-5-haiku-20241022",
            max_tokens=1,
            messages=[{"role": "user", "content": "ping"}],
        )

    def complete(self, prompt: str) -> str:
        client = self._client()
        response = client.messages.create(
            model=self.model_name or "claude-3-5-haiku-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
