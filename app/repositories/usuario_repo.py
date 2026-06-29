from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[Usuario]:
    query = select(Usuario).where(Usuario.email == email)
    result = await db.execute(query)

    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UsuarioCreate, password_hash: str) -> Usuario:
    nuevo_usuario = Usuario(
        nombre=user_in.nombre,
        email=user_in.email,
        rol=user_in.rol,
        password_hash=password_hash,
        activo=True
    )

    db.add(nuevo_usuario)

    await db.commit()
    await db.refresh(nuevo_usuario)

    return nuevo_usuario