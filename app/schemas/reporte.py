from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional

class ProductoMasVendido(BaseModel):
    nombre: str
    talle: str
    cantidad_vendida: int

class ReporteEstadisticoResponse(BaseModel):
    total_recaudado: Decimal
    cantidad_ventas: int
    ticket_promedio: Decimal
    productos_top: List[ProductoMasVendido]

class ResumenGananciasResponse(BaseModel):
    ganancia_diaria: Decimal
    ganancia_mensual: Decimal
    cantidad_ventas_hoy: int
    cantidad_ventas_mes: int
    productos_top: List[ProductoMasVendido]