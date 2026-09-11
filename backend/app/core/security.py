from datetime import datetime, timedelta, timezone

from cryptography.fernet import Fernet
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

_fernet = Fernet(settings.secret_key.encode()) if settings.secret_key else None
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_secret(value: str) -> str:
    if _fernet is None:
        raise RuntimeError("SECRET_KEY not configured")
    return _fernet.encrypt(value.encode()).decode()


def decrypt_secret(token: str) -> str:
    if _fernet is None:
        raise RuntimeError("SECRET_KEY not configured")
    return _fernet.decrypt(token.encode()).decode()


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _pwd_context.verify(password, password_hash)


def create_token(subject: str, team_id: str, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "team_id": team_id,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError("invalid token") from exc
