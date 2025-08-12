from datetime import date
from sqlalchemy import String, Integer, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Noticia(Base):
    __tablename__ = "noticias"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str | None] = mapped_column(String(255))
    contenido: Mapped[str | None] = mapped_column(Text)
    categoria: Mapped[str | None] = mapped_column(String(50))
    fecha: Mapped[date | None] = mapped_column(Date)
    imagen: Mapped[str | None] = mapped_column(String(255))
