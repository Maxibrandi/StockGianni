from datetime import datetime, time
from fastapi import APIRouter, Depends, Query
from app.schemas.reporte import ReporteEstadisticoResponse
from app.repositories.reporte_repo import ReporteRepository
from sqlalchemy.ext.asyncio import AsyncSession  # <-- AGREGA ESTA LÍNEA
from app.core.database import get_db

router = APIRouter(prefix="/reportes", tags=["Reportes/Estadísticas"])
reporte_repo = ReporteRepository()


@router.get("/", response_model=ReporteEstadisticoResponse, summary="Reporte general de ventas")
async def obtener_reporte(
        fecha_desde: datetime = Query(..., description="Fecha inicial del reporte"),
        fecha_hasta: datetime = Query(..., description="Fecha final del reporte"),
        db: AsyncSession = Depends(get_db)
):
    # Forzamos las horas para abarcar los días completos (00:00:00 hasta las 23:59:59)
    desde = datetime.combine(fecha_desde.date(), time.min)
    hasta = datetime.combine(fecha_hasta.date(), time.max)

    return await reporte_repo.obtain_metricas_periodo(db=db, desde=desde, hasta=hasta)