# Webscraping backend

Herramientas utilizadas:

- Selenium
- BeatifylSoup
- DB Mongo
- Framework FastAPI

## Resumen

La clase Judicatura utiliza Selenium y BeautifulSoup para realizar web scraping, interactuar con elementos de la página web, extraer datos y almacenarlos en una base de datos. También maneja errores y reintentos en caso de fallos en la obtención de datos.

- Estructura del documento en la colección:

```json
{
    _id: ObjectId('6472c8ceb787c1428581f60f'),
    documento: '0968599020001',
    fecha_creacion: '2023-05-27 22:21:50',
    procesos: [
        [
            {
                'No.': '1',
                'Fecha de ingreso': '02/05/2023',
                'No. proceso': '23303202300348G',
                'Acción/Infracción': 'ARCHIVO DE LA INVESTIGACIÓN PREVIA ART. 586',
                detalle: {
                    movimientos: {
                        'No.': '1',
                        Fecha: '02/05/2023 10:28',
                        'Actores/ Ofendidos': 'Tapia Torres Albaro Augusto, Empresa Electrica Publica Estrategica Corporacion Nacional De Electricidad Cnel Ep, Fiscalia General Del Estado',
                        'Demandados/ Procesados': '',
                        'Actuaciones Judiciales': 'folder_open'
                    }
                }
            },
        ]
    ]
}
```

- Documento almacenado en la colección:

![Visual Datos en MongoDB](/docs/img/img_005.png)

## Endpoints - FastAPI

![Endpoints](/docs/img/img_001.png)

/store-information/: Este endpoint es una ruta GET que muestra todos los identificadores de la información extraída almacenada. Llama a la función get_store_ids() del módulo db_judicatura para obtener los IDs almacenados y los devuelve como respuesta.

![Endpoints - Store Information](/docs/img/img_002.png)

/extracted-information/{document_id}: Este endpoint es una ruta GET que muestra la información extraída por su ID. Recibe el parámetro document_id que representa el ID del documento y llama a la función search_document_by_id() del módulo db_judicatura para buscar y obtener la información extraída correspondiente al ID proporcionado. Devuelve la información extraída como respuesta.

![Endpoints - Extracted Information](/docs/img/img_003.png)

/search: Este endpoint es una ruta POST que realiza una consulta por documento. Recibe los datos de búsqueda en el cuerpo de la solicitud como un objeto de tipo SearchRequest y ejecuta la función write_notification() en segundo plano utilizando BackgroundTasks. La función write_notification() crea una instancia de la clase Judicatura y llama al método search() para realizar la búsqueda de la información relacionada con el documento proporcionado. Retorna un mensaje indicando que la solicitud se recibió correctamente.

![Endpoints - Search](/docs/img/img_004.png)

## Ejecutar

A continuación se describe el proceso para correr el programa:

1. Verificar la versión de Python: Asegúrate de tener instalada una versión reciente de Python, preferiblemente la versión 3.9. Verificar la versión instalada ejecutando el siguiente comando en la línea de comandos:

```shell
python --version
```

2. Copiar el archivo template.env y crear el archivo .env: hay un archivo llamado template.env que contiene variables de entorno de ejemplo. Realizar una copia de este archivo y crear uno nuevo llamado .env.

- Encuentra el archivo template.env.
- Copia el archivo y pégalo en la misma ubicación con el nombre .env.
- Actualiza los datos correspondientes.

3. Crear un entorno virtual: Es recomendable crear un entorno virtual para aislar las dependencias del proyecto. Proceso para crear un entorno virtual:

- Abrir la línea de comandos en la ubicación deseada.
- Ejecuta el siguiente comando para crear un entorno virtual llamado "venv":

```shell
python -m venv venv
```

4. Activar el entorno virtual:

- En la línea de comandos, ejecutar el siguiente comando según tu sistema operativo:
  - En Windows:

```shell
venv\Scripts\activate.bat
```

- En macOS/Linux:

```shell
source venv/bin/activate
```

5. Instalar las dependencias:

```shell
pip install -r requirements.txt
```

6. Ejecutar el programa: Ejecuta el siguiente comando para iniciar el servidor:

```shell
python main.py
```

Esto iniciará el servidor FastAPI y mostrará información sobre el servidor en la línea de comandos.

7. URL - Ingrese a la ruta:

Una vez que el servidor esté en funcionamiento, se podrá acceder a las rutas definidas usando el navegador web o utilizando herramientas como cURL o Postman para enviar solicitudes HTTP a las rutas correspondientes.

Para visualizar la documentación interactica del proyecto ingresar a la ruta desde el navegador:

[localhost:8000](http://localhost:8000)

8. Deterner el servidor:

Presionar Ctrl+C en la línea de comandos donde se está ejecutando.
