from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# ESQUEMAS PARA VARIANTES DE STOCK (StockPrenda)
# ==========================================

class StockPrendaBase(BaseModel):
    """
    Atributos comunes para el control de inventario y variantes de una prenda.
    """
    talle: str = Field(..., max_length=10, description="Talle de la variante (ej: S, M, L, 42)")
    codigo_barras: str = Field(..., max_length=50, description="Código de barras único para escaneo rápido")
    precio_venta: Decimal = Field(..., max_digits=10, decimal_places=2, ge=0, description="Precio de venta exacto")
    stock_actual: int = Field(default=0, ge=0, description="Cantidad física disponible en el local")
    stock_minimo: int = Field(default=5, ge=0, description="Umbral mínimo para disparar alertas de reposición")


class StockPrendaCreate(StockPrendaBase):
    """
    Esquema utilizado para la creación de una variante de stock.
    Hereda directamente de la base sin campos adicionales.
    """
    pass


class StockPrendaResponse(StockPrendaBase):
    """
    Esquema de salida para las variantes de stock.
    Incluye su ID único e identifica a qué prenda pertenece.
    """
    id_stock_prenda: int
    id_prenda: int

    # Configuración nativa de Pydantic v2 para mapear desde modelos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# ESQUEMAS PARA EL MAESTRO DE PRENDAS (Prenda)
# ==========================================

class PrendaBase(BaseModel):
    """
    Atributos globales e inherentes al diseño o modelo de la prenda de indumentaria.
    """
    nombre: str = Field(..., max_length=100, description="Nombre descriptivo del artículo (ej: Remera Térmica)")
    categoria: str = Field(..., max_length=50, description="Categoría de la prenda (ej: Superior, Inferior, Accesorios)")
    tipo_tela: str = Field(..., max_length=50, description="Composición textil (ej: Algodón, Denim, Lycra)")


class PrendaCreate(PrendaBase):
    """
    Esquema clave para el endpoint de alta del producto.
    Habilita la validación anidada recibiendo una lista de variantes de stock.
    """
    variantes: List[StockPrendaCreate] = Field(
        ...,
        min_length=1,
        description="Lista de variantes por talle que se inicializarán con la prenda"
    )


class PrendaResponse(PrendaBase):
    """
    Esquema de salida completo del catálogo.
    Incluye ID, estado de baja lógica y serializa sus variantes asociadas de forma automática.
    """
    id_prenda: int
    activo: bool
    variantes: List[StockPrendaResponse] = []

    # Configuración nativa de Pydantic v2 para mapear desde modelos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class StockPrendaConPadreResponse(StockPrendaResponse):
    """
    Extensión para reportes donde se necesita saber la información
    maestra de la prenda además de la variante física.
    """
    # Pydantic validará e incluirá el objeto PrendaBase de forma anidada
    prenda: PrendaBase