from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import date
from app.core.validators import validar_cedula_ec, normalize_cedula
from app.db.models.socio import TipoUsuario

class DatosPersonales(BaseModel):
    cedula: str
    nombrecompleto: str
    correo: Optional[EmailStr] = None
    celular: Optional[str] = None
    campus: Optional[str] = None
    genero: Optional[str] = None
    regimen: Optional[str] = None
    cargo: Optional[str] = None
    direccion: Optional[str] = None
    fecha_afiliacion: Optional[date] = None

class SocioIn(BaseModel):
    cedula: str
    apellidos_nombres: str
    campus: Optional[str] = None
    genero: Optional[str] = None
    regimen: Optional[str] = None
    celular: Optional[str] = None
    rol: Optional[str] = "socio"
    cargo: Optional[str] = None
    direccion: Optional[str] = None
    fecha_afiliacion: Optional[date] = None
    documento_pdf: Optional[str] = None
    observaciones: Optional[str] = None
    correo: Optional[EmailStr] = None
    tipo_usuario: Optional[TipoUsuario] = TipoUsuario.adherente

    @field_validator("cedula")
    @classmethod
    def _val_cedula(cls, v):
        v2 = normalize_cedula(v)
        if not validar_cedula_ec(v2):
            raise ValueError("Cédula ecuatoriana inválida")
        return v2

class SocioOut(BaseModel):
    cedula: str
    apellidos_nombres: Optional[str] = None
    campus: Optional[str] = None
    genero: Optional[str] = None
    regimen: Optional[str] = None
    celular: Optional[str] = None
    rol: Optional[str] = None
    cargo: Optional[str] = None
    direccion: Optional[str] = None
    fecha_afiliacion: Optional[date] = None
    documento_pdf: Optional[str] = None
    observaciones: Optional[str] = None
    correo: Optional[EmailStr] = None
    tipo_usuario: Optional[TipoUsuario] = None

class PaginationInfo(BaseModel):
    pagina_actual: int
    total_paginas: int
    total_socios: int
    limite: int
    skip: int

class SociosResponse(BaseModel):
    socios: List[SocioOut]
    paginacion: PaginationInfo

class SocioCreate(BaseModel):
    cedula: str
    apellidos_nombres: str
    campus: Optional[str] = None
    genero: Optional[str] = None
    regimen: Optional[str] = None
    celular: Optional[str] = None
    rol: Optional[str] = "socio"
    cargo: Optional[str] = None
    direccion: Optional[str] = None
    fecha_afiliacion: Optional[date] = None
    documento_pdf: Optional[str] = None
    observaciones: Optional[str] = None
    correo: Optional[EmailStr] = None
    tipo_usuario: Optional[TipoUsuario] = TipoUsuario.adherente
    password: Optional[str] = None   # si no se envía, ponemos una temporal

    @field_validator("cedula")
    @classmethod
    def _val_cedula(cls, v):
        v2 = normalize_cedula(v)
        if not validar_cedula_ec(v2):
            raise ValueError("Cédula ecuatoriana inválida")
        return v2

class SocioUpdate(BaseModel):
    apellidos_nombres: Optional[str] = None
    campus: Optional[str] = None
    genero: Optional[str] = None
    regimen: Optional[str] = None
    celular: Optional[str] = None
    rol: Optional[str] = None
    cargo: Optional[str] = None
    direccion: Optional[str] = None
    fecha_afiliacion: Optional[date] = None
    documento_pdf: Optional[str] = None
    observaciones: Optional[str] = None
    correo: Optional[EmailStr] = None
    tipo_usuario: Optional[TipoUsuario] = None
