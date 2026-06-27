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
        1)