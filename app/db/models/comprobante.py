from datetime import datetime
from sqlalchemy import String, Numeric, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ComprobantePago(Base):
    __tablename__ = "comprobantes_pago"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cedula: Mapped[str] = mapped_column(String(10))
    fecha_pago: Mapped[datetime] = mapped_column(DateTime)
    total: Mapped[float] = mapped_column(Numeric(10,2))
    ingreso: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    meses_vencidos: Mapped[str | None] = mapped_column(Text)
    meses_adelantados: Mapped[str | None] = mapped_column(Text)
    numero_comprobante: Mapped[int] = mapped_column(Integer, unique=True)
    observaciones: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
