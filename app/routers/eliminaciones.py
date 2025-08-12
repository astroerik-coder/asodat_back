from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_roles
from app.db.models.socio import Socio
from app.db.models.eliminaciones import HistorialEliminacion
from app.schemas.eliminaciones import EliminacionIn, EliminacionOut, EliminacionesResponse, PaginationInfoEliminaciones
from datetime import date
import math

router = APIRouter(prefix="/eliminaciones", tags=["eliminaciones"])

@router.get("/", response_model=EliminacionesResponse)
def listar_eliminaciones(
    user=Depends(require_roles("tesorero", "secretaria")),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros por página"),
    cedula: str = Query(None, description="Filtrar por cédula"),
    buscar: str = Query(None, description="Buscar por nombre o cédula"),
):
    """Listar eliminaciones con paginación y filtros"""
    query = db.query(HistorialEliminacion)
    
    # Aplicar filtros
    if cedula:
        query = query.filter(HistorialEliminacion.cedula == cedula)
    if buscar:
        search_term = f"%{buscar}%"
        query = query.filter(
            (HistorialEliminacion.cedula.contains(buscar)) |
            (HistorialEliminacion.nombre_completo.contains(search_term))
        )
    
    # Contar total de registros
    total = query.count()
    
    # Calcular información de paginación
    total_paginas = math.ceil(total / limit) if total > 0 else 0
    pagina_actual = (skip // limit) + 1 if total > 0 else 0
    
    # Obtener registros paginados
    eliminaciones = query.offset(skip).limit(limit).all()
    
    # Crear respuesta paginada
    return EliminacionesResponse(
        eliminaciones=[
            EliminacionOut(
                id=elim.id,
                cedula=elim.cedula,
                nombre_completo=elim.nombre_completo,
                fecha_afiliacion=elim.fecha_afiliacion,
                motivo=elim.motivo,
                fecha_eliminacion=elim.fecha_eliminacion,
            )
            for elim in eliminaciones
        ],
        paginacion=PaginationInfoEliminaciones(
            pagina_actual=pagina_actual,
            total_paginas=total_paginas,
            total_eliminaciones=total,
            limite=limit,
            skip=skip
        )
    )

@router.post("/", response_model=EliminacionOut)
def crear_eliminacion(
    eliminacion: EliminacionIn,
    user=Depends(require_roles("tesorero", "secretaria")),   # tesorero y secretaria pueden eliminar
    db: Session = Depends(get_db),
):
    """Crear registro de eliminación de socio"""
    # Verificar que el socio existe
    socio = db.get(Socio, eliminacion.cedula)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    
    # Crear registro de eliminación
    elim = HistorialEliminacion(
        cedula=eliminacion.cedula,
        nombre_completo=socio.apellidos_nombres or "Sin nombre",
        fecha_afiliacion=socio.fecha_afiliacion,
        motivo=eliminacion.motivo,
    )
    
    db.add(elim)
    db.commit()
    db.refresh(elim)
    
    return EliminacionOut(
        id=elim.id,
        cedula=elim.cedula,
        nombre_completo=elim.nombre_completo,
        fecha_afiliacion=elim.fecha_afiliacion,
        motivo=elim.motivo,
        fecha_eliminacion=elim.fecha_eliminacion,
    )
