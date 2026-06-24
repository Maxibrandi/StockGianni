from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. IMPORTAR tus enrutadores desde la capa de controladores
from app.api.v1.auth import router as auth_router
from app.api.v1.prendas import router as prendas_router
from app.api.v1.ventas import router as ventas_router
app = FastAPI(
    title="Sistema de Gestión de Inventario - Tienda de Ropa",
    version="1.0.0",
    description="API transaccional para el control de stock, alertas de reposición y facturación."
)

# Configuración de CORS (opcional, útil para cuando conectemos Vue.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. REGISTRAR los enrutadores definiendo sus prefijos y etiquetas (tags)
# Esto es lo que lee el OpenAPI/Swagger para generar la especificación.

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


@app.get("/", tags=["Root"])
async def root():
    return {"message": "API del Sistema de Inventario operando con éxito"}