import csv
import io
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.channel import Channel
from app.models.product import Product
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


def import_sales_from_csv(db: Session, team_id: str, file_bytes: bytes) -> tuple[int, list[str]]:
    products = {p.name: p for p in db.scalars(select(Product).where(Product.team_id == team_id))}
    channels = {c.name: c for c in db.scalars(select(Channel).where(Channel.team_id == team_id))}

    reader = csv.DictReader(io.StringIO(file_bytes.decode("utf-8-sig")))
    imported = 0
    errors: list[str] = []

    for line_number, row in enumerate(reader, start=2):
        try:
            product = products[row["product_name"]]
        except KeyError:
            errors.append(f"satır {line_number}: ürün bulunamadı '{row.get('product_name')}'")
            continue
        try:
            channel = channels[row["channel_name"]]
        except KeyError:
            errors.append(f"satır {line_number}: kanal bulunamadı '{row.get('channel_name')}'")
            continue
        try:
            price = Decimal(row["price"])
        except (InvalidOperation, KeyError):
            errors.append(f"satır {line_number}: geçersiz fiyat '{row.get('price')}'")
            continue

        sold_at = None
        if row.get("sold_at"):
            try:
                sold_at = datetime.fromisoformat(row["sold_at"])
            except ValueError:
                errors.append(f"satır {line_number}: geçersiz tarih '{row['sold_at']}'")
                continue

        sale = SalesRecord(
            team_id=team_id,
            product_id=product.id,
            channel_id=channel.id,
            price=price,
            quantity=int(row.get("quantity") or 1),
            sold_at=sold_at or datetime.now(timezone.utc),
            source="import",
        )
        db.add(sale)
        imported += 1

    db.commit()
    return imported, errors


def get_sales_analytics(db: Session, team_id: str, group_by: str) -> dict:
    revenue_expr = func.sum(SalesRecord.price * SalesRecord.quantity)
    quantity_expr = func.sum(SalesRecord.quantity)

    series: list[dict] = []
    if group_by == "product":
        stmt = (
            select(Product.id, Product.name, revenue_expr, quantity_expr)
            .join(Product, Product.id == SalesRecord.product_id)
            .where(SalesRecord.team_id == team_id)
            .group_by(Product.id, Product.name)
            .order_by(Product.name)
        )
        for entity_id, name, revenue, quantity in db.execute(stmt).all():
            series.append(
                {"key": str(entity_id), "label": name, "revenue": float(revenue or 0), "quantity": int(quantity or 0)}
            )
    elif group_by == "channel":
        stmt = (
            select(Channel.id, Channel.name, revenue_expr, quantity_expr)
            .join(Channel, Channel.id == SalesRecord.channel_id)
            .where(SalesRecord.team_id == team_id)
            .group_by(Channel.id, Channel.name)
            .order_by(Channel.name)
        )
        for entity_id, name, revenue, quantity in db.execute(stmt).all():
            series.append(
                {"key": str(entity_id), "label": name, "revenue": float(revenue or 0), "quantity": int(quantity or 0)}
            )
    else:
        week_col = func.date_trunc("week", SalesRecord.sold_at).label("week")
        stmt = (
            select(week_col, revenue_expr, quantity_expr)
            .where(SalesRecord.team_id == team_id)
            .group_by(week_col)
            .order_by(week_col)
        )
        for week, revenue, quantity in db.execute(stmt).all():
            label = week.date().isoformat()
            series.append(
                {"key": label, "label": label, "revenue": float(revenue or 0), "quantity": int(quantity or 0)}
            )

    totals_stmt = select(
        func.coalesce(revenue_expr, 0), func.coalesce(quantity_expr, 0)
    ).where(SalesRecord.team_id == team_id)
    total_revenue, total_quantity = db.execute(totals_stmt).one()

    return {
        "group_by": group_by,
        "totals": {"revenue": float(total_revenue), "quantity": int(total_quantity)},
        "series": series,
    }
