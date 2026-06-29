from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.usuario import Usuario
from app.schemas.venta import VentaCreate, VentaResponse
from app.services.venta_service import procesar_venta

router = APIRouter()


@router.post(
    "/",
    response_model=VentaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Procesar y registrar una nueva venta de mercadería",
    description="Recibe un listado de productos con sus respectivas cantidades, valida la disponibilidad de stock, "
                "descuenta las unidades del inventario en tiempo real y calcula el monto total acumulado. "
                "Cualquier empleado autenticado (Vendedor o Administrador) puede realizar esta acción."
)
async def registrar_venta(
        venta_in: VentaCreate,
        db: AsyncSession = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
):

    nueva_venta = await procesar_venta(
        db=db,
        venta_in=venta_in,
        id_usuario=current_user.id_usuario
    )

    return nueva_venta