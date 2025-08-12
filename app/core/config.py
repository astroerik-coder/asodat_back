from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuración de Supabase
    supabase_url: str
    supabase_key: str
    
    # Configuración de base de datos PostgreSQL en Supabase
    database_url: str
    direct_url: str
    
    # Configuración JWT
    jwt_secret: str
    jwt_alg: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    
    # Configuración CORS
    cors_origins: str = "*"

    class Config:
        env_file = ".env"
        extra = "allow"  # Permite variables extra

settings = Settings()
