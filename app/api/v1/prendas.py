from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.usuario import Usuario
from app.schemas.prenda import PrendaCreate, PrendaResponse, StockPrendaResponse, PrendaUpdate
from app.models.prenda import Prenda as PrendaDB
from app.repositories.prenda_repo import PrendaRepository
from fastapi.responses import StreamingResponse

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
    alertas = await prenda_repo.get_variantes_bajo_stock(db=db)
    return alertas

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


@router.get("/", response_model=List[PrendaResponse])
async def listar_prendas(
        offset: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    query = select(PrendaDB).offset(offset).limit(limit).options(selectinload(PrendaDB.variantes))

    result = await db.execute(query)
    return result.scalars().all()


@router.put("/{id_prenda}", response_model=PrendaResponse)
async def actualizar_prenda(
    id_prenda: int,
    prenda_in: PrendaUpdate, # <-- Aquí recibe las variantes, el precio y stock nuevo
    db: AsyncSession = Depends(get_db)
):
    prenda_actualizada = await prenda_repo.update(db=db, id_prenda=id_prenda, prenda_update=prenda_in)
    if not prenda_actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La prenda que intentas modificar no existe"
        )
    return prenda_actualizada


@router.get(
    "/buscar/codigo",
    response_model=PrendaResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar una prenda mediante el código de barras de una de sus variantes"
)
async def obtener_prenda_por_codigo(
    codigo: str,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    prenda = await prenda_repo.get_prenda_by_codigo_barras(db=db, codigo_barras=codigo)
    if not prenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún producto con el código de barras: {codigo}"
        )
    return prenda



@router.get("/{id_prenda}/pdf-codigos", summary="Descargar PDF con códigos de barras")
async def descargar_pdf_codigos(id_prenda: int, db: AsyncSession = Depends(get_db)):
    pdf_buffer = await prenda_repo.generar_pdf_codigos(db=db, id_prenda=id_prenda)
    if not pdf_buffer:
        raise HTTPException(status_code=404, detail="Prenda no encontrada")

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=codigos_prenda_{id_prenda}.pdf"}
    )