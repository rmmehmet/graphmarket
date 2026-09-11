import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    category: str | None = None
    base_price: Decimal


class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    base_price: Decimal | None = None


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    category: str | None
    base_price: Decimal
