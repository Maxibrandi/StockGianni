from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.seed import seed_data
from app.models.usuario import Usuario
from app.models.prenda import Prenda
from app.models.stock import StockPrenda
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta

# 1. IMPORTAR tus enrutadores desde la capa de controladores
from app.api.v1.auth import router as auth_router
from app.api.v1.prendas import router as prendas_router
from app.api.v1.ventas import router as ventas_router
from app.api.v1.reportes import router as reportes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta de forma obligatoria apenas enciende el contenedor
    print("🚀 Iniciando la aplicación FastAPI...")
    try:
        await seed_data()
    except Exception as e:
        print(f"❌ Error crítico ejecutando el archivo seed: {e}")
    yield

app = FastAPI(
    title="Sistema de Inventario Gianni",
    lifespan=lifespan
)

app = FastAPI(
    title="Sistema de Gestión de Inventario - Tienda de Ropa",
    version="1.0.0",
    description="API transaccional para el control de stock, alertas de reposición y facturación.",
    lifespan=lifespan  # <-- Conectamos el ciclo de vida aquí
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. REGISTRAR los enrutadores definiendo sus prefijos y etiquetas (tags)
app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Autenticación"]
)

app.include_router(
    prendas_router,
    prefix="/api/v1/prendas",
    tags=["Catálogo y Stock"]
)

app.include_router(
    ventas_router,
    prefix="/api/v1/ventas",
    tags=["Transacciones y Ventas"]
)

app.include_router(
    reportes_router,
    prefix="/api/v1",  # Mantiene tu prefijo base para que use /api/v1/reportes
    tags=["Reportes"]
)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "API del Sistema de Inventario operando con éxito"}