from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sale import SalesRecord


def list_sales(
    db: Session,
    team_id: str,
    product_id: str | None,
    channel_id: str | None,
    date_from: datetime | None,
    date_to: datetime | None,
):
    stmt = select(SalesRecord).where(SalesRecord.team_id == team_id)
    if product_id:
        stmt = stmt.where(SalesRecord.product_id == product_id)
    if channel_id:
        stmt = stmt.where(SalesRecord.channel_id == channel_id)
    if date_from:
        stmt = stmt.where(SalesRecord.sold_at >= date_from)
    if date_to:
        stmt = stmt.where(SalesRecord.sold_at <= date_to)
    return db.scalars(stmt.order_by(SalesRecord.sold_at.desc())).all()


def create_sale(
    db: Session,
    team_id: str,
    product_id: UUID,
    channel_id: UUID,
    price: Decimal,
    quantity: int,
    sold_at: datetime | None,
) -> SalesRecord:
    sale = SalesRecord(
        team_id=team_id,
        product_id=product_id,
        channel_id=channel_id,
        price=price,
        quantity=quantity,
        sold_at=sold_at or datetime.now(timezone.utc),
        source="manual",
    )
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale
