from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from app.db.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    cedula: Mapped[str] = mapped_column(String(15), primary_key=True)
    contrasena: Mapped[str] = mapped_column(String(20))
    rol: Mapped[str | None] = mapped_column(String(20), default="socio")
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
