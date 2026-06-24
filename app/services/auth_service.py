from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Importamos las funciones necesarias de la capa de repositorios
from app.repositories import usuario_repo
# Importamos la lógica de encriptación de la capa de seguridad
from app.core.security import get_password_hash
# Importamos los esquemas y modelos necesarios para el tipado
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


async def registrar_nuevo_usuario(db: AsyncSession, user_in: UsuarioCreate) -> Usuario:
    """
    Servicio de negocio para gestionar el registro de nuevos usuarios en el sistema.
    Valida políticas comerciales, encripta credenciales y coordina la persistencia.

    Args:
        db (AsyncSession): Sesión asíncrona de la base de datos activa.
        user_in (UsuarioCreate): Esquema de validación Pydantic con los datos de entrada.

    Raises:
        HTTPException: Si el correo electrónico ya está registrado en el sistema.

    Returns:
        Usuario: El objeto del modelo ORM persistido e inicializado.
    """
    # 1. Regla de Negocio: Verificar si el correo electrónico ya está en uso
    usuario_existente = await usuario_repo.get_user_by_email(db, email=user_in.email)

    if usuario_existente:
        # Si el usuario ya existe, cortamos el flujo de inmediato lanzando una excepción HTTP
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado."
        )

    # 2. Lógica de Seguridad: Encriptar la contraseña en texto plano suministrada en el DTO
    password_hasheada = get_password_hash(user_in.password)

    # 3. Capa de Persistencia: Delegar la inserción de datos en la BD al repositorio correspondiente
    nuevo_usuario = await usuario_repo.create_user(
        db=db,
        user_in=user_in,
        password_hash=password_hasheada
    )

    return nuevo_usuario