from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Importamos el objeto settings desde la capa core de configuración
from app.core.config import settings

# 1. Crear la instancia del motor asíncrono para PostgreSQL
# Se utiliza el driver asyncpg especificado en la URL de conexión del archivo .env
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Cambiar a True si deseas ver las consultas SQL crudas en la consola en desarrollo
    future=True  # Asegura total compatibilidad con las directrices de SQLAlchemy 2.0
)

# 2. Crear la fábrica de sesiones asíncronas
# Configurar expire_on_commit=False es vital en entornos asíncronos para evitar que
# SQLAlchemy intente emitir consultas perezosas (lazy loads) transparentes tras un commit.
SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession  # Especificamos explícitamente el uso de sesiones asíncronas
)

# 3. Crear la clase base declarativa para el mapeo de los modelos ORM
# Todos los modelos de datos (Usuario, Prenda, StockPrenda, etc.) heredarán de esta clase base
class Base(DeclarativeBase):
    pass

# 4. Función generadora asíncrona (Dependencia para FastAPI)
# Abre una sesión por cada petición HTTP entrante, la expone mediante 'yield'
# y garantiza su cierre seguro gracias al bloque try/finally.
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        # Se asegura de liberar los recursos de la conexión y cerrar la sesión de forma asíncrona
        await session.close()