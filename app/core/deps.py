from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal

security = HTTPBearer(auto_error=True)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
        if payload.get("scope") != "access":
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"cedula": payload.get("sub"), "rol": payload.get("rol")}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")

def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
        if payload.get("scope") != "refresh":
            raise HTTPException(status_code=401, detail="Refresh inválido")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh inválido / expirado")

def require_roles(*roles: str):
    def checker(user=Depends(get_current_user)):
        if user["rol"] not in [r for r in roles]:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return user
    return checker
