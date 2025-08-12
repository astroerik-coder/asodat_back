from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.deps import get_db, require_roles
from app.db.models.socio import Socio
from app.db.models.aportes import AportesSocios
from app.db.models.comprobante import ComprobantePago
from app.schemas.aportes import AporteIn, AporteOut, AportesResponse, PaginationInfoAportes
from datetime import datetime, date
from typing import List, Dict, Any
import math

router = APIRouter(prefix="/aportes", tags=["aportes"])

@router.get("/", response_model=AportesResponse)
def listar_aportes(
    user=Depends(require_roles("tesorero", "secretaria")),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros por página"),
    cedula: str = Query(None, description="Filtrar por cédula"),
    buscar: str = Query(None, description="Buscar por nombre o cédula"),
):
    """Listar aportes con paginación y filtros"""
    query = db.query(AportesSocios)
    
    # Aplicar filtros
    if cedula:
        query = query.filter(AportesSocios.cedula == cedula)
    if buscar:
        search_term = f"%{buscar}%"
        query = query.filter(
            (AportesSocios.cedula.contains(buscar)) |
            (AportesSocios.apellidos_y_nombres.contains(search_term))
        )
    
    # Contar total de registros
    total = query.count()
    
    # Calcular información de paginación
    total_paginas = math.ceil(total / limit) if total > 0 else 0
    pagina_actual = (skip // limit) + 1 if total > 0 else 0
    
    # Obtener registros paginados
    aportes = query.offset(skip).limit(limit).all()
    
    # Crear respuesta paginada
    return AportesResponse(
        aportes=[
            AporteOut(
                cedula=a.cedula,
                apellidos_y_nombres=a.apellidos_y_nombres,
                nuevos_ingresos=float(a.nuevos_ingresos) if a.nuevos_ingresos else 0,
                dic_24=float(a.dic_24) if a.dic_24 else 0,
                ene_25=float(a.ene_25) if a.ene_25 else 0,
                feb_25=float(a.feb_25) if a.feb_25 else 0,
                mar_25=float(a.mar_25) if a.mar_25 else 0,
                abr_25=float(a.abr_25) if a.abr_25 else 0,
                may_25=float(a.may_25) if a.may_25 else 0,
                jun_25=float(a.jun_25) if a.jun_25 else 0,
                jul_25=float(a.jul_25) if a.jul_25 else 0,
                ago_25=float(a.ago_25) if a.ago_25 else 0,
                sept_25=float(a.sept_25) if a.sept_25 else 0,
                oct_25=float(a.oct_25) if a.oct_25 else 0,
                nov_25=float(a.nov_25) if a.nov_25 else 0,
                dic_25=float(a.dic_25) if a.dic_25 else 0,
            )
            for a in aportes
        ],
        paginacion=PaginationInfoAportes(
            pagina_actual=pagina_actual,
            total_paginas=total_paginas,
            total_aportes=total,
            limite=limit,
            skip=skip
        )
    )

@router.post("/", response_model=AporteOut)
def crear_aporte(
    aporte: AporteIn,
    user=Depends(require_roles("tesorero")),  # solo tesorero registra
    db: Session = Depends(get_db),
):
    """Crear nuevo registro de aportes"""
    # Verificar que el socio existe
    socio = db.get(Socio, aporte.cedula)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    
    # Crear o actualizar aporte
    db_aporte = AportesSocios(
        cedula=aporte.cedula,
        apellidos_y_nombres=socio.apellidos_nombres,
        nuevos_ingresos=aporte.nuevos_ingresos,
        dic_24=aporte.dic_24,
        ene_25=aporte.ene_25,
        feb_25=aporte.feb_25,
        mar_25=aporte.mar_25,
        abr_25=aporte.abr_25,
        may_25=aporte.may_25,
        jun_25=aporte.jun_25,
        jul_25=aporte.jul_25,
        ago_25=aporte.ago_25,
        sept_25=aporte.sept_25,
        oct_25=aporte.oct_25,
        nov_25=aporte.nov_25,
        dic_25=aporte.dic_25,
    )
    
    db.add(db_aporte)
    db.commit()
    db.refresh(db_aporte)
    
    return AporteOut(
        cedula=db_aporte.cedula,
        apellidos_y_nombres=db_aporte.apellidos_y_nombres,
        nuevos_ingresos=float(db_aporte.nuevos_ingresos) if db_aporte.nuevos_ingresos else 0,
        dic_24=float(db_aporte.dic_24) if db_aporte.dic_24 else 0,
        ene_25=float(db_aporte.ene_25) if db_aporte.ene_25 else 0,
        feb_25=float(db_aporte.feb_25) if db_aporte.feb_25 else 0,
        mar_25=float(db_aporte.mar_25) if db_aporte.mar_25 else 0,
        abr_25=float(db_aporte.abr_25) if db_aporte.abr_25 else 0,
        may_25=float(db_aporte.may_25) if db_aporte.may_25 else 0,
        jun_25=float(db_aporte.jun_25) if db_aporte.jun_25 else 0,
        jul_25=float(db_aporte.jul_25) if db_aporte.jul_25 else 0,
        ago_25=float(db_aporte.ago_25) if db_aporte.ago_25 else 0,
        sept_25=float(db_aporte.sept_25) if db_aporte.sept_25 else 0,
        oct_25=float(db_aporte.oct_25) if db_aporte.oct_25 else 0,
        nov_25=float(db_aporte.nov_25) if db_aporte.nov_25 else 0,
        dic_25=float(db_aporte.dic_25) if db_aporte.dic_25 else 0,
    )

@router.put("/{cedula}", response_model=AporteOut)
def actualizar_aporte(
    cedula: str,
    aporte: AporteIn,
    user=Depends(require_roles("tesorero")),  # solo tesorero edita
    db: Session = Depends(get_db),
):
    """Actualizar aporte existente"""
    db_aporte = db.get(AportesSocios, cedula)
    if not db_aporte:
        raise HTTPException(status_code=404, detail="Aporte no encontrado")
    
    # Actualizar campos
    for field, value in aporte.dict(exclude_unset=True).items():
        if field != "cedula":  # No cambiar la cédula
            setattr(db_aporte, field, value)
    
    db.commit()
    db.refresh(db_aporte)
    
    return AporteOut(
        cedula=db_aporte.cedula,
        apellidos_y_nombres=db_aporte.apellidos_y_nombres,
        nuevos_ingresos=float(db_aporte.nuevos_ingresos) if db_aporte.nuevos_ingresos else 0,
        dic_24=float(db_aporte.dic_24) if db_aporte.dic_24 else 0,
        ene_25=float(db_aporte.ene_25) if db_aporte.ene_25 else 0,
        feb_25=float(db_aporte.feb_25) if db_aporte.feb_25 else 0,
        mar_25=float(db_aporte.mar_25) if db_aporte.mar_25 else 0,
        abr_25=float(db_aporte.abr_25) if db_aporte.abr_25 else 0,
        may_25=float(db_aporte.may_25) if db_aporte.may_25 else 0,
        jun_25=float(db_aporte.jun_25) if db_aporte.jun_25 else 0,
        jul_25=float(db_aporte.jul_25) if db_aporte.jul_25 else 0,
        ago_25=float(db_aporte.ago_25) if db_aporte.ago_25 else 0,
        sept_25=float(db_aporte.sept_25) if db_aporte.sept_25 else 0,
        oct_25=float(db_aporte.oct_25) if db_aporte.oct_25 else 0,
        nov_25=float(db_aporte.nov_25) if db_aporte.nov_25 else 0,
        dic_25=float(db_aporte.dic_25) if db_aporte.dic_25 else 0,
    )
