from decimal import Decimal
from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class DetalleVenta(Base):

    __tablename__ = "detalle_venta"

    id_detalle_venta: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id_venta: Mapped[int] = mapped_column(
        ForeignKey("venta.id_venta", ondelete="CASCADE"),
        nullable=False
    )

    id_stock_prenda: Mapped[int] = mapped_column(
        ForeignKey("stock_prenda.id_stock_prenda"),
        nullable=False
    )

    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    precio_unitario: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False
    )

    venta: Mapped["Venta"] = relationship(
        "Venta",
        back_populates="detalles"
    )

    variante_prenda: Mapped["StockPrenda"] = relationship(
        "StockPrenda"
    )

    def __repr__(self) -> str:
        return f"<DetalleVenta(id={self.id_detalle_venta}, id_venta={self.id_venta}, cantidad={self.cantidad})>"