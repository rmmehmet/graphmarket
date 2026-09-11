from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.product import Product


def list_products(db: Session, team_id: str, category: str | None, search: str | None):
    stmt = select(Product).where(Product.team_id == team_id)
    if category:
        stmt = stmt.where(Product.category == category)
    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))
    return db.scalars(stmt.order_by(Product.created_at.desc())).all()


def create_product(
    db: Session, team_id: str, name: str, category: str | None, base_price: Decimal
) -> Product:
    product = Product(team_id=team_id, name=name, category=category, base_price=base_price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, team_id: str, product_id: str) -> Product:
    product = db.scalar(select(Product).where(Product.id == product_id, Product.team_id == team_id))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return product


def update_product(db: Session, team_id: str, product_id: str, data: dict) -> Product:
    product = get_product(db, team_id, product_id)
    for key, value in data.items():
        if value is not None:
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, team_id: str, product_id: str) -> None:
    product = get_product(db, team_id, product_id)
    db.delete(product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="product has sales records and cannot be deleted",
        )
