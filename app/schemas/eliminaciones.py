from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class EliminacionIn(BaseModel):
    cedula: str
    motivo: str

class EliminacionOut(BaseModel):
    id: int
    cedula: str
    nombre_completo: str
    fecha_afiliacion: Optional[date] = None
    motivo: str
    fecha_eliminacion: datetime

class PaginationInfoEliminaciones(BaseModel):
    pagina_actual: int
    total_paginas: int
    total_eliminaciones: int
    limite: int
    skip: int

class EliminacionesResponse(BaseModel):
    eliminaciones: List[EliminacionOut]
    paginacion: PaginationInfoEliminaciones
