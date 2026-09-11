from app.agents.providers.anthropic_provider import AnthropicProvider
from app.agents.providers.base import ModelProvider
from app.agents.providers.claude_subscription_provider import ClaudeSubscriptionProvider
from app.agents.providers.huggingface_provider import HuggingFaceProvider
from app.agents.providers.ollama_provider import OllamaProvider

_PROVIDER_CLASSES: dict[str, type[ModelProvider]] = {
    "ollama": OllamaProvider,
    "huggingface": HuggingFaceProvider,
    "anthropic_api": AnthropicProvider,
    "claude_subscription": ClaudeSubscriptionProvider,
}


def get_provider(provider_name: str, model_name: str | None, api_key: str | None) -> ModelProvider:
    try:
        provider_cls = _PROVIDER_CLASSES[provider_name]
    except KeyError:
        raise ValueError(f"unknown provider: {provider_name}")
    return provider_cls(model_name=model_name, api_key=api_key)
