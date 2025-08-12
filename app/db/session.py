from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Usar la URL de conexión de Supabase (sin parámetros de pgbouncer)
DATABASE_URL = settings.database_url

# Engine para operaciones normales (usando connection pooling)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    # Configuraciones específicas para Supabase
    connect_args={
        "sslmode": "require"
    }
)

# Engine para migraciones (conexión directa)
direct_engine = create_engine(
    settings.direct_url,
    pool_pre_ping=True,
    # Para migraciones, usar NullPool para evitar problemas
    poolclass=NullPool,
    connect_args={
        "sslmode": "require"
    }
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
