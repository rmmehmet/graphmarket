from pydantic import BaseModel


class UsageBreakdownItem(BaseModel):
    job_type: str
    used: int
    limit: int | None
    remaining: int | None


class UsageResponse(BaseModel):
    period: str
    plan: str
    breakdown: list[UsageBreakdownItem]
