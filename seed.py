import asyncio
import sys
from decimal import Decimal

# IMPORTACIÓN AJUSTADA: Traemos SessionLocal de tu archivo real y le asignamos el alias
from app.core.database import SessionLocal as async_session_maker, engine, Base

# Importamos los modelos ORM de la aplicación
from app.models.usuario import Usuario
from app.models.prenda import Prenda
from app.models.stock import StockPrenda

# Importamos la función utilitaria para encriptar contraseñas
from app.core.security import get_password_hash


async def main():
    print("Iniciando la inserción de datos de prueba (Seed)...")

    # NUEVO: Esto le dice a SQLAlchemy que cree las tablas en PostgreSQL si no existen
    print("Creando tablas en la base de datos si no existen...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # El resto de tu código continúa exactamente igual:
    async with async_session_maker() as db:
        try:
            print("Generando usuarios con roles diferenciados...")

            password_comun = "Password123*"
            hash_seguro = get_password_hash(password_comun)

            admin_user = Usuario(
                nombre="Administrador General",
                email="admin@local.com",
                password_hash=hash_seguro,
                rol="administrador",
                activo=True
            )

            vendedor_user = Usuario(
                nombre="Vendedor Principal",
                email="vendedor@local.com",
                password_hash=hash_seguro,
                rol="vendedor",
                activo=True
            )

            db.add_all([admin_user, vendedor_user])

            # 2. CREACIÓN DE PRENDA MAESTRA Y SUS VARIANTES ANIDADAS
            print("Generando catálogo inicial de indumentaria y variantes de stock...")

            prenda_maestra = Prenda(
                nombre="Camisa Oxford",
                categoria="Superior",
                tipo_tela="Algodón Premium",
                activo=True
            )

            # Variante M: Stock saludable para procesar ventas con éxito
            variante_m = StockPrenda(
                talle="M",
                codigo_barras="7791234567891",
                precio_venta=Decimal("45000.00"),
                stock_actual=15,
                stock_minimo=3
            )

            # Variante L: Stock crítico para validar de inmediato el endpoint de alertas
            variante_l = StockPrenda(
                talle="L",
                codigo_barras="7791234567892",
                precio_venta=Decimal("47500.00"),
                stock_actual=2,  # Menor al mínimo, disparará alerta de reposición
                stock_minimo=5
            )

            # Asociamos las variantes de talle a la lista del modelo padre
            prenda_maestra.variantes.append(variante_m)
            prenda_maestra.variantes.append(variante_l)

            db.add(prenda_maestra)

            # 3. TRANSACCIÓN ATÓMICA: Confirmamos todos los datos en PostgreSQL
            await db.commit()
            print("¡Base de datos poblada con éxito de forma segura!")
            print("\nCredenciales de prueba disponibles:")
            print("  - Admin:    admin@local.com    / Contraseña: Password123*")
            print("  - Vendedor: vendedor@local.com / Contraseña: Password123*")
            print("Artículos cargados:")
            print("  - Camisa Oxford (Talle M - Stock: 15 / Talle L - Stock: 2 [ALERTA])")

        except Exception as e:
            # En caso de error, hacemos rollback inmediato para mantener la integridad
            await db.rollback()
            print(f"Error crítico durante el seeding: {e}", file=sys.stderr)
            raise e


if __name__ == "__main__":
    # Ejecución del bucle de eventos asíncronos nativo de Python
    asyncio.run(main())