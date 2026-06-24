from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Importamos el modelo de datos ORM y el esquema de validación
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[Usuario]:
    """
    Busca un usuario activo o inactivo en la base de datos basándose en su correo electrónico.
    Útil para el flujo de login y para evitar la duplicación de cuentas durante el registro.

    Args:
        db (AsyncSession): Sesión asíncrona de la base de datos conectada.
        email (str): Correo electrónico a consultar.

    Returns:
        Usuario | None: Devuelve la instancia del modelo Usuario si se encuentra,
                        o None de lo contrario.
    """
    # En SQLAlchemy 2.0 se utiliza la función select() junto con await db.execute()
    query = select(Usuario).where(Usuario.email == email)
    result = await db.execute(query)

    # .scalar_one_or_none() extrae el primer objeto mapeado o devuelve None de forma segura
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UsuarioCreate, password_hash: str) -> Usuario:
    """
    Registra un nuevo usuario (Administrador o Vendedor) en el sistema,
    persistiendo sus datos y confirmando la transacción.

    Args:
        db (AsyncSession): Sesión asíncrona de la base de datos conectada.
        user_in (UsuarioCreate): Esquema Pydantic que contiene los datos del cliente.
        password_hash (str): Hash seguro de la contraseña ya procesado por la capa de seguridad.

    Returns:
        Usuario: La instancia del modelo ORM ya guardada, incluyendo el id_usuario autoincremental.
    """
    # 1. Instanciamos el modelo ORM mapeando los atributos comunes del esquema
    # e inyectando explícitamente el hash seguro en lugar de la clave en texto plano.
    nuevo_usuario = Usuario(
        nombre=user_in.nombre,
        email=user_in.email,
        rol=user_in.rol,
        password_hash=password_hash,
        activo=True  # Todo usuario inicia activo por defecto
    )

    # 2. Agregar el objeto a la sesión actual
    db.add(nuevo_usuario)

    # 3. Confirmar (commit) la transacción de forma asíncrona en la base de datos
    await db.commit()

    # 4. Refrescar la instancia para recuperar los datos generados por el motor de la base de datos
    # Esto es indispensable en modo asíncrono para poblar campos automáticos como 'id_usuario'
    await db.refresh(nuevo_usuario)

    return nuevo_usuario