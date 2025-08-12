# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
import uuid
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.schemas.auth import LoginIn, TokenOut, RefreshIn, LogoutIn
from app.schemas.auth_extra import ForgotPasswordIn, ForgotPasswordOut, ResetPasswordIn, ChangePasswordIn
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.deps import get_db, decode_refresh_token, get_current_user
from app.core.config import settings
from app.core.validators import normalize_cedula
from app.db.models.iniciosesion import InicioSesion
from app.db.models.socio import Socio
from app.db.models.refresh_token import RefreshToken
from app.db.models.password_reset import PasswordResetToken

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    ced = normalize_cedula(data.cedula)
    
    # Buscar usuario en la tabla iniciosesion
    user = db.get(InicioSesion, ced)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Verificar contraseña (comparar directamente ya que está en texto plano en la BD)
    if user.contrasena != data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Obtener rol del usuario desde la tabla socios
    socio = db.query(Socio).filter(Socio.cedula == ced).first()
    rol = socio.rol if socio and socio.rol else "socio"
    
    # Si no tiene rol específico, asignar según el tipo de usuario
    if not rol and socio:
        if socio.tipo_usuario == "fundador":
            rol = "presidente"
        elif socio.tipo_usuario == "adherente":
            rol = "socio"
        else:
            rol = "socio"

    access = create_access_token(user.cedula, rol)
    refresh, jti = create_refresh_token(user.cedula, rol)
    exp = datetime.now(timezone.utc) + timedelta(days=7)
    
    # Crear refresh token en la base de datos
    db.add(RefreshToken(jti=jti, cedula=user.cedula, expires_at=exp))
    db.commit()
    
    return {"access_token": access, "refresh_token": refresh, "rol": rol}

@router.post("/refresh", response_model=TokenOut)
def refresh(body: RefreshIn, db: Session = Depends(get_db)):
    payload = decode_refresh_token(body.refresh_token)
    jti = payload.get("jti")
    cedula = payload.get("sub")
    rol = payload.get("rol")

    rt = db.get(RefreshToken, jti)
    if not rt or rt.is_revoked:
        raise HTTPException(status_code=401, detail="Refresh inválido")
    if rt.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh expirado")

    rt.is_revoked = True
    access = create_access_token(cedula, rol)
    new_refresh, new_jti = create_refresh_token(cedula, rol)
    exp = datetime.now(timezone.utc) + timedelta(days=7)
    db.add(RefreshToken(jti=new_jti, cedula=cedula, expires_at=exp))
    db.commit()

    return {"access_token": access, "refresh_token": new_refresh, "rol": rol}

@router.post("/logout")
def logout(body: LogoutIn, db: Session = Depends(get_db)):
    payload = decode_refresh_token(body.refresh_token)
    jti = payload.get("jti")
    rt = db.get(RefreshToken, jti)
    if rt and not rt.is_revoked:
        rt.is_revoked = True
        db.commit()
    return {"detail": "Sesión cerrada"}

@router.post("/password/forgot", response_model=ForgotPasswordOut)
def forgot_password(body: ForgotPasswordIn, db: Session = Depends(get_db)):
    if not body.cedula and not body.correo:
        raise HTTPException(422, "Envíe cédula o correo")

    user = None
    if body.cedula:
        user = db.get(Usuario, normalize_cedula(body.cedula))
    else:
        # Buscar por correo en la tabla socios
        socio = db.query(Socio).filter(Socio.correo == body.correo).first()
        if socio:
            user = db.get(Usuario, socio.cedula)

    if not user:
        return ForgotPasswordOut(message="Si el usuario existe, recibirá instrucciones")

    jti = uuid.uuid4().hex
    exp = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {"sub": user.cedula, "type": "reset", "jti": jti, "exp": exp}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)

    db.add(PasswordResetToken(jti=jti, cedula=user.cedula, expires_at=exp))
    db.commit()

    return ForgotPasswordOut(message="Token de reseteo generado", reset_token=token)


@router.post("/password/reset")
def reset_password(body: ResetPasswordIn, db: Session = Depends(get_db)):
    try:
        data = jwt.decode(body.token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    except JWTError:
        raise HTTPException(400, "Token inválido")
    if data.get("type") != "reset":
        raise HTTPException(400, "Token inválido")

    jti = data.get("jti")
    ced = data.get("sub")

    rec = db.get(PasswordResetToken, jti)
    if not rec or rec.cedula != ced or rec.used or rec.expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, "Token expirado o inválido")

    user = db.get(Usuario, ced)
    if not user:
        raise HTTPException(404, "Usuario no existe")

    # Actualizar contraseña en texto plano (como está en la BD original)
    user.contrasena = body.new_password
    rec.used = True
    db.commit()
    return {"message": "Contraseña actualizada"}

@router.post("/password/change")
def change_password(
    body: ChangePasswordIn,
    current=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.get(Usuario, current.cedula)
    if not user or user.contrasena != body.old_password:
        raise HTTPException(400, "Contraseña actual incorrecta")
    if body.old_password == body.new_password:
        raise HTTPException(400, "La nueva contraseña debe ser distinta")

    user.contrasena = body.new_password
    db.commit()
    return {"message": "Contraseña cambiada"}
