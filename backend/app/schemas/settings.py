from typing import Literal

from pydantic import BaseModel

NodeName = Literal["planner", "extraction", "synthesis", "verification"]
ProviderName = Literal["ollama", "huggingface", "anthropic_api", "claude_subscription"]


class ModelProfileOut(BaseModel):
    node: NodeName
    provider: ProviderName
    model_name: str | None
    has_api_key: bool


class ModelProfileUpdate(BaseModel):
    node: NodeName
    provider: ProviderName
    model_name: str | None = None
    api_key: str | None = None


class ModelProfileTestRequest(BaseModel):
    node: NodeName


class ModelProfileTestResponse(BaseModel):
    ok: bool
    latency_ms: int
    error: str | None = None
