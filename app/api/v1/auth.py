from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

# Importamos la dependencia de la base de datos
from app.core.database import get_db
# Importamos las herramientas de seguridad y firmado de tokens
from app.core.security import verify_password, create_access_token
# Importamos los repositorios para la consulta de datos
from app.repositories import usuario_repo
# Importamos los esquemas Pydantic necesarios
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.token import Token  # Asumiendo que se guardó en app/schemas/token.py

# Inicializar el enrutador
router = APIRouter()


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario"
)
async def register_user(user_in: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    # ... (Código anterior de registro ya implementado)
    from app.services.auth_service import registrar_nuevo_usuario
    return await registrar_nuevo_usuario(db=db, user_in=user_in)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión y obtener token de acceso",
    description="Autentica a un usuario mediante su correo (username) y contraseña. Devuelve un token JWT."
)
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    """
    Endpoint de Login seguro.

    - **form_data.username**: Almacena el correo electrónico ingresado por el cliente.
    - **form_data.password**: Almacena la contraseña en texto plano.
    """
    # 1. Buscar al usuario en la base de datos a través de su correo electrónico
    # Nota: OAuth2PasswordRequestForm requiere el campo bajo el nombre 'username'
    usuario = await usuario_repo.get_user_by_email(db, email=form_data.username)

    # 2. Primera validación: Verificar que el usuario exista y esté activo
    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Segunda validación: Verificar la contraseña contra el hash de la BD
    contrasenia_valida = verify_password(form_data.password, usuario.password_hash)
    if not contrasenia_valida:
        # Por seguridad extrema, mantenemos exactamente el mismo mensaje de error (evita enumeración de usuarios)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Generación del Payload y firma del Token JWT
    # Guardamos la identidad principal (email) en la clave estándar 'sub' (Subject)
    token_payload = {
        "sub": usuario.email,
        "rol": usuario.rol  # Opcional: inyectamos el rol para acelerar validaciones en el frontend
    }
    jwt_string = create_access_token(data=token_payload)

    # 5. Retornar el esquema estructurado Token
    return {
        "access_token": jwt_string,
        "token_type": "bearer"
    }