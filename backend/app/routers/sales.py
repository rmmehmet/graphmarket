from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.schemas.sale import SaleCreate, SaleOut
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.sales_service import create_sale, list_sales

router = APIRouter(prefix="/api/sales", tags=["sales"])


@router.get("/", response_model=list[SaleOut])
def list_sales_endpoint(
    product_id: str | None = None,
    channel_id: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_sales(db, current_user.team_id, product_id, channel_id, date_from, date_to)


@router.post("/", response_model=SaleOut, status_code=201)
def create_sale_endpoint(
    payload: SaleCreate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_sale(
        db,
        current_user.team_id,
        payload.product_id,
        payload.channel_id,
        payload.price,
        payload.quantity,
        payload.sold_at,
    )
