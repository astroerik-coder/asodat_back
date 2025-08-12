from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class InicioSesion(Base):
    __tablename__ = "iniciosesion"
    cedula: Mapped[str] = mapped_column(String(15), primary_key=True)
    contrasena: Mapped[str | None] = mapped_column(String(20))
