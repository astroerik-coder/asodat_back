from pydantic import BaseModel, Field
from typing import Optional

class ForgotPasswordIn(BaseModel):
    cedula: Optional[str] = None
    correo: Optional[str] = None

class ForgotPasswordOut(BaseModel):
    message: str
    reset_token: Optional[str] = None  # lo exponemos en DEV para pruebas

class ResetPasswordIn(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)

class ChangePasswordIn(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8, max_length=128)
