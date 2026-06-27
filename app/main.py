from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. IMPORTAR tus enrutadores desde la capa de controladores
from app.api.v1.auth import router as auth_router
from app.api.v1.prendas import router as prendas_router  # <-- ¡AGREGAMOS ESTA LÍNEA!
from app.api.v1.ventas import router as ventas_router
from app.api.v1.reportes import router as reportes_router


app = FastAPI(
    title="Sistema de Gestión de Inventario - Tienda de Ropa",
    version="1.0.0",
    description="API transaccional para el control de stock, alertas de reposición y facturación."
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

# 💡 NOTA: Eliminamos las líneas repetidas de ventas y reportes que tenías acá abajo
# para evitar rutas duplicadas en tu documentación de Swagger.

@app.get("/", tags=["Root"])
async def root():
    return {"message": "API del Sistema de Inventario operando con éxito"}