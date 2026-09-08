import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configuración y base de datos
from app.core.config import settings
from app.core.database import engine, Base
from app.seed import seed_data

# Importación de Routers
from app.api.v1.auth import router as auth_router
from app.api.v1.prendas import router as prendas_router
from app.api.v1.ventas import router as ventas_router
from app.api.v1.reportes import router as reportes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando la aplicacion FastAPI y sincronizando tablas con PostgreSQL...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        await seed_data()
    except Exception as e:
        print(f"Error al ejecutar el seed (o los datos ya existen): {e}")
    yield


app = FastAPI(
    title="Sistema de Gestión de Inventario - Tienda de Ropa",
    version="1.0.0",
    description="API transaccional para el control de stock, alertas de reposición y facturación.",
    lifespan=lifespan
)

# Configuración de CORS
origins = [
    "http://localhost:5173",            # Vite local
    "http://127.0.0.1:5173",
    "https://gianni-ferro.vercel.app",  # Frontend en Vercel
]

if hasattr(settings, "FRONTEND_URL") and settings.FRONTEND_URL:
    clean_url = settings.FRONTEND_URL.rstrip("/")
    if clean_url not in origins:
        origins.append(clean_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🌟 REGISTRO DE RUTAS (Faltaba en main.py)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(prendas_router, prefix="/api/v1/prendas", tags=["Catálogo y Stock"])
app.include_router(ventas_router, prefix="/api/v1/ventas", tags=["Transacciones y Ventas"])
app.include_router(reportes_router, prefix="/api/v1", tags=["Reportes"])


@app.get("/", tags=["Root"])
async def root():
    return {"message": "API del Sistema de Inventario operando con éxito"}

@app.get("/health")
def health():
    return {"status": "ok"}