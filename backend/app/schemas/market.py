import uuid

from pydantic import BaseModel


class MarketResearchRequest(BaseModel):
    category: str
    product_id: uuid.UUID | None = None


class MarketResearchJobOut(BaseModel):
    job_id: uuid.UUID


class MarketResearchResultOut(BaseModel):
    status: str
    result: dict | None = None


class TrendSignalOut(BaseModel):
    category: str
    direction: str
    strength: float
    observed_at: str
    source: str


class CompetitorOut(BaseModel):
    name: str
    platform: str
    anonymized: bool
