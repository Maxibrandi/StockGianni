from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
# Reemplaza con las rutas exactas de tus modelos de venta/detalles
from app.models.detalle_venta import DetalleVenta  # <-- Ahora lo traemos de su nuevo hogarfrom app.models.prenda import Prenda
from app.models.stock import StockPrenda


class ReporteRepository:

    async def obtener_metricas_periodo(self, db: AsyncSession, desde: datetime, hasta: datetime):
        # 1. Total Recaudado y Cantidad de Transacciones
        query_ventas = (
            select(
                func.sum(Venta.total).label("total"),
                func.count(Venta.id_venta).label("cantidad")
            )
            .where(Venta.fecha_venta.between(desde, hasta))
        )
        res_ventas = await db.execute(query_ventas)
        total, cantidad = res_ventas.fetchone()

        total_recaudado = total if total else Decimal("0.00")
        cantidad_ventas = cantidad if cantidad else 0
        ticket_promedio = total_recaudado / cantidad_ventas if cantidad_ventas > 0 else Decimal("0.00")

        # 2. Ranking de los 5 productos más vendidos del periodo
        query_top = (
            select(
                Prenda.nombre,
                StockPrenda.talle,
                func.sum(DetalleVenta.cantidad).label("total_cant")
            )
            .join(DetalleVenta.variante)  # Conecta DetalleVenta con StockPrenda
            .join(StockPrenda.prenda)  # Conecta StockPrenda con Prenda (Padre)
            .join(Venta)  # Conecta Detalle con el encabezado Venta para la fecha
            .where(Venta.fecha_venta.between(desde, hasta))
            .group_by(Prenda.nombre, StockPrenda.talle)
            .order_by(func.sum(DetalleVenta.cantidad).desc())
            .limit(5)
        )
        res_top = await db.execute(query_top)
        top_productos = [
            {"nombre": r[0], "talle": r[1], "cantidad_vendida": r[2]}
            for r in res_top.fetchall()
        ]

        return {
            "total_recaudado": total_recaudado,
            "cantidad_ventas": cantidad_ventas,
            "ticket_promedio": ticket_promedio,
            "productos_top": top_productos
        }