# Back End Developer Scraper Challenge

_Por David Laguna Parra_

Repositorio con las soluciones a las 2 tareas del challenge.

## Estructura de Archivos

Los archivos son los siguientes:

-   .gitignore
    -   Contiene los archivos a ignorar en Git
-   api.py
    -   El punto de entrada de la app, una API que contiene 3 endpoints:
        1. `GET /health` para revisar que el servicio esté funcionando
        1. `GET /task-1` ejecuta la Tarea 1
        1. `POST /task-2?url="http://..."` ejecuta la Tarea 2, requiere de una URL como un parámetro de llamada
-   app_log.log
    -   Contiene los logs de la aplicación, se crea si no existe
-   Dockerfile
    -   La Dockerfile con los detalles de la imagen
-   logger_config.py
    -   Contiene la configuración del `logger` usado en la app
-   requirements.txt
    -   Archivo con todas las dependencias de la app
-   task_1_query_config.py
    -   Archivo de configuración que contiene los valores dinámicos de la información a buscar
-   task_1.py
    -   Archivo con la implementación de la tarea 1
-   task_2_xpaths.py
    -   Archivo de configuración que contiene valores XPath dinámicos de la información a buscar y elementos web a manipular
-   task_2.py
    -   Archivo con la implementación de la tarea 2

## Tarea 1

Genera un script en Python que obtenga y de formato a las siguientes
propiedades de un archivo JSON:

-   allergens
-   sku
-   vegan,
-   kosher,
-   organic,
-   vegetarian,
-   gluten_free,
-   lactose_free,
-   package_quantity,
-   Unit_size,
-   net_weight

### Ejecución

Con Docker

1. En consola, navegar al directorio raíz del proyecto y ejecutar el siguiente comando: `docker build -t scraper-api-img .`
1. Ejecutar el siguiente comando para correr la app en un contenedor: `docker run -d -p 8080:8080 --name scraper-api-cnt scraper-api-img`
1. Con un cliente para llamadas a APIs como Postman o un navegador, solicitar la URL: `http://127.0.0.1:8080/task-1`
1. Esperar a obtener el resultado en JSON

Sin Docker

1. En una consola en el directorio raíz del proyecto ejecutar `pip install requirements.txt`
1. Ejecutar `api.py` en la consola
1. Con un cliente para llamadas a APIs como Postman o un navegador, solicitar la URL: `http://127.0.0.1:8080/task-1`
1. Esperar a obtener el resultado en JSON

### Notas

-   En varios casos el JSON original tiene valores numéricos como cadenas de texto, utilizo la función `numeric_cast()` y expresiones regulares para poder transformar el texto a int o float según sea el caso. Implementé el paso de transformación para igualar los valores numéricos a los valores del JSON esperado, pero este paso de limpieza podría dejarse para otro procesamiento futuro y concentrarse en extraer la información cruda solamente.

## Tarea 2

Genera una API en python con un servicio que tenga la capacidad de recibir
una URL como parámetro de entrada (POST) y extraer los primeros 15
productos. Incluye un Dockerfile.

### Ejecución

Con Docker

1. En consola, navegar al directorio raíz del proyecto y ejecutar el siguiente comando: `docker build -t scraper-api-img .`
1. Ejecutar el siguiente comando para correr la app en un contenedor: `docker run -d -p 8080:8080 --name scraper-api-cnt scraper-api-img`
1. Con un cliente para llamadas a APIs como Postman o un navegador, solicitar la URL: `http://127.0.0.1:8080/task-2?url=URL_A_PROBAR`
   Reemplazar `URL_A_PROBAR` con alguna de las siguientes URLs: - https://www.tiendasjumbo.co/supermercado/despensa/enlatados-y-conservas - https://www.tiendasjumbo.co/supermercado/despensa/harinas-y-mezclas-para-preparar - https://www.tiendasjumbo.co/supermercado/despensa/bebida-achocolatada-en-polvo - https://www.tiendasjumbo.co/supermercado/despensa/aceite
1. Esperar a obtener el resultado en JSON

Sin Docker

1. En una consola en el directorio raíz del proyecto ejecutar `pip install requirements.txt`
1. Ejecutar `api.py` en la consola
1. Con un cliente para llamadas a APIs como Postman o un navegador, solicitar la URL: `http://127.0.0.1:8080/task-2?url=URL_A_PROBAR`
   Reemplazar `URL_A_PROBAR` con alguna de las siguientes URLs: - https://www.tiendasjumbo.co/supermercado/despensa/enlatados-y-conservas - https://www.tiendasjumbo.co/supermercado/despensa/harinas-y-mezclas-para-preparar - https://www.tiendasjumbo.co/supermercado/despensa/bebida-achocolatada-en-polvo - https://www.tiendasjumbo.co/supermercado/despensa/aceite
1. Esperar a obtener el resultado en JSON

### Notas

-   Se utiliza `selenium` por que el sitio no maneja paginación en la URL, siendo necesario una manera de poder "presionar el botón de siguiente" y obtener el siguiente set de resultados.
    -   Es posible poder utilizar la API de Tiendas Jumbo directamente para extraer la información, pero requeriría de ingeniería inversa del sitio trazando sus peticiones y la API a la cual el sitio solicita su información.
-   Si bien existen muchos tipos de selectores de elementos HTML, `XPath` fue escogido por su poder de búsqueda, amplia gama de selectores y legibilidad.
-   La extracción puede ser lenta principalmente por los tiempos del carga del sitio, ya que la UI tarda un poco en "hidratarse" cargando los productos.
    -   La velocidad de carga puede afectarse por que la implementación hace un zoom del 10% a la página para cargar todos los productos de la página, en caso contrario se necesitaría lógica compleja de JS para hacer scroll en el sitio, ya que los productos son cargados dinamicamente conforme el usuario haga scroll en el sitio.
-   Existen casos donde hay productos con varios precios de oferta/descuento, la implementación retorna solamente el precio más bajo.
