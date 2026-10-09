Pipeline de telemetría vehicular con análisis espacial

Este proyecto se desarrolló como una prueba técnica para aplicar herramientas de programación y análisis espacial al estudio de la movilidad urbana. Para el ejercicio tomé como referencia la ciudad de Cali y trabajé con datos de movilidad urbana relacionados con cruces viales y accidentalidad, tomando como referencia la información publicada en el portal de datos abiertos de la Alcaldía de Santiago de Cali.

A partir de esta información, preparé datos y recorridos simulados de vehículos para construir un pipeline de telemetría que permite registrar posiciones GPS, consultar geocercas y generar alertas relacionadas con la velocidad y el combustible. La idea fue integrar la información territorial de Cali con herramientas de programación y bases de datos espaciales para explorar cómo se pueden organizar, consultar y analizar estos datos desde una perspectiva geográfica.

Tecnologías utilizadas
Python
FastAPI
PostgreSQL y PostGIS
SQL
QGIS
Pytest
Git y GitHub
¿Qué hace el proyecto?

El pipeline está organizado en tres partes:

Bronze: recibe y almacena los reportes simulados de los vehículos, incluyendo su identificador, fecha, ubicación, velocidad y nivel de combustible.
Silver: permite revisar si los vehículos se encuentran dentro de una geocerca, comparar su velocidad con el límite establecido para la zona y calcular alertas de combustible según la distancia que les queda por recorrer.
Gold: reúne la información procesada en vistas de PostgreSQL para facilitar las consultas y su visualización en un mapa.

El componente territorial toma como referencia información de Cali relacionada con cruces viales y calles con mayor accidentalidad. Estos datos permiten explorar la distribución espacial de elementos asociados a la movilidad urbana y sirven como base para el ejercicio cartográfico.

También se implementó el enmascaramiento de los identificadores de los vehículos en las respuestas destinadas a usuarios no administradores. Esta funcionalidad es demostrativa y no reemplaza un sistema real de autenticación.

Estructura del proyecto
main.py: contiene la API desarrollada con FastAPI.
services/: reúne las funciones para consultar información de los vehículos y calcular su autonomía.
tests/: contiene las pruebas automatizadas de las funciones principales.
DATA/: incluye los archivos y scripts utilizados para preparar la información territorial, los cruces viales, las rutas y los vehículos simulados.
sql/esquema.sql: contiene la estructura de las tablas, los índices y las vistas de la base de datos.
DESIGN.md: explica cómo está organizado el proyecto y las decisiones técnicas que se tomaron.
SETUP.md: contiene los pasos para instalar y configurar el entorno.
telemetria_cali.qgz: es el proyecto cartográfico elaborado en QGIS.
Mapa_Telemetria_Cali.pdf: contiene el mapa exportado desde QGIS.
Requisitos

Para ejecutar el proyecto se necesita Python, Git, PostgreSQL con PostGIS y las dependencias de Python incluidas en requirements.txt. También se utiliza QGIS para abrir y consultar el proyecto cartográfico.

Instalación y ejecución

Para ponerlo en funcionamiento hay que clonar el repositorio, crear un entorno virtual, instalar las dependencias y configurar la base de datos con PostgreSQL y PostGIS. También es necesario crear un archivo .env local con los datos de conexión a la base de datos.

En el archivo SETUP.md están los pasos detallados para realizar la configuración.

Una vez preparado el entorno, la API se puede iniciar desde la carpeta principal con:

python -m uvicorn main:app --reload

La documentación interactiva de los endpoints queda disponible en:

http://127.0.0.1:8000/docs

Pruebas

El proyecto incluye pruebas para comprobar el funcionamiento de las geocercas, los cálculos de autonomía y las consultas de información de los vehículos.

Para ejecutarlas se utiliza:

python -m pytest -v

En la última ejecución local, las ocho pruebas incluidas finalizaron correctamente.

Datos y limitaciones

La información territorial de Cali se utiliza como referencia para el análisis espacial de cruces viales y accidentalidad. Como fuente de referencia se encuentra el portal de datos abiertos de la Alcaldía de Santiago de Cali.

Los reportes GPS y los recorridos de los vehículos utilizados en las pruebas son simulados y no corresponden a recorridos reales. Los cálculos de combustible se basan en capacidades de tanque y consumos definidos para la simulación.

Además, el parámetro de administrador de la API se utiliza únicamente para demostrar el enmascaramiento de identificadores; no constituye un mecanismo real de control de acceso.

Documentación adicional
Diseño del proyecto
Instalación y configuración
Esquema SQL