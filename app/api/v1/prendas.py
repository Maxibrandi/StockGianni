from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.usuario import Usuario

# --- CAPA SCHEMAS (Pydantic para validaciones de API) ---
from app.schemas.prenda import PrendaCreate, PrendaResponse, StockPrendaResponse, PrendaUpdate

# --- CAPA MODELS (SQLAlchemy para Base de Datos) ---
from app.models.prenda import Prenda as PrendaDB  # Le ponemos alias para que no choque

# --- CAPA REPOSITORIES ---
from app.repositories.prenda_repo import PrendaRepository

router = APIRouter()
prenda_repo = PrendaRepository()


@router.post(
    "/",
    response_model=PrendaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Dar de alta una nueva prenda con variantes de talle"
)
async def registrar_prenda(
    prenda_in: PrendaCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: Usuario = Depends(get_current_admin)
):
    return await prenda_repo.create_prenda_completa(db=db, prenda_in=prenda_in)


# =========================================================================
# ENDPOINT Estático: Alertas de Reposición (DEBE IR ANTES DE LA RUTA DINÁMICA)
# =========================================================================
@router.get(
    "/alertas/reposicion",
    response_model=List[StockPrendaResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar variantes de prendas con stock crítico",
    description="Devuelve de forma prioritaria un listado con todas las prendas y talles "
                "específicos que alcanzaron el stock mínimo para coordinar la reposición."
)
async def obtener_alertas_reposicion(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cualquier empleado autenticado en el sistema (Vendedor o Administrador)
    puede acceder en tiempo real a este reporte desde su puesto de trabajo.
    """
    alertas = await prenda_repo.get_variantes_bajo_stock(db=db)
    return alertas


# =========================================================================
# ENDPOINT Dinámico: Ver Detalle de Prenda
# =========================================================================
@router.get(
    "/{id_prenda}",
    response_model=PrendaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener el detalle y stock de una prenda específica"
)
async def obtener_prenda(
    id_prenda: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    prenda = await prenda_repo.get_prenda_by_id(db=db, id_prenda=id_prenda)
    if not prenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La prenda con ID {id_prenda} no fue encontrada en el catálogo maestro."
        )
    return prenda


# Ejemplo en tu ruta de listado:
@router.get("/", response_model=List[PrendaResponse])
async def listar_prendas(
        offset: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    # Cambiamos Prenda por PrendaDB aquí inside select y selectinload
    query = select(PrendaDB).offset(offset).limit(limit).options(selectinload(PrendaDB.variantes))

    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/{id_prenda}", response_model=PrendaResponse, status_code=status.HTTP_200_OK)
async def modificar_prenda(
        id_prenda: int,
        prenda_in: PrendaUpdate,
        db: AsyncSession = Depends(get_db)
):
    """
    Modifica los datos de una prenda existente (Nombre y/o Precio).
    """
    prenda_actualizada = await prenda_repo.update(db=db, id_prenda=id_prenda, prenda_update=prenda_in)

    if not prenda_actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la prenda con ID {id_prenda}"
        )

    return prenda_actualizada