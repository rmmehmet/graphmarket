from abc import ABC, abstractmethod


class ModelProvider(ABC):
    def __init__(self, model_name: str | None = None, api_key: str | None = None):
        self.model_name = model_name
        self.api_key = api_key

    @abstractmethod
    def test_connection(self) -> None:
        """Raise an exception if the provider is unreachable or misconfigured."""

    @abstractmethod
    def complete(self, prompt: str) -> str:
        ...
