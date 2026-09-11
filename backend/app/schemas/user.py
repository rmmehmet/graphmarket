import uuid

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    business_name: str | None = None


class RegisterResponse(BaseModel):
    user_id: uuid.UUID
    access_token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str


class UserProfile(BaseModel):
    id: uuid.UUID
    email: EmailStr
    business_name: str | None
