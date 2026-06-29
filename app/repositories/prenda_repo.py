import io
from typing import List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

# Herramientas para la generación de códigos de barra y PDF
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image as RLImage

# Modelos
from app.models.prenda import Prenda
from app.models.stock import StockPrenda

# Esquemas
from app.schemas.prenda import PrendaCreate, PrendaUpdate


class PrendaRepository:

    async def get_prenda_by_id(self, db: AsyncSession, id_prenda: int) -> Optional[Prenda]:
        query = (
            select(Prenda)
            .where(Prenda.id_prenda == id_prenda)
            .options(selectinload(Prenda.variantes))
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_variantes_bajo_stock(self, db: AsyncSession):
        query = (
            select(StockPrenda)
            .options(selectinload(StockPrenda.prenda))
            .where(StockPrenda.stock_actual <= StockPrenda.stock_minimo)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_prenda_by_codigo_barras(self, db: AsyncSession, codigo_barras: str) -> Optional[Prenda]:
        query = (
            select(StockPrenda)
            .where(StockPrenda.codigo_barras == codigo_barras)
            .options(selectinload(StockPrenda.prenda).selectinload(Prenda.variantes))
        )
        result = await db.execute(query)
        variante = result.scalar_one_or_none()

        if variante:
            return variante.prenda
        return None

    async def generar_pdf_codigos(self, db: AsyncSession, id_prenda: int) -> io.BytesIO:
        prenda = await self.get_prenda_by_id(db=db, id_prenda=id_prenda)
        if not prenda or not prenda.variantes:
            return None

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        story = []

        data_tabla = []
        fila_actual = []

        for variante in prenda.variantes:
            fp = io.BytesIO()
            barcode_obj = Code128(variante.codigo_barras, writer=ImageWriter())
            barcode_obj.write(fp, options={"write_text": False, "module_height": 5.0})
            fp.seek(0)

            img_barcode = RLImage(fp, width=140, height=45)

            celda_diseno = Table([
                [f"{prenda.nombre}"],
                [f"Talle: {variante.talle}"],
                [img_barcode],
                [f"*{variante.codigo_barras}*"]
            ], colWidths=[170])

            celda_diseno.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (0, 0), 10),  # Nombre prenda
                ('FONTSIZE', (0, 1), (0, 1), 9),   # Talle
                ('FONTSIZE', (0, 3), (0, 3), 8),   # Texto código
            ]))

            fila_actual.append(celda_diseno)
            if len(fila_actual) == 3:
                data_tabla.append(fila_actual)
                fila_actual = []

        if fila_actual:  # Rellenamos si la última fila quedó incompleta
            while len(fila_actual) < 3:
                fila_actual.append("")
            data_tabla.append(fila_actual)

        # Diseño final de la cuadrícula de etiquetas (con guías de corte ligeras)
        tabla = Table(data_tabla, colWidths=[180, 180, 180])
        tabla.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))

        story.append(tabla)
        doc.build(story)
        buffer.seek(0)
        return buffer

    async def update(self, db: AsyncSession, id_prenda: int, prenda_update: PrendaUpdate):
        query = (
            select(Prenda)
            .where(Prenda.id_prenda == id_prenda)
            .options(selectinload(Prenda.variantes))
        )
        result = await db.execute(query)
        db_prenda = result.scalar_one_or_none()

        if not db_prenda:
            return None

        update_data = prenda_update.model_dump(exclude_unset=True)
        variantes_data = update_data.pop("variantes", None)

        for key, value in update_data.items():
            setattr(db_prenda, key, value)

        if variantes_data:
            for v_data in variantes_data:
                for db_variante in db_prenda.variantes:
                    if db_variante.id_stock_prenda == v_data["id_stock_prenda"]:
                        if "precio_venta" in v_data and v_data["precio_venta"] is not None:
                            db_variante.precio_venta = v_data["precio_venta"]
                        if "stock_actual" in v_data and v_data["stock_actual"] is not None:
                            db_variante.stock_actual = v_data["stock_actual"]
                        if "stock_minimo" in v_data and v_data["stock_minimo"] is not None:
                            db_variante.stock_minimo = v_data["stock_minimo"]

        await db.commit()
        await db.refresh(db_prenda, attribute_names=["variantes"])
        return db_prenda