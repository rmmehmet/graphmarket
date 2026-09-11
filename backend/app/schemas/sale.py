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
