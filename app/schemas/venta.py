from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel, ConfigDict, Field


class DetalleVentaCreate(BaseModel):

    id_stock_prenda: int = Field(...)
    cantidad: int = Field(..., ge=1)


class DetalleVentaResponse(BaseModel):

    id_detalle_venta: int
    id_stock_prenda: int
    cantidad: int
    precio_unitario: Decimal

    # Configuración nativa de Pydantic v2
    model_config = ConfigDict(from_attributes=True)


class VentaCreate(BaseModel):

        productos: List[DetalleVentaCreate] = Field(...,min_length=1,)


class VentaResponse(BaseModel):

    id_venta: int
    fecha_venta: datetime
    total: Decimal
    id_usuario: int
    detalles: List[DetalleVentaResponse] = Field(
        default=[],
        alias="detalles",
        )

    # Configuración nativa de Pydantic v2
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)