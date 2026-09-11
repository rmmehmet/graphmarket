import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict


class ReportPeriod(BaseModel):
    start: date
    end: date


class ReportGenerateRequest(BaseModel):
    type: str = "sales_summary"
    period: ReportPeriod
    channel_ids: list[uuid.UUID] = []


class ReportGenerateResponse(BaseModel):
    job_id: uuid.UUID


class ReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_id: uuid.UUID | None
    period_start: date
    period_end: date
    content: dict | None
