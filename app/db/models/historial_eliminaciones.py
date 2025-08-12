from datetime import date, datetime
from sqlalchemy import String, Date, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class HistorialEliminaciones(Base):
    __tablename__ = "historial_eliminaciones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cedula: Mapped[str] = mapped_column(String(15))
    nombre_completo: Mapped[str] = mapped_column(String(255))
    fecha_afiliacion: Mapped[date] = mapped_column(Date)
    motivo: Mapped[str] = mapped_column(Text)
    fecha_eliminacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
