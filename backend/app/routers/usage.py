from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.schemas.usage import UsageResponse
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.quota_service import get_usage_breakdown

router = APIRouter(prefix="/api/usage", tags=["usage"])


@router.get("/", response_model=UsageResponse)
def get_usage_endpoint(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_usage_breakdown(db, current_user.team_id)
