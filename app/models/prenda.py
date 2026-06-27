from typing import List
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Prenda(Base):
    """
    Modelo ORM para la tabla 'prenda'.
    Representa el catálogo maestro de artículos de indumentaria.
    """
    __tablename__ = "prenda"

    id_prenda: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)  # Ej: Superior, Inferior, Accesorios
    tipo_tela: Mapped[str] = mapped_column(String(50), nullable=False)  # Ej: Algodón, Denim, Lycra
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    codigo_barras = mapped_column(String, unique=True, index=True, nullable=False)


    # Relación uno-a-muchos (One-to-Many) hacia StockPrenda
    # Una prenda general puede tener múltiples variantes de talles y códigos de barra
    variantes: Mapped[List["StockPrenda"]] = relationship(
        "StockPrenda",
        back_populates="prenda",
        cascade="all, delete-orphan"  # Si se elimina la prenda, se eliminan sus variantes de stock
    )

    def __repr__(self) -> str:
        return f"<Prenda(id={self.id_prenda}, nombre='{self.nombre}', categoria='{self.categoria}')>"


    # 2. AGREGA ESTE MÉTODO (Genera 12 números aleatorios)
    @staticmethod
    def generar_codigo_unico():
        return "".join([str(random.randint(0, 9)) for _ in range(12)])