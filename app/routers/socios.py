from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_roles
from app.db.models.socio import Socio
from app.schemas.socios import SocioIn, SocioOut, DatosPersonales, SociosResponse, PaginationInfo
from typing import List
from datetime import date
import math

router = APIRouter(prefix="/socios", tags=["socios"])

@router.get("/", response_model=SociosResponse)
def listar_socios(
    user=Depends(require_roles("tesorero", "secretaria")),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros por página"),
    cedula: str = Query(None, description="Filtrar por cédula"),
    rol: str = Query(None, description="Filtrar por rol"),
    buscar: str = Query(None, description="Buscar por nombre o cédula"),
):
    """Listar socios con paginación y filtros"""
    query = db.query(Socio)
    
    # Aplicar filtros
    if cedula:
        query = query.filter(Socio.cedula == cedula)
    if rol:
        query = query.filter(Socio.rol == rol)
    if buscar:
        search_term = f"%{buscar}%"
        query = query.filter(
            (Socio.cedula.contains(buscar)) |
            (Socio.apellidos_nombres.contains(search_term))
        )
    
    # Contar total de registros
    total = query.count()
    
    # Calcular información de paginación
    total_paginas = math.ceil(total / limit) if total > 0 else 0
    pagina_actual = (skip // limit) + 1 if total > 0 else 0
    
    # Obtener registros paginados
    socios = query.offset(skip).limit(limit).all()
    
    # Crear respuesta paginada
    return SociosResponse(
        socios=[
            SocioOut(
                cedula=s.cedula,
                apellidos_nombres=s.apellidos_nombres,
                campus=s.campus,
                genero=s.genero,
                regimen=s.regimen,
                celular=s.celular,
                rol=s.rol,
                cargo=s.cargo,
                direccion=s.direccion,
                fecha_afiliacion=s.fecha_afiliacion,
                documento_pdf=s.documento_pdf,
                observaciones=s.observaciones,
                correo=s.correo,
                tipo_usuario=s.tipo_usuario,
            )
            for s in socios
        ],
        paginacion=PaginationInfo(
            pagina_actual=pagina_actual,
            total_paginas=total_paginas,
            total_socios=total,
            limite=limit,
            skip=skip
        )
    )

@router.get("/{cedula}", response_model=SocioOut)
def obtener_socio(
    cedula: str,
    user=Depends(require_roles("tesorero", "secretaria")),
    db: Session = Depends(get_db),
):
    """Obtener socio por cédula"""
    socio = db.get(Socio, cedula)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    
    return SocioOut(
        cedula=socio.cedula,
        apellidos_nombres=socio.apellidos_nombres,
        campus=socio.campus,
        genero=socio.genero,
        regimen=socio.regimen,
        celular=socio.celular,
        rol=socio.rol,
        cargo=socio.cargo,
        direccion=socio.direccion,
        fecha_afiliacion=socio.fecha_afiliacion,
        documento_pdf=socio.documento_pdf,
        observaciones=socio.observaciones,
        correo=socio.correo,
        tipo_usuario=socio.tipo_usuario,
    )

@router.post("/", response_model=SocioOut)
def crear_socio(
    socio: SocioIn,
    user=Depends(require_roles("tesorero", "secretaria")),
    db: Session = Depends(get_db),
):
    """Crear nuevo socio"""
    # Verificar que la cédula no exista
    if db.get(Socio, socio.cedula):
        raise HTTPException(status_code=400, detail="Ya existe un socio con esa cédula")
    
    db_socio = Socio(**socio.dict())
    db.add(db_socio)
    db.commit()
    db.refresh(db_socio)
    
    return SocioOut(
        cedula=db_socio.cedula,
        apellidos_nombres=db_socio.apellidos_nombres,
        campus=db_socio.campus,
        genero=db_socio.genero,
        regimen=db_socio.regimen,
        celular=db_socio.celular,
        rol=db_socio.rol,
        cargo=db_socio.cargo,
        direccion=db_socio.direccion,
        fecha_afiliacion=db_socio.fecha_afiliacion,
        documento_pdf=db_socio.documento_pdf,
        observaciones=db_socio.observaciones,
        correo=db_socio.correo,
        tipo_usuario=db_socio.tipo_usuario,
    )

@router.put("/{cedula}", response_model=SocioOut)
def actualizar_socio(
    cedula: str,
    socio: SocioIn,
    user=Depends(require_roles("tesorero")),  # solo tesorero edita
    db: Session = Depends(get_db),
):
    """Actualizar socio existente"""
    db_socio = db.get(Socio, cedula)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    
    # Actualizar campos
    for field, value in socio.dict(exclude_unset=True).items():
        if field != "cedula":  # No cambiar la cédula
            setattr(db_socio, field, value)
    
    db.commit()
    db.refresh(db_socio)
    
    return SocioOut(
        cedula=db_socio.cedula,
        apellidos_nombres=db_socio.apellidos_nombres,
        campus=db_socio.campus,
        genero=db_socio.genero,
        regimen=db_socio.regimen,
        celular=db_socio.celular,
        rol=db_socio.rol,
        cargo=db_socio.cargo,
        direccion=db_socio.direccion,
        fecha_afiliacion=db_socio.fecha_afiliacion,
        documento_pdf=db_socio.documento_pdf,
        observaciones=db_socio.observaciones,
        correo=db_socio.correo,
        tipo_usuario=db_socio.tipo_usuario,
    )