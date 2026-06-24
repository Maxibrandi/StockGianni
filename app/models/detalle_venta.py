from decimal import Decimal
from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DetalleVenta(Base):
    """
    Modelo ORM para la tabla 'detalle_venta'.
    Representa cada línea o artículo despachado dentro de una venta específica.
    """
    __tablename__ = "detalle_venta"

    id_detalle_venta: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Vínculo con la cabecera de la venta. Si se borra la venta, se eliminan sus renglones.
    id_venta: Mapped[int] = mapped_column(
        ForeignKey("venta.id_venta", ondelete="CASCADE"),
        nullable=False
    )

    # Vínculo con la variante física de stock (saber qué talle/código de barras se redujo)
    id_stock_prenda: Mapped[int] = mapped_column(
        ForeignKey("stock_prenda.id_stock_prenda"),
        nullable=False
    )

    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    # Precio histórico resguardado ante futuras modificaciones de tarifas en el catálogo maestro
    precio_unitario: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False
    )

    # Relación inversa muchos-a-uno hacia la cabecera Venta
    venta: Mapped["Venta"] = relationship(
        "Venta",
        back_populates="detalles"
    )

    # Relación muchos-a-uno hacia StockPrenda para auditoría de talle, código de barras, etc.
    variante_prenda: Mapped["StockPrenda"] = relationship(
        "StockPrenda"
    )

    def __repr__(self) -> str:
        return f"<DetalleVenta(id={self.id_detalle_venta}, id_venta={self.id_venta}, cantidad={self.cantidad})>"