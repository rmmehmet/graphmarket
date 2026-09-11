from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.schemas.settings import (
    ModelProfileOut,
    ModelProfileTestRequest,
    ModelProfileTestResponse,
    ModelProfileUpdate,
)
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.settings_service import get_model_profiles, test_model_profile, upsert_model_profile

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/model-profile", response_model=list[ModelProfileOut])
def get_model_profile_endpoint(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_model_profiles(db, current_user.team_id)


@router.put("/model-profile", response_model=ModelProfileOut)
def update_model_profile_endpoint(
    payload: ModelProfileUpdate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return upsert_model_profile(
        db, current_user.team_id, payload.node, payload.provider, payload.model_name, payload.api_key
    )


@router.post("/model-profile/test", response_model=ModelProfileTestResponse)
def test_model_profile_endpoint(
    payload: ModelProfileTestRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return test_model_profile(db, current_user.team_id, payload.node)
