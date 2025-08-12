from datetime import datetime
from sqlalchemy import String, Numeric, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class HistorialCargaAportes(Base):
    __tablename__ = "historial_carga_aportes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cedula: Mapped[str | None] = mapped_column(String(20))
    nombre: Mapped[str | None] = mapped_column(String(100))
    mes: Mapped[str | None] = mapped_column(String(20))
    monto: Mapped[float | None] = mapped_column(Numeric(10,2))
    archivo: Mapped[str | None] = mapped_column(String(255))
    fecha_registro: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
