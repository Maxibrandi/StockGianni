from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.models.stock import StockPrenda
from app.models.prenda import Prenda as PrendaDB
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


async def procesar_cambio(db: AsyncSession, cambio_in, id_usuario: int) -> dict:
    # Buscar variante que sale (la que devuelve el cliente y vuelve al stock)
    result_sale = await db.execute(select(StockPrenda).where(StockPrenda.id_stock_prenda == cambio_in.id_stock_prenda_sale))
    variante_sale = result_sale.scalar_one_or_none()

    if not variante_sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La variante con ID {cambio_in.id_stock_prenda_sale} no existe."
        )

    # Buscar variante que entra (la que se lleva el cliente y sale del stock)
    result_entra = await db.execute(select(StockPrenda).where(StockPrenda.id_stock_prenda == cambio_in.id_stock_prenda_entra))
    variante_entra = result_entra.scalar_one_or_none()

    if not variante_entra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La variante con ID {cambio_in.id_stock_prenda_entra} no existe."
        )

    if variante_entra.stock_actual < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sin stock disponible para la variante ID {cambio_in.id_stock_prenda_entra}."
        )

    # Buscar nombres de prendas padre
    result_prenda_sale = await db.execute(select(PrendaDB).where(PrendaDB.id_prenda == variante_sale.id_prenda))
    prenda_sale = result_prenda_sale.scalar_one_or_none()

    result_prenda_entra = await db.execute(select(PrendaDB).where(PrendaDB.id_prenda == variante_entra.id_prenda))
    prenda_entra = result_prenda_entra.scalar_one_or_none()

    nombre_devuelta = f"{prenda_sale.nombre} (talle {variante_sale.talle})" if prenda_sale else f"Variante ID {variante_sale.id_stock_prenda}"
    nombre_entregada = f"{prenda_entra.nombre} (talle {variante_entra.talle})" if prenda_entra else f"Variante ID {variante_entra.id_stock_prenda}"

    # Actualizar stock
    variante_sale.stock_actual += 1   # Devuelve prenda -> reingresa al inventario
    variante_entra.stock_actual -= 1  # Lleva prenda nueva -> descuenta del inventario

    # Calcular diferencia de precio (positivo: cliente abona diferencia, negativo: a favor del cliente)
    diferencia = variante_entra.precio_venta - variante_sale.precio_venta

    await db.commit()

    return {
        "mensaje": "Cambio de prenda registrado exitosamente.",
        "prenda_devuelta": nombre_devuelta,
        "prenda_entregada": nombre_entregada,
        "diferencia_precio": diferencia,
    }