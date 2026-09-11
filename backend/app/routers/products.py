from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.product_service import (
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
def list_products_endpoint(
    category: str | None = None,
    search: str | None = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_products(db, current_user.team_id, category, search)


@router.post("/", response_model=ProductOut, status_code=201)
def create_product_endpoint(
    payload: ProductCreate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_product(db, current_user.team_id, payload.name, payload.category, payload.base_price)


@router.get("/{product_id}", response_model=ProductOut)
def get_product_endpoint(
    product_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_product(db, current_user.team_id, product_id)


@router.put("/{product_id}", response_model=ProductOut)
def update_product_endpoint(
    product_id: str,
    payload: ProductUpdate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_product(db, current_user.team_id, product_id, payload.model_dump())


@router.delete("/{product_id}", status_code=204)
def delete_product_endpoint(
    product_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_product(db, current_user.team_id, product_id)
