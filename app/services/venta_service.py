from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

# Importación de los modelos ORM
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.models.stock import StockPrenda
# Importación de los esquemas de validación Pydantic
from app.schemas.venta import VentaCreate


async def procesar_venta(db: AsyncSession, venta_in: VentaCreate, id_usuario: int) -> Venta:
    """
    Registra una venta de indumentaria reduciendo de manera sincrónica el inventario,
    calculando el monto total y asegurando la persistencia de precios históricos.

    Todo se ejecuta bajo una misma transacción atómica (All-or-Nothing).
    """
    # 1. Instanciar la cabecera de la venta (el total se calculará dinámicamente)
    nueva_venta = Venta(
        id_usuario=id_usuario,
        total=Decimal("0.00")
    )

    acumulador_total = Decimal("0.00")
    detalles_a_crear = []

    # 2. Iterar sobre cada uno de los productos que envía el vendedor
    for item in venta_in.productos:
        # Consultar la variante física de stock actual en la base de datos
        query_stock = select(StockPrenda).where(StockPrenda.id_stock_prenda == item.id_stock_prenda)
        result_stock = await db.execute(query_stock)
        variante_stock = result_stock.scalar_one_or_none()

        # Validación de existencia del producto
        if not variante_stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La variante de producto con ID {item.id_stock_prenda} no existe."
            )

        # Regla de Negocio: Validación estricta de disponibilidad en el inventario
        if variante_stock.stock_actual < item.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para la variante ID {item.id_stock_prenda}. "
                       f"Disponibles: {variante_stock.stock_actual}, Solicitados: {item.cantidad}."
            )

        # 3. Lógica de Inventario: Descontar las unidades despachadas
        variante_stock.stock_actual -= item.cantidad

        # 4. Lógica Financiera: Multiplicar cantidad por el precio actual de catálogo y acumular
        subtotal_item = variante_stock.precio_venta * item.cantidad
        acumulador_total += subtotal_item

        # 5. Instanciar la línea de detalle congelando el precio unitario histórico
        nuevo_detalle = DetalleVenta(
            id_stock_prenda=item.id_stock_prenda,
            cantidad=item.cantidad,
            precio_unitario=variante_stock.precio_venta  # Resguardo histórico anti-modificaciones futuras
        )
        detalles_a_crear.append(nuevo_detalle)

    # 6. Asignar los valores calculados a la entidad padre
    nueva_venta.total = acumulador_total
    nueva_venta.detalles = detalles_a_crear

    # 7. Guardar cambios en la base de datos y confirmar la transacción
    db.add(nueva_venta)
    await db.commit()

    # 8. Carga anticipada (Eager Loading) mediante selectinload para el retorno del JSON
    query_final = (
        select(Venta)
        .where(Venta.id_venta == nueva_venta.id_venta)
        .options(selectinload(Venta.detalles))
    )
    result_final = await db.execute(query_final)
    return result_final.scalar_one()