from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.models.usuario import Usuario, RolUsuario
from app.repositories import usuario_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> Usuario:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o el token ha expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    # Buscar al usuario en la base de datos para confirmar su vigencia
    usuario = await usuario_repo.get_user_by_email(db, email=email)
    if usuario is None:
        raise credentials_exception

    # Verificar si el usuario sufrió una baja lógica
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario se encuentra inactivo en el sistema.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario


async def get_current_admin(
        current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    rol_str = current_user.rol.value if hasattr(current_user.rol, 'value') else str(current_user.rol)
    if rol_str.lower() not in ("administrador", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene permisos para realizar esta acción."
        )

    return current_user