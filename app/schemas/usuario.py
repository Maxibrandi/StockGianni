from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from app.models.usuario import RolUsuario


class UsuarioBase(BaseModel):

    nombre: str = Field(..., max_length=100)
    email: EmailStr = Field(...)
    rol: RolUsuario = Field(default=RolUsuario.VENDEDOR)


class UsuarioCreate(UsuarioBase):
    password: str = Field(...)

    @field_validator("password")
    @classmethod
    # Validacion de constraseña con Pydantic
    def validar_longitud_password(cls, v: str) -> str:

        if len(v) < 6:
            raise ValueError("La contraseña debe tener un mínimo de 6 caracteres.")
        return v


class UsuarioResponse(UsuarioBase):
    #Filtra datos sensibles y configuracion pydantic
    id_usuario: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str