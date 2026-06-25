import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# ------------------------------------------------------------------
# CONFIGURACIÓN PERSONALIZADA: Importación de Ajustes y Modelos ORM
# ------------------------------------------------------------------
from app.core.config import settings
from app.core.database import Base
import app.models
from app.models.venta import Venta
from app.models.usuario import Usuario


target_metadata = Base.metadata

# Es CRUCIAL importar todos los modelos explícitamente para el --autogenerate
from app.models.usuario import Usuario
from app.models.prenda import Prenda
from app.models.stock import StockPrenda
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta

# ------------------------------------------------------------------

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging. This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------------------------------------------------------
# MODIFICACIÓN: Apuntar la metadata hacia nuestros modelos mapeados
# ------------------------------------------------------------------
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
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


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an async connection."""
    configuration = config.get_section(config.config_ini_section) or {}

    # Usamos directamente la URL asíncrona de la configuración de tu App
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Ejecutamos la migración online de forma asíncrona
    asyncio.run(run_migrations_online())