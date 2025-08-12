from fastapi import APIRouter
from app.core.validators import validar_cedula_ec, normalize_cedula

router = APIRouter(prefix="/validaciones", tags=["validaciones"])

@router.get("/cedula/{cedula}")
def validar_cedula(cedula: str):
    c = normalize_cedula(cedula)
    return {"cedula": c, "valida": validar_cedula_ec(c)}
