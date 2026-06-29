import asyncio
from decimal import Decimal
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import SessionLocal, Base, engine  # <-- Asegúrate de importar Base y engine
from app.models.usuario import Usuario
from app.models.prenda import Prenda
from app.models.stock import StockPrenda


async def seed_data():
    # 🛠️ ESTO CREA LAS TABLAS (usuario, prenda, stock, etc.) SI NO EXISTEN
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("📋 Tablas verificadas / creadas con éxito.")

    async with SessionLocal() as db:
        # 1. GENERAR USUARIOS SEMILLA
        result_usuarios = await db.execute(select(Usuario).limit(1))
        if result_usuarios.scalar_one_or_none() is None:
            print("🌱 Creando usuarios de ejemplo...")

            admin = Usuario(
                nombre="Máximo Admin",
                email="admin@gianni.com",
                password_hash="admin123",
                rol="ADMINISTRADOR",  # 🔄 CAMBIADO A MAYÚSCULAS para que coincida con 'VENDEDOR'
                activo=True
            )

            vendedor = Usuario(
                nombre="Empleado Gianni",
                email="ventas@gianni.com",
                password_hash="ventas123",
                rol="VENDEDOR",  # <-- Mantenemos en mayúsculas como figuraba en tu log
                activo=True
            )

            db.add(admin)
            db.add(vendedor)
            print("🌱 Usuarios insertados con éxito.")

        # 2. GENERAR PRENDAS SEMILLA
        result_prendas = await db.execute(select(Prenda).limit(1))
        if result_prendas.scalar_one_or_none() is None:
            print("🌱 Base de datos sin prendas. Generando stock de ejemplo...")

            camisa = Prenda(nombre="Camisa Rayada", categoria="Camisas", tipo_tela="Algodón", activo=True)
            camisa.variantes.append(
                StockPrenda(talle="M", codigo_barras="111111111111", precio_venta=Decimal("25000.00"), stock_actual=15,
                            stock_minimo=5))
            camisa.variantes.append(
                StockPrenda(talle="L", codigo_barras="222222222222", precio_venta=Decimal("25000.00"), stock_actual=3,
                            stock_minimo=5))

            pantalon = Prenda(nombre="Jeans Slim Fit", categoria="Pantalones", tipo_tela="Denim", activo=True)
            pantalon.variantes.append(
                StockPrenda(talle="42", codigo_barras="333333333333", precio_venta=Decimal("38000.00"), stock_actual=20,
                            stock_minimo=5))

            db.add(camisa)
            db.add(pantalon)
            print("🌱 Prendas e inventario insertados con éxito.")

        await db.commit()