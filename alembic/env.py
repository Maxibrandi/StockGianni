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
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL

    # Limpieza absoluta del driver asíncrono
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
    """Run migrations in 'online' mode."""
    # Obtenemos la sección de configuración de alembic.ini si existiera
    configuration = config.get_section(config.config_ini_section) or {}

    url = settings.DATABASE_URL

    # Forzar estrictamente el uso del dialecto síncrono estándar de PostgreSQL
    if "postgresql+asyncpg://" in url:
        url = url.replace("postgresql+asyncpg://", "postgresql://")

    # Inyectamos de forma directa la URL limpia sobreescribiendo cualquier residuo
    configuration["sqlalchemy.url"] = url

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