import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# 🌟 Calculamos la raíz del proyecto de forma dinámica (sube dos niveles desde este archivo config.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")
    JWT_SECRET: str = Field(..., validation_alias="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", validation_alias="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Configuración de Pydantic v2 optimizada para Docker y Local
    model_config = SettingsConfigDict(
        # 🌟 Ahora le pasamos la ruta absoluta exacta del .env
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()