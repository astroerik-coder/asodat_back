from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import List, Optional

MESES_VALIDOS = [
    "dic_24","ene_25","feb_25","mar_25","abr_25","may_25",
    "jun_25","jul_25","ago_25","sept_25","oct_25","nov_25","dic_25"
]

class AporteIn(BaseModel):
    cedula: str = Field(min_length=8, max_length=20)
    apellidos_y_nombres: Optional[str] = None
    nuevos_ingresos: Optional[float] = 0.0
    dic_24: Optional[float] = 0.0
    ene_25: Optional[float] = 0.0
    feb_25: Optional[float] = 0.0
    mar_25: Optional[float] = 0.0
    abr_25: Optional[float] = 0.0
    may_25: Optional[float] = 0.0
    jun_25: Optional[float] = 0.0
    jul_25: Optional[float] = 0.0
    ago_25: Optional[float] = 0.0
    sept_25: Optional[float] = 0.0
    oct_25: Optional[float] = 0.0
    nov_25: Optional[float] = 0.0
    dic_25: Optional[float] = 0.0

class AporteOut(BaseModel):
    cedula: str
    apellidos_y_nombres: Optional[str] = None
    nuevos_ingresos: float = 0.0
    dic_24: float = 0.0
    ene_25: float = 0.0
    feb_25: float = 0.0
    mar_25: float = 0.0
    abr_25: float = 0.0
    may_25: float = 0.0
    jun_25: float = 0.0
    jul_25: float = 0.0
    ago_25: float = 0.0
    sept_25: float = 0.0
    oct_25: float = 0.0
    nov_25: float = 0.0
    dic_25: float = 0.0

class AportesQuery(BaseModel):
    cedula: str = Field(min_length=8, max_length=20)

class RegistrarAporteIn(BaseModel):
    cedula: str = Field(min_length=8, max_length=20)
    meses: List[str] = Field(..., description=f"Meses a marcar como pagados. Permitidos: {MESES_VALIDOS}")
    valor_mensual: float = 10.0
    fecha_pago: Optional[date] = None
    observaciones: Optional[str] = None
    numero_comprobante: Optional[int] = None  # si omites, se autogenera

class ComprobanteOut(BaseModel):
    id: int
    cedula: str
    fecha_pago: datetime
    total: float
    ingreso: float
    meses_vencidos: Optional[str] = None
    meses_adelantados: Optional[str] = None
    numero_comprobante: int
    observaciones: Optional[str] = None
    created_at: datetime

class HistorialPaged(BaseModel):
    page: int
    size: int
    total: int
    items: list[ComprobanteOut]

class PaginationInfoAportes(BaseModel):
    pagina_actual: int
    total_paginas: int
    total_aportes: int
    limite: int
    skip: int

class AportesResponse(BaseModel):
    aportes: List[AporteOut]
    paginacion: PaginationInfoAportes
