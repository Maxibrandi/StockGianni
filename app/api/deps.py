import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

# Importamos las herramientas de conexión y configuración global
from app.core.config import settings
from app.core.database import get_db
# Importamos los repositorios y modelos de datos
from app.models.usuario import Usuario, RolUsuario
from app.repositories import usuario_repo

# Inicializamos el esquema OAuth2. FastAPI inspeccionará automáticamente la cabecera
# de las peticiones buscando un token del tipo 'Bearer'.
# El parámetro tokenUrl le indica a Swagger dónde debe enviar las credenciales para el login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> Usuario:
    """
    Dependencia utilitaria que valida el token JWT y retorna el objeto Usuario autenticado.
    Si el token ha expirado, está alterado o el usuario fue eliminado/desactivado,
    corta el flujo web devolviendo un error 401 Unauthorized.
    """
    # Excepción estándar reutilizable para fallos de credenciales
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o el token ha expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 🌟 LOG DE CONTROL
        print(f"🔑 DEPS - Usando secreto para DECODIFICAR: '{settings.JWT_SECRET}'")

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            print("🚨 ERROR: El campo 'sub' no viene en el payload o está vacío.")  # <- LOG
            raise credentials_exception

    except Exception as e:
        # 🌟 ESTO VA A IMPRIMIR EL ERROR REAL EN TU TERMINAL DE DOCKER:
        print(f"🚨 ERROR DE DECODIFICACIÓN JWT: {str(e)}")
        print(f"Token recibido: {token}")
        raise credentials_exception

    # 3. Buscar al usuario en la base de datos para confirmar su vigencia
    usuario = await usuario_repo.get_user_by_email(db, email=email)
    if usuario is None:
        raise credentials_exception

    # 4. Verificar si el usuario sufrió una baja lógica (parámetro de seguridad adicional)
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario se encuentra inactivo en el sistema.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Devolvemos la instancia completa del usuario ORM
    return usuario


async def get_current_admin(
        current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Dependencia utilitaria de segundo nivel (encadenada).
    Toma el usuario ya validado por 'get_current_user' y comprueba si tiene rol de Administrador.
    Si el usuario es un Vendedor, deniega el acceso con un error 403 Forbidden.
    """
    # Evaluar si el rol coincide con la restricción jerárquica
    if current_user.rol != RolUsuario.ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene permisos para realizar esta acción."
        )

    return current_user