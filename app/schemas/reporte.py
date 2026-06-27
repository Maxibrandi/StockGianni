from pydantic import BaseModel
from decimal import Decimal
from typing import List

class ProductoMasVendido(BaseModel):
    nombre: str
    talle: str
    cantidad_vendida: int

class ReporteEstadisticoResponse(BaseModel):
    total_recaudado: Decimal
    cantidad_ventas: int
    ticket_promedio: Decimal
    productos_top: List[ProductoMasVendido]