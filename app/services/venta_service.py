from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.models.stock import StockPrenda
from app.schemas.venta import VentaCreate


async def procesar_venta(db: AsyncSession, venta_in: VentaCreate, id_usuario: int) -> Venta:

    nueva_venta = Venta(
        id_usuario=id_usuario,
        total=Decimal("0.00")
    )

    acumulador_total = Decimal("0.00")
    detalles_a_crear = []

    for item in venta_in.productos:
        query_stock = select(StockPrenda).where(StockPrenda.id_stock_prenda == item.id_stock_prenda)
        result_stock = await db.execute(query_stock)
        variante_stock = result_stock.scalar_one_or_none()

        if not variante_stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La variante de producto con ID {item.id_stock_prenda} no existe."
            )

        if variante_stock.stock_actual < item.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para la variante ID {item.id_stock_prenda}. "
                       f"Disponibles: {variante_stock.stock_actual}, Solicitados: {item.cantidad}."
            )

        variante_stock.stock_actual -= item.cantidad

        subtotal_item = variante_stock.precio_venta * item.cantidad
        acumulador_total += subtotal_item

        nuevo_detalle = DetalleVenta(
            id_stock_prenda=item.id_stock_prenda,
            cantidad=item.cantidad,
            precio_unitario=variante_stock.precio_venta
        )
        detalles_a_crear.append(nuevo_detalle)

    nueva_venta.total = acumulador_total
    nueva_venta.detalles = detalles_a_crear

    db.add(nueva_venta)
    await db.commit()

    query_final = (
        select(Venta)
        .where(Venta.id_venta == nueva_venta.id_venta)
        .options(selectinload(Venta.detalles))
    )
    result_final = await db.execute(query_final)
    return result_final.scalar_one()