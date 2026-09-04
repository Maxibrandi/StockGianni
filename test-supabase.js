import sys
import os
import asyncio

# --- ESTO SOLUCIONA EL ERROR DE RUTA ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# ---------------------------------------

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.models.prenda import Prenda
from app.models.stock import StockPrenda
from app.schemas.prenda import PrendaCreate
from app.repositories.prenda_repo import PrendaRepository
Base = declarative_base()

async def probar_repositorio():
    # 1. Configurar base de datos SQLite local asíncrona para la prueba
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    repo = PrendaRepository()

    async with AsyncSessionLocal() as session:
        print("🔄 Probando la creación de una prenda completa...")

        # Simulamos datos de entrada con Pydantic o diccionarios según tu esquema
        # (Ajusta los campos según los atributos reales de tu modelo PrendaCreate)
        datos_prueba = PrendaCreate(
            nombre="Remera Básica StockGianni",
            descripcion="Algodón 100%",
            categoria="Remeras",       # <--- Agrega este campo
            tipo_tela="Algodón",       # <--- Agrega este campo
            precio_base=1500.0,
            variantes=[
                {"talle": "S", "color": "Negro", "stock_actual": 10, "stock_minimo": 2, "precio_venta": 2000.0},
                {"talle": "M", "color": "Negro", "stock_actual": 15, "stock_minimo": 3, "precio_venta": 2000.0}
            ]
        )

        try:
            # 2. Probar creación
            prenda_creada = await repo.create_prenda_completa(db=session, prenda_in=datos_prueba)
            print(f"✅ ¡Prenda creada con éxito! ID: {prenda_creada.id_prenda}")
            print(f"🏷️ Variantes con códigos de barras generados:")
            for v in prenda_creada.variantes:
                print(f"   - Talle {v.talle}: Código -> {v.codigo_barras}")

            # 3. Probar generación de PDF
            print("\n🔄 Probando la generación del PDF de códigos de barras...")
            pdf_buffer = await repo.generar_pdf_codigos(db=session, id_prenda=prenda_creada.id_prenda)

            if pdf_buffer:
                # Guardamos el PDF de prueba en la raíz para verificarlo
                with open("etiquetas_prueba.pdf", "wb") as f:
                    f.write(pdf_buffer.getvalue())
                print("✅ ¡PDF generado y guardado como 'etiquetas_prueba.pdf'! Reumís y verifica el archivo.")
            else:
                print("⚠️ No se pudo generar el PDF (sin variantes).")

        except Exception as e:
            print("❌ Error durante la prueba:", e)

# Ejecutar la prueba asíncrona
if __name__ == "__main__":
    asyncio.run(probar_repositorio())