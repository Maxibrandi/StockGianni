from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str

    # Atributos de Seguridad JWT
    JWT_SECRET: str = "clave_secreta_super_segura_para_desarrollo_123"
    ALGORITHM: str = "HS256"
    JWT_ALGORITHM: str = "HS256"  # 🌟 Agregado para resolver el AttributeError
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url


settings = Settings()