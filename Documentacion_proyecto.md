# Documentacion del proyecto:

## Historia de Usuario:
        
    1) Creacion de Usuarios:
            -El administrador es el unico que puede crear usuarios, asiganando el rol de "Vendedor" 
            o de "Administrador" para delegar responsabilidades y proteger informacion.
            -El administrador debe ingresar: Usuario, contraseña y rol.
            -No puede haber dos usuario con el mismo Nombre de usuario.
            -Las contraseñas no deben ser visibles en la base de datos.
    
    2) CRUD de stock:
            -Registrar, modificar, y dar de baja prendas detallando, talle, tipo de tela y precios
            diferenciados.
            -Catalogo de stock actualizado.
            -Al ingresar una prenda debe permitir ingresar multiples talles, y asociar precios segun
            el talle/tela de ser necesario.
            -Debe incluir el campo "Stock minimo" por talle.
        
    3) Alerta de Stock Minimo:
            -Recibir notificaciones visuales de cuando un articulo alcance el stock minimo definido.
            -Reponer la mercaderia a tiempo y evitar faltantes.
            -Debe detallar la prenda, el talle y la cantidad actual.
        
    4) Generacion de codigo de barras:    
            -El administrador debe generar codigos de barras únicos para cada prenda y talle,
            para poder etiquetar la mercaderia eficientemente.
            -El sistema debe crear un código descargable e imprimible en pdf.
        
    5) Baja de Stock por venta o cambio:
            -Registrar la salida de una prenda mediante la lectura del codigo de barras o de forma manual
            -Concretar venta o cambio y actualizar el stock en tiempo real.
            -Se debe poder seleccionar venta o cambio.
            -Al concretarse, el stock se actualiza indemediatamente.
        
    6) Busqueda de stock:
            -El vendedor puede buscar prendas porm categoria, tipo de tela, o nombre especifico.
            -Responder rapidamente a las consultas de disponibilidad.
            -Si el producto no existe o no tenga stock, el sistema debe mostrar un mensaje claro.
        
    7) Analisis de venta:
            -El administrador debe poder visualizar reportes de venta diaria, mensuales y anuales.
            -El administrador puede ver la rotacion de la mercaderia.


## Casos de uso:
    1) Registrar salida de mercaderia:
        -El vendedor escanea el codigo de barras de la etiqueta de la prenda, el sistema notifica el 
        producto talle, precio y lo muestra en pantalla.
        El vendero selecciona el tipo de operacion y hace click en "confirmar". El sistema descuenta 
        la unidad del inventario, registra la transaccion y actualiza los datos en tiempo real.
    
    2) Alerta de stock minimo:
        -Se realiza por venta o cambio un descuento de stock de una prenda. El sistema ceifica el stock
        actual, al cumplirse la condicion, el sistema genera una notificacion.
        Muestra una alerta visual y una notificacion en el la seccion faltantes.
        
    3) Reporte de Venta:
        -El administrador ingresa a "Reportes", selecciona el filtro de tiempo: Diario, Mensual o Anual
        el sistema procesa las ventas registradas en el periodo de tiempo seleccionado.

    4) Carga de stock:
        -El adminnistrador puede cargar el stock, seleccionando categoria, talle, tipo de tela,
        precio de compra, precio de venta, stock actual, stock minimo para la alerta y codigo de barras,
        si no tiene seleccionado, se le generara automaticamente
    
    5) Modificar Stock:
        -El administrador puede modificar el stock, la cantidad, los precios e inhabilitar el producto
        de ser necesario

## Diagrama de Actividades
    Carriles:
        .Vendedor: Acciones manuales y de interfaz (escanear, buscar y seleccionar)
        .Sistema: Procesa datos, valida stock, genera alertas y actualiza la base de datos
        .Administrador: Recibe notificacion de falta de stock, administra el stock
    
    Paso a paso:
        -El vendedor busca el producto, elige si escanear, a traves del codigo de barras
        o buscar manualmente por nombre, talle, tela o categoria.
        -El sistema busca coincidencia, si no existe, vuelve al punto de busqueda y notifica.
        Si existe, muestra el producto con sus talles y precios en pantalla
        -El vendedor selecciona si es Venta o Cambio y confirma la transaccion.
        -El sistema descuenta la unidad. Actualiza de inmedianto la pantalla y evalua si hay que
        notificar faltan
        