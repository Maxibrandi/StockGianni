from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class StockPrendaBase(BaseModel):
    talle: str = Field(..., max_length=10)

    # 🔄 MODIFICADO: Ahora es Optional y su valor por defecto es None
    codigo_barras: Optional[str] = Field(default=None, max_length=50)

    precio_venta: Decimal = Field(..., max_digits=10, decimal_places=2, ge=0)
    stock_actual: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=5, ge=0)


# El resto del archivo queda exactamente igual...
class StockPrendaCreate(StockPrendaBase):
    pass


class StockPrendaResponse(StockPrendaBase):
    id_stock_prenda: int
    id_prenda: int
    model_config = ConfigDict(from_attributes=True)


class PrendaBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    categoria: str = Field(..., max_length=50)
    tipo_tela: str = Field(..., max_length=50)


class PrendaCreate(PrendaBase):
    variantes: List[StockPrendaCreate] = Field(..., min_length=1)


class PrendaResponse(PrendaBase):
    id_prenda: int
    activo: bool
    variantes: List[StockPrendaResponse] = []
    model_config = ConfigDict(from_attributes=True)


class StockPrendaConPadreResponse(StockPrendaResponse):
    prenda: PrendaBase

class StockPrendaUpdate(BaseModel):
    id_stock_prenda: int
    precio_venta: Optional[Decimal] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None

class PrendaUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    tipo_tela: Optional[str] = None
    variantes: Optional[List[StockPrendaUpdate]] = None

    class Config:
        from_attributes = True