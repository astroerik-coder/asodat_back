from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Aportes(Base):
    __tablename__ = "aportes"
    cedula: Mapped[str] = mapped_column(String(20), primary_key=True)
    apellidos_y_nombres: Mapped[str] = mapped_column(String(255))
    nuevos_ingresos: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    dic_aa: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    enero: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    febrero: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    marzo: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    abril: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    mayo: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    junio: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    julio: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    agosto: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    septiembre: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    octubre: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    noviembre: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)

class AportesSocios(Base):
    __tablename__ = "aportes_socios"
    cedula: Mapped[str] = mapped_column(String(20), primary_key=True)
    apellidos_y_nombres: Mapped[str | None] = mapped_column(String(255))
    nuevos_ingresos: Mapped[float | None] = mapped_column(Numeric(10,2))
    dic_24: Mapped[float | None] = mapped_column(Numeric(10,2))
    ene_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    feb_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    mar_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    abr_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    may_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    jun_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    jul_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    ago_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    sept_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    oct_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    nov_25: Mapped[float | None] = mapped_column(Numeric(10,2))
    dic_25: Mapped[float | None] = mapped_column(Numeric(10,2))
