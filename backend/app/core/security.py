from cryptography.fernet import Fernet

from app.core.config import settings

_fernet = Fernet(settings.secret_key.encode()) if settings.secret_key else None


def encrypt_secret(value: str) -> str:
    if _fernet is None:
        raise RuntimeError("SECRET_KEY not configured")
    return _fernet.encrypt(value.encode()).decode()


def decrypt_secret(token: str) -> str:
    if _fernet is None:
        raise RuntimeError("SECRET_KEY not configured")
    return _fernet.decrypt(token.encode()).decode()
