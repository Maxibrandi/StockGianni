import asyncio
from decimal import Decimal
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.usuario import Usuario, RolUsuario
from app.models.prenda import Prenda
from app.models.stock import StockPrenda


async def seed_data():
    # 🛠️ ESTO CREA LAS TABLAS (usuario, prenda, stock, etc.) SI NO EXISTEN
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("📋 Tablas verificadas / creadas con éxito.")

    async with SessionLocal() as db:
        # 1. GENERAR / ACTUALIZAR USUARIOS SEMILLA
        res_admin = await db.execute(select(Usuario).where(Usuario.email == "admin@gianni.com"))
        admin = res_admin.scalar_one_or_none()
        if not admin:
            admin = Usuario(
                nombre="Máximo Admin",
                email="admin@gianni.com",
                password_hash=get_password_hash("admin123"),
                rol=RolUsuario.ADMINISTRADOR,
                activo=True
            )
            db.add(admin)
            print("🌱 Usuario Admin creado con éxito.")
        else:
            admin.password_hash = get_password_hash("admin123")
            admin.rol = RolUsuario.ADMINISTRADOR
            admin.activo = True

        res_vendedor = await db.execute(select(Usuario).where(Usuario.email == "ventas@gianni.com"))
        vendedor = res_vendedor.scalar_one_or_none()
        if not vendedor:
            vendedor = Usuario(
                nombre="Empleado Gianni",
                email="ventas@gianni.com",
                password_hash=get_password_hash("ventas123"),
                rol=RolUsuario.VENDEDOR,
                activo=True
            )
            db.add(vendedor)
            print("🌱 Usuario Vendedor creado con éxito.")
        else:
            vendedor.password_hash = get_password_hash("ventas123")
            vendedor.rol = RolUsuario.VENDEDOR
            vendedor.activo = True

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