from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, func
from app.db.base import Base

class PasswordResetToken(Base):
    __tablename__ = "password_resets"
    jti: Mapped[str] = mapped_column(String(64), primary_key=True)  
    cedula: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
