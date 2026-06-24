from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# ESQUEMAS PARA EL DETALLE DE LA VENTA
# ==========================================

class DetalleVentaCreate(BaseModel):
    """
    Validación para cada renglón de artículos que el vendedor envía
    desde su puesto de trabajo al realizar una venta.
    """
    id_stock_prenda: int = Field(..., description="ID de la variante específica de la prenda (talle/código)")
    cantidad: int = Field(..., ge=1, description="Cantidad física a vender. Debe ser mayor o igual a 1.")


class DetalleVentaResponse(BaseModel):
    """
    Esquema de salida para renderizar cada ítem despachado dentro de la venta.
    Incluye el precio unitario histórico congelado al momento de la compra.
    """
    id_detalle_venta: int
    id_stock_prenda: int
    cantidad: int
    precio_unitario: Decimal

    # Habilita el mapeo automático desde los objetos ORM de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# ESQUEMAS PARA LA CABECERA DE LA VENTA
# ==========================================

class VentaCreate(BaseModel):
    """
    Esquema principal de entrada para la creación de una transacción.
    Garantiza que no se procesen facturas vacías mediante la regla 'min_length=1'.
    """
    productos: List[DetalleVentaCreate] = Field(
        ...,
        min_length=1,
        description="Listado de productos y cantidades que componen la venta física"
    )


class VentaResponse(BaseModel):
    """
    Esquema de salida estructurado que representa el comprobante o factura final de la venta.
    """
    id_venta: int
    fecha_venta: datetime
    total: Decimal
    id_usuario: int
    detalles: List[DetalleVentaResponse] = Field(
        default=[],
        alias="detalles",
        description="Líneas de detalle asociadas a la transacción"
    )

    # Configuración nativa de Pydantic v2 para la lectura directa del ORM asíncrono
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)