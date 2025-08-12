from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada genérica"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

class MessageResponse(BaseModel):
    """Respuesta de mensaje simple"""
    message: str
    detail: Optional[str] = None

class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
