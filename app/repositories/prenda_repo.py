from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

# Importamos los modelos ORM de la base de datos
from app.models.prenda import Prenda
from app.models.stock import StockPrenda
from app.schemas.prenda import PrendaUpdate
# Importamos el esquema de validación Pydantic
from app.schemas.prenda import PrendaCreate

#Codigo de barras
import io
from barcode import Code128
from barcode.writer import ImageWriter

#Pdfs
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image as RLImage, Spacer
from reportlab.lib import colors



async def create_prenda_completa(self, db: AsyncSession, prenda_in: PrendaCreate) -> Prenda:
    # 1. Instanciar el modelo principal (Padre)
    nueva_prenda = Prenda(
        nombre=prenda_in.nombre,
        categoria=prenda_in.categoria,
        tipo_tela=prenda_in.tipo_tela,
        activo=True
    )

    # 2. Iterar e instanciar los hijos (StockPrenda)
    for variante_in in prenda_in.variantes:

        # --- AQUÍ LÓGICA DE AUTOGENERACIÓN ---
        # Si el código viene vacío o None desde el frontend, le inventamos uno único por talle
        cod_barras = variante_in.codigo_barras
        if not cod_barras:
            cod_barras = "".join([str(random.randint(0, 9)) for _ in range(12)])

        nueva_variante = StockPrenda(
            talle=variante_in.talle,
            codigo_barras=cod_barras,  # <--- Usamos el código verificado/generado
            precio_venta=variante_in.precio_venta,
            stock_actual=variante_in.stock_actual,
            stock_minimo=variante_in.stock_minimo
        )
        nueva_prenda.variantes.append(nueva_variante)

    # 3. Guardar en la sesión y confirmar la transacción
    db.add(nueva_prenda)
    await db.commit()

    # 🚀 REEMPLAZO DE DB.REFRESH POR SELECTINLOAD:
    query = (
        select(Prenda)
        .where(Prenda.id_prenda == nueva_prenda.id_prenda)
        .options(selectinload(Prenda.variantes))
    )
    result = await db.execute(query)

    return result.scalar_one()


# --- NUEVO MÉTODO DE BÚSQUEDA ---
async def get_prenda_by_codigo_barras(self, db: AsyncSession, codigo_barras: str) -> Prenda | None:
    """
    Busca la prenda completa haciendo un JOIN por el código de barras de su variante (hijo).
    """
    query = (
        select(Prenda)
        .join(Prenda.variantes)  # Conectamos con StockPrenda
        .where(StockPrenda.codigo_barras == codigo_barras)
        .options(selectinload(Prenda.variantes))  # Precargamos todos los talles para el frontend
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


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


class PrendaRepository:
    async def update(self, db: AsyncSession, id_prenda: int, prenda_update: PrendaUpdate):
        # 1. Buscamos la prenda cargando explícitamente sus variantes de forma asíncrona
        query = (
            select(Prenda)
            .where(Prenda.id_prenda == id_prenda)
            .options(selectinload(Prenda.variantes))  # <-- Esto evita el MissingGreenlet
        )
        result = await db.execute(query)
        db_prenda = result.scalar_one_or_none()

        if not db_prenda:
            return None

        # 2. Actualizamos los campos
        update_data = prenda_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_prenda, key, value)

        # 3. Guardamos los cambios
        await db.commit()
        await db.refresh(db_prenda, attribute_names=["variantes"])  # <-- Refrescamos incluyendo la relación

        return db_prenda

    async def get_prenda_by_codigo_barras(self, db: AsyncSession, codigo_barras: str) -> Prenda | None:        # Buscamos la prenda por código e incluimos sus variantes (talles/stock)
        query = (
            select(PrendaDB)
            .where(PrendaDB.codigo_barras == codigo_barras)
            .options(selectinload(PrendaDB.variantes))
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def generar_pdf_codigos(self, db: AsyncSession, id_prenda: int) -> io.BytesIO:
        """
        Genera un PDF en memoria con las etiquetas de código de barras de todas las variantes.
        """
        prenda = await self.get_prenda_by_id(db=db, id_prenda=id_prenda)
        if not prenda:
            return None

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        story = []

        data_tabla = []
        fila_actual = []

        for variante in prenda.variantes:
            # 1. Generar la imagen del código de barras en memoria
            fp = io.BytesIO()
            # Usamos Code128 que es excelente para texto/números compactos
            barcode_obj = Code128(variante.codigo_barras, writer=ImageWriter())
            barcode_obj.write(fp, options={"write_text": False, "module_height": 5.0})
            fp.seek(0)

            # 2. Construir la etiqueta visual
            img_barcode = RLImage(fp, width=140, height=45)

            # Celda de la etiqueta: Nombre + Talle + Código Barras + Texto del Código
            celda = [
                f"{prenda.nombre}",
                f"Talle: {variante.talle}",
                img_barcode,
                f"*{variante.codigo_barras}*"
            ]

            # Armamos una cuadrícula de 3 columnas de etiquetas por fila
            fila_actual.append(celda)
            if len(fila_actual) == 3:
                data_tabla.append(fila_actual)
                fila_actual = []

        if fila_actual:  # Si quedaron etiquetas colgadas
            while len(fila_actual) < 3:
                fila_actual.append("")
            data_tabla.append(fila_actual)

        # 3. Darle estilo de cuadrícula de etiquetas al PDF
        tabla = Table(data_tabla, colWidths=[180, 180, 180])
        tabla.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),  # Guía de corte temporal
            ('BOX', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))

        story.append(tabla)
        doc.build(story)
        buffer.seek(0)
        return buffer