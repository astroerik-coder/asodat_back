from pydantic import BaseModel, Field

class LoginIn(BaseModel):
    cedula: str = Field(min_length=8, max_length=20)
    password: str = Field(min_length=4, max_length=100)

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    rol: str

class RefreshIn(BaseModel):
    refresh_token: str

class LogoutIn(BaseModel):
    refresh_token: str
