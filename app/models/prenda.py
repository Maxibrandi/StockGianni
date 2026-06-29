import random  # <-- Agregado para que no falle tu método estático
from typing import List
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Prenda(Base):
    __tablename__ = "prenda"

    id_prenda: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    tipo_tela: Mapped[str] = mapped_column(String(50), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ❌ SE ELIMINÓ LA COLUMNA codigo_barras DE AQUÍ

    # Una prenda general puede tener distintos talles y códigos de barra
    variantes: Mapped[List["StockPrenda"]] = relationship(
        "StockPrenda",
        back_populates="prenda",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Prenda(id={self.id_prenda}, nombre='{self.nombre}', categoria='{self.categoria}')>"

    # Metodo para generar el codigo de barras
    @staticmethod
    def generar_codigo_unico():
        return "".join([str(random.randint(0, 9)) for _ in range(12)])