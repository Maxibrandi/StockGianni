from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StockPrenda(Base):
    """
    Modelo ORM para la tabla 'stock_prenda'.
    Controla el inventario específico por talle y el código de barras único para escaneo.
    """
    __tablename__ = "stock_prenda"

    id_stock_prenda: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Clave foránea vinculada al catálogo de prendas generales
    id_prenda: Mapped[int] = mapped_column(
        ForeignKey("prenda.id_prenda", ondelete="CASCADE"),
        nullable=False
    )

    talle: Mapped[str] = mapped_column(String(10), nullable=False)  # Ej: S, M, L, XL, 42, 44

    # Código de barras único e indexado para búsquedas instantáneas mediante escáner O(1)
    codigo_barras: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    # Uso de Numeric(10, 2) para almacenar dinero con hasta 2 decimales exactos
    precio_venta: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False
    )

    stock_actual: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stock_minimo: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    # Relación inversa (Many-to-One) hacia el modelo Prenda
    prenda: Mapped["Prenda"] = relationship(
        "Prenda",
        back_populates="variantes"
    )

    def __repr__(self) -> str:
        return f"<StockPrenda(id={self.id_stock_prenda}, codigo_barras='{self.codigo_barras}', stock={self.stock_actual})>"