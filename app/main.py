# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="Stock Gianni API")

# Definir orígenes permitidos
origins = [
    "http://localhost:5173",          # Entorno local Vite
    "http://localhost:3000",
    "https://gianni-ferro.vercel.app", # Frontend en Vercel
]

# Si tienes FRONTEND_URL configurada en settings, la agregamos dinámicamente
if hasattr(settings, "FRONTEND_URL") and settings.FRONTEND_URL:
    origins.append(settings.FRONTEND_URL.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)