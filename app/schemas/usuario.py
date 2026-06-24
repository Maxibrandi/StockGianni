from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from app.models.usuario import RolUsuario  # Importamos el Enum que creamos en el modelo


class UsuarioBase(BaseModel):
    """
    Esquema base que contiene los atributos compartidos
    para la lectura y escritura de un usuario.
    """
    nombre: str = Field(..., max_length=100, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico único del usuario")
    rol: RolUsuario = Field(default=RolUsuario.VENDEDOR, description="Rol de acceso en el sistema")


class UsuarioCreate(UsuarioBase):
    """
    Esquema utilizado exclusivamente para el endpoint de registro/creación.
    Recibe la contraseña en texto plano enviada por el cliente antes de ser hasheada.
    """
    password: str = Field(..., description="Contraseña en texto plano suministrada por el usuario")

    @field_validator("password")
    @classmethod
    def validar_longitud_password(cls, v: str) -> str:
        """
        Validador de campo en Pydantic v2 para asegurar políticas mínimas de seguridad
        en la contraseña ingresada por el Administrador.
        """
        if len(v) < 6:
            raise ValueError("La contraseña debe tener un mínimo de 6 caracteres.")
        return v


class UsuarioResponse(UsuarioBase):
    """
    Esquema de salida (Response Model) que la API devolverá al cliente.
    Filtra datos sensibles (como la contraseña) y añade metadatos del registro.
    """
    id_usuario: int
    activo: bool

    # Configuración de Pydantic v2 para permitir la lectura directa desde objetos ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str