from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class CupoSocio(Base):
    __tablename__ = "cupossocios"
    cedula: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombrecompleto: Mapped[str] = mapped_column(String(100))
    cupo: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
