from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import usuario_repo
from app.core.security import get_password_hash
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


async def registrar_nuevo_usuario(db: AsyncSession, user_in: UsuarioCreate) -> Usuario:

    usuario_existente = await usuario_repo.get_user_by_email(db, email=user_in.email)

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado."
        )

    password_hasheada = get_password_hash(user_in.password)

    nuevo_usuario = await usuario_repo.create_user(
        db=db,
        user_in=user_in,
        password_hash=password_hasheada
    )

    return nuevo_usuario