from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_token, decode_token, hash_password, verify_password
from app.db.postgres import get_db
from app.models.user import Team, TeamMember, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


class AuthenticatedUser:
    def __init__(self, user_id: str, team_id: str):
        self.user_id = user_id
        self.team_id = team_id


def register_user(
    db: Session, email: str, password: str, business_name: str | None
) -> tuple[User, str]:
    existing = db.scalar(select(User).where(User.email == email))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already registered")

    user = User(email=email, password_hash=hash_password(password), business_name=business_name)
    db.add(user)
    db.flush()

    team = Team(name=business_name or email, owner_id=user.id)
    db.add(team)
    db.flush()

    db.add(TeamMember(team_id=team.id, user_id=user.id, role="owner"))
    db.commit()

    access_token = create_token(
        str(user.id), str(team.id), "access", timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    return user, access_token


def authenticate_user(db: Session, email: str, password: str) -> tuple[User, str]:
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    member = db.scalar(select(TeamMember).where(TeamMember.user_id == user.id))
    if member is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user has no team")
    return user, str(member.team_id)


def issue_tokens(user_id: str, team_id: str) -> tuple[str, str]:
    access_token = create_token(
        user_id, team_id, "access", timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    refresh_token = create_token(
        user_id, team_id, "refresh", timedelta(days=settings.jwt_refresh_token_expire_days)
    )
    return access_token, refresh_token


def refresh_access_token(refresh_token: str) -> str:
    try:
        payload = decode_token(refresh_token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type")
    return create_token(
        payload["sub"],
        payload["team_id"],
        "access",
        timedelta(minutes=settings.jwt_access_token_expire_minutes),
    )


def get_current_user(token: str | None = Depends(oauth2_scheme)) -> AuthenticatedUser:
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated")
    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type")
    return AuthenticatedUser(user_id=payload["sub"], team_id=payload["team_id"])
