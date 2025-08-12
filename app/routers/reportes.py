from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.core.deps import get_db, require_roles
from app.db.models.socio import Socio
from app.db.models.aportes import AportesSocios
from app.db.models.comprobante import ComprobantePago
from app.schemas.reportes import (
    ReporteSociosResponse, 
    ReporteAportesResponse, 
    ReporteComprobantesResponse,
    ReporteSocio,
    ReporteAporte,
    ReporteComprobante,
    PaginationInfoReportes
)
from datetime import datetime, date
from typing import List, Dict, Any
import math

router = APIRouter(prefix="/reportes", tags=["reportes"])

@router.get("/socios", response_model=ReporteSociosResponse)
def reporte_socios(
    user=Depends(require_roles("tesorero", "secretaria")),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros por página"),
    campus: str = Query(None, description="Filtrar por campus"),
    rol: str = Query(None, description="Filtrar por rol"),
    buscar: str = Query(None, description="Buscar por nombre o cédula"),
):
    """Reporte de socios con paginación y filtros"""
    query = db.query(Socio)
    
    # Aplicar filtros
    if campus:
        query = query.filter(Socio.campus == campus)
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
    
    return ReporteSociosResponse(
        socios=[
            ReporteSocio(
                cedula=s.cedula,
                nombre=s.apellidos_nombres,
                campus=s.campus,
                rol=s.rol,
                tipo_usuario=s.tipo_usuario,
                fecha_afiliacion=s.fecha_afiliacion
            )
            for s in socios
        ],
        paginacion=PaginationInfoReportes(
            pagina_actual=pagina_actual,
            total_paginas=total_paginas,
            total_registros=total,
            limite=limit,
            skip=skip
        )
    )

@router.get("/aportes", response_model=ReporteAportesResponse)
def reporte_aportes(
    user=Depends(require_roles("tesorero", "secretaria")),
    db: Session = Depends(get_db),
    cedula: str = Query(None, description="Filtrar por cédula"),
    buscar: str = Query(None, description="Buscar por nombre o cédula"),
):
    """Reporte de aportes por socio"""
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
    
    aportes = query.all()
    
    return ReporteAportesResponse(
        aportes=[
            ReporteAporte(
                cedula=a.cedula,
                nombre=a.apellidos_y_nombres,
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
        ]
    )

@router.get("/comprobantes", response_model=ReporteComprobantesResponse)
def reporte_comprobantes(
    user=Depends(require_roles("tesorero", "secretaria")),
    db: Session = Depends(get_db),
    fecha_inicio: date = Query(None, description="Fecha de inicio"),
    fecha_fin: date = Query(None, description="Fecha de fin"),
    cedula: str = Query(None, description="Filtrar por cédula"),
):
    """Reporte de comprobantes de pago"""
    query = db.query(ComprobantePago)
    
    # Aplicar filtros
    if fecha_inicio:
        query = query.filter(ComprobantePago.fecha_pago >= fecha_inicio)
    if fecha_fin:
        query = query.filter(ComprobantePago.fecha_pago <= fecha_fin)
    if cedula:
        query = query.filter(ComprobantePago.cedula == cedula)
    
    comprobantes = query.all()
    
    return ReporteComprobantesResponse(
        comprobantes=[
            ReporteComprobante(
                id=c.id,
                cedula=c.cedula,
                fecha_pago=c.fecha_pago,
                total=float(c.total),
                ingreso=float(c.ingreso) if c.ingreso else 0,
                numero_comprobante=c.numero_comprobante,
                observaciones=c.observaciones
            )
            for c in comprobantes
        ]
    )
