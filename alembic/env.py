import asyncio
from logging.config import fileConfig
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

# ------------------------------------------------------------------
# CONFIGURACIÓN DE PATHS Y MODELOS
# ------------------------------------------------------------------
# Añadir el directorio raíz al path para importar el módulo app
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.config import settings
from app.core.database import Base

# Importar explícitamente todos los modelos para autogenerate de Alembic
from app.models.usuario import Usuario
from app.models.prenda import Prenda
from app.models.stock import StockPrenda
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta

target_metadata = Base.metadata

# Configuración de logs desde alembic.ini
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ------------------------------------------------------------------
# MIGRACIONES OFFLINE
# ------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'."""
    url = settings.ASYNC_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------------------
# MIGRACIONES ONLINE (ASÍNCRONAS)
# ------------------------------------------------------------------
async def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online' usando el engine asíncrono."""
    configuration = config.get_section(config.config_ini_section) or {}

    # Forzar el uso de ASYNC_DATABASE_URL que garantiza el driver postgresql+asyncpg://
    configuration["sqlalchemy.url"] = settings.ASYNC_DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# ------------------------------------------------------------------
# PUNTO DE ENTRADA
# ------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())