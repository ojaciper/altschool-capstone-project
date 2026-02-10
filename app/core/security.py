from typing import Optional
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from jwt.exceptions import InvalidTokenError


password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password:str):
    return password_hash.hash(password)


def create_access_token(email:str, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {
        "sub":email,
        "exp":expire
    }
    encoded_jwt = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except InvalidTokenError:
        return None



