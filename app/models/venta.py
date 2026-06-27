from datetime import datetime, timezone
from decimal import Decimal
from typing import List
from sqlalchemy import Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


# 💡 Eliminamos el import de DetalleVenta para romper el bucle circular

class Venta(Base):
    """
    Modelo ORM para la tabla 'venta'.
    Almacena la cabecera de cada transacción de salida realizada en el local.
    """
    __tablename__ = "venta"

    id_venta: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    fecha_venta: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False
    )

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )

    # Esto funciona perfectamente sin el import gracias a las comillas ""
    detalles: Mapped[List["DetalleVenta"]] = relationship(
        "DetalleVenta",
        back_populates="venta",
        cascade="all, delete-orphan"
    )

    vendedor: Mapped["Usuario"] = relationship(
        "Usuario"
    )

    def __repr__(self) -> str:
        return f"<Venta(id={self.id_venta}, total={self.total}, fecha={self.fecha_venta})>"