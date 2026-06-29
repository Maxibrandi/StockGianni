from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.repositories import usuario_repo
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.token import Token

router = APIRouter()


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario"
)
async def register_user(user_in: UsuarioCreate, db: AsyncSession = Depends(get_db)):
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


    usuario = await usuario_repo.get_user_by_email(db, email=form_data.username)

    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    contrasenia_valida = verify_password(form_data.password, usuario.password_hash)
    if not contrasenia_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_payload = {
        "sub": usuario.email,
        "rol": usuario.rol
    }
    jwt_string = create_access_token(data=token_payload)

    return {
        "access_token": jwt_string,
        "token_type": "bearer"
    }