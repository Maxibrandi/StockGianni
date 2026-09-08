# app/core/database.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# 🌟 MODIFICACIÓN AQUÍ: Cambiar settings.DATABASE_URL por settings.ASYNC_DATABASE_URL
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False,
    future=True
)

SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()