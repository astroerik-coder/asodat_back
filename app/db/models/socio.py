from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Enum, Text
from app.db.base import Base
import enum

class TipoUsuario(str, enum.Enum):
    nuevo = "nuevo"
    adherente = "adherente"
    fundador = "fundador"

class Socio(Base):
    __tablename__ = "socios"
    cedula: Mapped[str] = mapped_column(String(15), primary_key=True)
    apellidos_nombres: Mapped[str | None] = mapped_column(String(255))
    campus: Mapped[str | None] = mapped_column(String(50))
    genero: Mapped[str | None] = mapped_column(String(1))
    regimen: Mapped[str | None] = mapped_column(String(50))
    celular: Mapped[str | None] = mapped_column(String(15))
    rol: Mapped[str | None] = mapped_column(String(20))
    cargo: Mapped[str | None] = mapped_column(String(255))
    direccion: Mapped[str | None] = mapped_column(String(255))
    fecha_afiliacion: Mapped[date | None] = mapped_column(Date)
    documento_pdf: Mapped[str | None] = mapped_column(String(255))
    observaciones: Mapped[str | None] = mapped_column(Text)
    correo: Mapped[str | None] = mapped_column(String(30))
    tipo_usuario: Mapped[TipoUsuario | None] = mapped_column(Enum(TipoUsuario), default=TipoUsuario.nuevo)
