from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# ------------------------------------------------------------------
# CONFIGURACIÓN PERSONALIZADA: Importación de Ajustes y Modelos ORM
# ------------------------------------------------------------------
from app.core.config import settings
from app.core.database import Base

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
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DB API to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    # Para el modo offline, también interceptamos la URL y la hacemos dinámica
    url = settings.DATABASE_URL
    # Truco Pro: Alembic nativo corre sincrónico bajo el capó. Si usas asyncpg,
    # reemplazamos el driver para que no falle al generar scripts SQL offline.
    if "postgresql+asyncpg://" in url:
        url = url.replace("postgresql+asyncpg://", "postgresql://")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # ------------------------------------------------------------------
    # MODIFICACIÓN: Inyección dinámica de la URL desde la configuración
    # ------------------------------------------------------------------
    configuration = config.get_section(config.config_ini_section) or {}

    url = settings.DATABASE_URL
    # Forzamos el driver síncrono estándar (postgresql://) únicamente durante
    # la ejecución de las migraciones para evitar conflictos de hilos con asyncpg.
    if "postgresql+asyncpg://" in url:
        url = url.replace("postgresql+asyncpg://", "postgresql://")

    configuration["sqlalchemy.url"] = url

    # Pasamos la configuración modificada al generador del engine
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()