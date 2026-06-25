from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

# Importamos los modelos ORM de la base de datos
from app.models.prenda import Prenda
from app.models.stock import StockPrenda
# Importamos el esquema de validación Pydantic
from app.schemas.prenda import PrendaCreate


async def create_prenda_completa(db: AsyncSession, prenda_in: PrendaCreate) -> Prenda:
    # 1. Instanciar el modelo principal (Padre)
    nueva_prenda = Prenda(
        nombre=prenda_in.nombre,
        categoria=prenda_in.categoria,
        tipo_tela=prenda_in.tipo_tela,
        activo=True
    )

    # 2. Iterar e instanciar los hijos (StockPrenda)
    for variante_in in prenda_in.variantes:
        nueva_variante = StockPrenda(
            talle=variante_in.talle,
            codigo_barras=variante_in.codigo_barras,
            precio_venta=variante_in.precio_venta,
            stock_actual=variante_in.stock_actual,
            stock_minimo=variante_in.stock_minimo
        )
        nueva_prenda.variantes.append(nueva_variante)

    # 3. Guardar en la sesión y confirmar la transacción
    db.add(nueva_prenda)
    await db.commit()

    # 🚀 REEMPLAZO DE DB.REFRESH POR SELECTINLOAD:
    # Hacemos un select explícito precargando las variantes para que Pydantic no explote
    query = (
        select(Prenda)
        .where(Prenda.id_prenda == nueva_prenda.id_prenda)
        .options(selectinload(Prenda.variantes))
    )
    result = await db.execute(query)

    # Devolvemos el objeto completamente cargado
    return result.scalar_one()


async def get_prenda_by_id(db: AsyncSession, id_prenda: int) -> Optional[Prenda]:
    """
    Recupera una prenda específica de la base de datos a través de su ID.
    Usa selectinload para precargar todas sus variantes en una sola ronda de consultas.
    """
    query = (
        select(Prenda)
        .where(Prenda.id_prenda == id_prenda)
        .options(selectinload(Prenda.variantes))
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_variantes_bajo_stock(db: AsyncSession) -> List[StockPrenda]:
    """
    Consulta todas las variantes de prendas cuyo inventario físico sea menor o igual
    al umbral mínimo configurado. Trae la relación del padre para identificar el nombre de la prenda.
    """
    query = (
        select(StockPrenda)
        .where(StockPrenda.stock_actual <= StockPrenda.stock_minimo)
        .options(selectinload(StockPrenda.prenda))  # Carga la información de la prenda padre
    )
    result = await db.execute(query)
    return list(result.scalars().all())