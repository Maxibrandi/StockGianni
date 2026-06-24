import enum
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

# Importamos la clase base declarativa desde la configuración de la base de datos
from app.core.database import Base


class RolUsuario(str, enum.Enum):
    """
    Definición de los roles admitidos en el sistema utilizando un Enum de Python.
    Heredar de 'str' facilita la serialización y persistencia en la base de datos.
    """
    ADMINISTRADOR = "administrador"
    VENDEDOR = "vendedor"


class Usuario(Base):
    """
    Modelo ORM que representa la tabla 'usuario' en la base de datos.
    Utiliza la sintaxis estricta y tipada de SQLAlchemy 2.0.
    """
    __tablename__ = "usuario"

    # Clave Primaria (Autoincremental por defecto en enteros en SQLAlchemy)
    id_usuario: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    # Nombre completo del personal
    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Email utilizado como identificador para el login (único e indexado para búsquedas rápidas)
    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False
    )

    # Hash de la contraseña para cumplir con la autenticación segura
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Rol asignado utilizando el Enum nativo mapeado en la base de datos
    rol: Mapped[RolUsuario] = mapped_column(
        Enum(RolUsuario, name="rol_usuario_enum"),
        nullable=False,
        default=RolUsuario.VENDEDOR
    )

    # Atributo para la baja lógica del usuario (evita romper la integridad de las ventas históricas)
    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self) -> str:
        return f"<Usuario(id={self.id_usuario}, email='{self.email}', rol='{self.rol}')>"