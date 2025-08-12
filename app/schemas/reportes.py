from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

class ReporteSocio(BaseModel):
    cedula: str
    nombre: Optional[str] = None
    campus: Optional[str] = None
    rol: Optional[str] = None
    tipo_usuario: Optional[str] = None
    fecha_afiliacion: Optional[date] = None

class ReporteAporte(BaseModel):
    cedula: str
    nombre: Optional[str] = None
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

class ReporteComprobante(BaseModel):
    id: int
    cedula: str
    fecha_pago: datetime
    total: float
    ingreso: float = 0.0
    numero_comprobante: int
    observaciones: Optional[str] = None

class PaginationInfoReportes(BaseModel):
    pagina_actual: int
    total_paginas: int
    total_registros: int
    limite: int
    skip: int

class ReporteSociosResponse(BaseModel):
    socios: List[ReporteSocio]
    paginacion: PaginationInfoReportes

class ReporteAportesResponse(BaseModel):
    aportes: List[ReporteAporte]

class ReporteComprobantesResponse(BaseModel):
    comprobantes: List[ReporteComprobante]
