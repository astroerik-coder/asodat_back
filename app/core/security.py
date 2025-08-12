from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from uuid import uuid4
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def _create_token(claims: dict, minutes: int | None = None, days: int | None = None) -> str:
    to_encode = claims.copy()
    now = datetime.now(timezone.utc)
    if minutes is not None:
        exp = now + timedelta(minutes=minutes)
    else:
        exp = now + timedelta(days=days or 1)
    to_encode.update({"exp": exp, "iat": now})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_alg)

def create_access_token(sub: str, rol: str) -> str:
    return _create_token({"sub": sub, "scope": "access", "rol": rol},
                         minutes=settings.access_token_expire_minutes)

def create_refresh_token(sub: str, rol: str, jti: str | None = None) -> tuple[str, str]:
    jti = jti or uuid4().hex
    token = _create_token({"sub": sub, "scope": "refresh", "rol": rol, "jti": jti},
                          days=settings.refresh_token_expire_days)
    return token, jti
