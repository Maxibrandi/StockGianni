from datetime import datetime, timezone
from decimal import Decimal
from typing import List
from sqlalchemy import Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Venta(Base):
    """
    Modelo ORM para la tabla 'venta'.
    Almacena la cabecera de cada transacción de salida realizada en el local.
    """
    __tablename__ = "venta"

    id_venta: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Almacena fecha y hora exacta con soporte de zona horaria (UTC recomendado)
    fecha_venta: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Total de la venta acumulado
    total: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False
    )

    # Clave foránea vinculada al empleado que realizó la operación
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )

    # Relación uno-a-muchos hacia los renglones o detalles de los artículos vendidos
    detalles: Mapped[List["DetalleVenta"]] = relationship(
        "DetalleVenta",
        back_populates="venta",
        cascade="all, delete-orphan"
    )

    # Relación muchos-a-uno hacia el Usuario (Vendedor/Admin)
    vendedor: Mapped["Usuario"] = relationship(
        "Usuario"
    )

    def __repr__(self) -> str:
        return f"<Venta(id={self.id_venta}, total={self.total}, fecha={self.fecha_venta})>"