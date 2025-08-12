from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_roles
from app.db.models.socio import Socio
from app.db.models.cupo import CupoSocio
from app.db.models.aportes import AportesSocios
from app.schemas.socios import DatosPersonales

router = APIRouter(prefix="/me", tags=["me"])

@router.get("/datos", response_model=DatosPersonales)
def mis_datos(
    user=Depends(require_roles("socio", "tesorero", "secretaria", "presidente")),
    db: Session = Depends(get_db),
):
    s = db.get(Socio, user["cedula"])
    if not s:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return DatosPersonales(
        cedula=s.cedula,
        nombrecompleto=s.apellidos_nombres,
        correo=s.correo,
        celular=s.celular,
        campus=s.campus,
        genero=s.genero,
        regimen=s.regimen,
        cargo=s.cargo,
        direccion=s.direccion,
        fecha_afiliacion=s.fecha_afiliacion,
    )

@router.get("/aportes")
def mis_aportes(
    user=Depends(require_roles("socio", "tesorero", "secretaria", "presidente")),
    db: Session = Depends(get_db),
):
    row = db.get(AportesSocios, user["cedula"])
    if not row:
        return {"cedula": user["cedula"], "meses": {}, "total": 0.0}
    meses = {k: float(getattr(row, k)) if getattr(row, k) is not None else None
             for k in ["dic_24","ene_25","feb_25","mar_25","abr_25","may_25","jun_25","jul_25","ago_25","sept_25","oct_25","nov_25","dic_25"]}
    total = sum(v for v in meses.values() if v)
    estados = {m: ("Pagado" if (v and v > 0) else "No pagado") for m,v in meses.items()}
    return {"cedula": row.cedula, "meses": estados, "valores": meses, "total": total}
