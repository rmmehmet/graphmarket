import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SaleCreate(BaseModel):
    product_id: uuid.UUID
    channel_id: uuid.UUID
    price: Decimal
    quantity: int = 1
    sold_at: datetime | None = None


class SaleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    channel_id: uuid.UUID
    price: Decimal
    quantity: int
    source: str
    sold_at: datetime


class SalesImportResult(BaseModel):
    imported_count: int
    errors: list[str]


class AnalyticsSeriesItem(BaseModel):
    key: str
    label: str
    revenue: float
    quantity: int


class AnalyticsTotals(BaseModel):
    revenue: float
    quantity: int


class SalesAnalyticsResponse(BaseModel):
    group_by: str
    totals: AnalyticsTotals
    series: list[AnalyticsSeriesItem]
