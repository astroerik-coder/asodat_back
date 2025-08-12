from datetime import datetime
from sqlalchemy import String, Numeric, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class HistorialAportes(Base):
    __tablename__ = "historial_aportes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cedula: Mapped[str | None] = mapped_column(String(20))
    apellidos_y_nombres: Mapped[str | None] = mapped_column(String(255))
    nuevos_ingresos: Mapped[float | None] = mapped_column(Numeric(10,2))
    dic_aa: Mapped[float | None] = mapped_column(Numeric(10,2))
    enero: Mapped[float | None] = mapped_column(Numeric(10,2))
    febrero: Mapped[float | None] = mapped_column(Numeric(10,2))
    marzo: Mapped[float | None] = mapped_column(Numeric(10,2))
    abril: Mapped[float | None] = mapped_column(Numeric(10,2))
    mayo: Mapped[float | None] = mapped_column(Numeric(10,2))
    junio: Mapped[float | None] = mapped_column(Numeric(10,2))
    julio: Mapped[float | None] = mapped_column(Numeric(10,2))
    agosto: Mapped[float | None] = mapped_column(Numeric(10,2))
    septiembre: Mapped[float | None] = mapped_column(Numeric(10,2))
    octubre: Mapped[float | None] = mapped_column(Numeric(10,2))
    noviembre: Mapped[float | None] = mapped_column(Numeric(10,2))
    anio_respaldo: Mapped[int | None] = mapped_column(Integer)
    fecha_respaldo: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
