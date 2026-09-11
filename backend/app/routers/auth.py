from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.models.user import User
from app.schemas.user import (
    AccessTokenResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserProfile,
)
from app.services.auth_service import (
    AuthenticatedUser,
    authenticate_user,
    get_current_user,
    issue_tokens,
    refresh_access_token,
    register_user,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user, access_token = register_user(db, payload.email, payload.password, payload.business_name)
    return RegisterResponse(user_id=user.id, access_token=access_token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user, team_id = authenticate_user(db, payload.email, payload.password)
    access_token, refresh_token = issue_tokens(str(user.id), team_id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(payload: RefreshRequest):
    access_token = refresh_access_token(payload.refresh_token)
    return AccessTokenResponse(access_token=access_token)


@router.get("/me", response_model=UserProfile)
def me(current_user: AuthenticatedUser = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == current_user.user_id))
    return UserProfile(id=user.id, email=user.email, business_name=user.business_name)
