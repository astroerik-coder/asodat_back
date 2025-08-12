from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, func
from app.db.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    jti: Mapped[str] = mapped_column(String(64), primary_key=True)
    cedula: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
