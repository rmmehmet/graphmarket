import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Citation(BaseModel):
    type: str
    id: str | None = None
    label: str


class AskRequest(BaseModel):
    question: str
    context_product_id: uuid.UUID | None = None


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]


class AskDeepRequest(BaseModel):
    question: str


class AskDeepResponse(BaseModel):
    job_id: uuid.UUID


class AgentHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question: str
    answer: str | None
    citations: list[Citation] | None
    mode: str
    created_at: datetime
