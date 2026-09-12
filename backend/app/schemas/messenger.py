import uuid

from pydantic import BaseModel


class ConnectResponse(BaseModel):
    redirect_url: str


class ImportExportResponse(BaseModel):
    job_id: uuid.UUID
    message_count: int


class SyncResponse(BaseModel):
    job_id: uuid.UUID


class ConversationOut(BaseModel):
    customer: str
    product: str | None
    sentiment: str | None
    mentioned_at: str


class ConversationDetailOut(BaseModel):
    customer: str
    product: str | None
    sentiment: str | None
    mentioned_at: str
    messages: list[str]
