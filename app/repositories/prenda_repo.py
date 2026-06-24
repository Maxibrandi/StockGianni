from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.stock import StockPrenda

# Importamos los modelos ORM de la base de datos
from app.models.prenda import Prenda
from app.models.stock import StockPrenda
# Importamos el esquema de validación Pydantic
from app.schemas.prenda import PrendaCreate


async def create_prenda_completa(db: AsyncSession, prenda_in: PrendaCreate) -> Prenda:
    """
    Crea un artículo maestro de indumentaria junto con todas sus variantes de talle
    y códigos de barra en una única transacción atómica.

    Args:
        db (AsyncSession): Sesión asíncrona de base de datos activa.
        prenda_in (PrendaCreate): Esquema Pydantic anidado con los datos de entrada.

    Returns:
        Prenda: El objeto del modelo Prenda completamente poblado con sus variantes.
    """
    # 1. Instanciar el modelo principal (Padre)
    nueva_prenda = Prenda(
        nombre=prenda_in.nombre,
        categoria=prenda_in.categoria,
        tipo_tela=prenda_in.tipo_tela,
        activo=True
    )

    # 2. Recorrer las variantes del esquema e instanciar los objetos StockPrenda (Hijos)
    # Al añadirlos a la lista .variantes, SQLAlchemy mapea automáticamente las claves foráneas
    for variante_in in prenda_in.variantes:
        nueva_variante = StockPrenda(
            talle=variante_in.talle,
            codigo_barras=variante_in.codigo_barras,
            precio_venta=variante_in.precio_venta,
            stock_actual=variante_in.stock_actual,
            stock_minimo=variante_in.stock_minimo
        )
        nueva_prenda.variantes.append(nueva_variante)

    # 3. Agregar la estructura jerárquica a la sesión y confirmar en PostgreSQL
    db.add(nueva_prenda)
    await db.commit()

    # 4. Solución Pro: Para garantizar que el objeto de retorno contenga las variantes
    # cargadas en memoria sin conflictos asíncronos, realizamos una consulta controlada
    # empleando selectinload justo antes de devolver el resultado.
    query = (
        select(Prenda)
        .where(Prenda.id_prenda == nueva_prenda.id_prenda)
        .options(selectinload(Prenda.variantes))
    )
    result = await db.execute(query)
    return result.scalar_one()


async def get_prenda_by_id(db: AsyncSession, id_prenda: int) -> Optional[Prenda]:
    """
    Recupera del catálogo una prenda específica a través de su ID.
    Usa selectinload para precargar de manera eficiente y asíncrona todas sus
    variantes de talle y stock en una sola ronda de consultas.

    Args:
        db (AsyncSession): Sesión asíncrona de base de datos activa.
        id_prenda (int): Identificador único de la prenda a buscar.

    Returns:
        Prenda | None: La entidad Prenda junto con sus variantes si existe, o None.
    """
    # selectinload ejecuta una segunda consulta optimizada usando un operador IN (id_prenda)
    # lo cual es significativamente más rápido y limpio que un JOIN para relaciones pesadas.
    query = (
        select(Prenda)
        .where(Prenda.id_prenda == id_prenda)
        .options(selectinload(Prenda.variantes))
    )
    result = await db.execute(query)

    return result.scalar_one_or_none()


async def get_variantes_bajo_stock(db: AsyncSession) -> List[StockPrenda]:
    """
    Consulta en la base de datos todas las variantes de prendas cuyo inventario físico
    haya alcanzado o sea menor al umbral mínimo de seguridad configurado.

    Trae anticipadamente la información del catálogo padre para que el reporte sea legible.
    """
    query = (
        select(StockPrenda)
        .where(StockPrenda.stock_actual <= StockPrenda.stock_minimo)
        .options(selectinload(StockPrenda.prenda))
    )
    result = await db.execute(query)

    # Devuelve la lista completa de objetos de stock filtrados
    return result.scalars().all()