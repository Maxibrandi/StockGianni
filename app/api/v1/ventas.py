from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# Importamos la dependencia para obtener la sesión de la base de datos
from app.core.database import get_db

# Importamos la dependencia de seguridad para validar el token JWT del empleado
from app.api.deps import get_current_user

# Importamos el modelo ORM de Usuario para el tipado de los parámetros
from app.models.usuario import Usuario

# Importamos los esquemas Pydantic v2 para validación de entrada y formateo de salida
from app.schemas.venta import VentaCreate, VentaResponse

# Importamos la lógica de negocio centralizada en la capa de servicios
from app.services.venta_service import procesar_venta

# Inicializamos el enrutador para el módulo de ventas físicas
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
    """
    Endpoint para la creación de ventas físicas en los puestos de trabajo.

    - **venta_in**: Carrito de compras que contiene la lista de IDs de variantes de stock y sus cantidades.
    - **current_user**: Instancia del usuario autenticado a través del token Bearer JWT de la cabecera.
    """
    # Se delega toda la lógica atómica al servicio, enviando el ID del usuario logueado
    nueva_venta = await procesar_venta(
        db=db,
        venta_in=venta_in,
        id_usuario=current_user.id_usuario
    )

    # Se retorna el modelo ORM Venta, el cual será serializado automáticamente por el response_model
    return nueva_venta