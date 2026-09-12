import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: str
    status: str
    progress: int
    result_ref: str | None
    error_message: str | None


class JobSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: str
    status: str
    progress: int
    input_payload: dict | None
    result_ref: str | None
    error_message: str | None
    created_at: datetime
