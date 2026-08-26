from datetime import datetime, time, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.reporte import ReporteEstadisticoResponse, ResumenGananciasResponse
from app.repositories.reporte_repo import ReporteRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter(prefix="/reportes", tags=["Reportes/Estadísticas"])
reporte_repo = ReporteRepository()


@router.get("/resumen", response_model=ResumenGananciasResponse, summary="Resumen de ganancias diarias y mensuales")
@router.get("/reporte-ganancias", response_model=ResumenGananciasResponse, summary="Alias: Resumen de ganancias")
async def obtener_resumen_ganancias(
    db: AsyncSession = Depends(get_db)
):
    return await reporte_repo.get_resumen_ganancias(db=db)


@router.get("/", response_model=ReporteEstadisticoResponse, summary="Reporte general de ventas")
async def obtener_reporte(
        fecha_desde: Optional[datetime] = Query(None, description="Fecha inicial del reporte"),
        fecha_hasta: Optional[datetime] = Query(None, description="Fecha final del reporte"),
        db: AsyncSession = Depends(get_db)
):
    ahora = datetime.now()
    if not fecha_desde:
        fecha_desde = ahora - timedelta(days=30)
    if not fecha_hasta:
        fecha_hasta = ahora

    desde = datetime.combine(fecha_desde.date(), time.min)
    hasta = datetime.combine(fecha_hasta.date(), time.max)

    return await reporte_repo.obtain_metricas_periodo(db=db, desde=desde, hasta=hasta)