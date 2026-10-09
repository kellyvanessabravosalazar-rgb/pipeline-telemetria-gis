Instalación y ejecución del proyecto
1. Requisitos

Para trabajar con el proyecto se necesitan las siguientes herramientas:

Python: para ejecutar la API y las funciones del pipeline.
PostgreSQL: para almacenar los registros de telemetría.
PostGIS: para trabajar con las coordenadas y realizar consultas espaciales.
Git: para descargar el repositorio y llevar el control de los cambios.
Visual Studio Code (VS Code): para revisar y modificar el código y ejecutar los comandos desde la terminal.
pgAdmin 4: para conectarse a PostgreSQL, ejecutar consultas SQL y revisar las tablas, vistas e índices.
QGIS: para abrir el proyecto cartográfico y consultar los datos en el mapa.

Los pasos de esta guía están pensados para Windows y PowerShell.

2. Descargar y preparar el proyecto

Primero se debe descargar el repositorio y abrir la carpeta del proyecto en VS Code.

Desde una terminal de PowerShell se ejecutan los siguientes comandos, reemplazando URL_DEL_REPOSITORIO por la dirección real del repositorio:

git clone URL_DEL_REPOSITORIO
cd P_PYTHON
code .

Después, se crea un entorno virtual para instalar las dependencias del proyecto sin mezclarlas con las de otras aplicaciones:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Con el entorno virtual activado, se instalan las dependencias registradas en requirements.txt:

python -m pip install -r requirements.txt

Si PowerShell no permite activar el entorno virtual por las restricciones de ejecución, se puede habilitar temporalmente para la sesión actual con:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
3. Configurar la base de datos desde pgAdmin 4

El proyecto utiliza PostgreSQL para guardar los registros de telemetría y PostGIS para realizar las operaciones espaciales.

Primero se debe abrir pgAdmin 4 y conectarse al servidor PostgreSQL. Desde allí se puede crear la base de datos que se utilizará para ejecutar el proyecto.

Una vez creada, se selecciona la base de datos y se abre el Query Tool para ejecutar las instrucciones SQL necesarias.

Para habilitar PostGIS, se utiliza:

CREATE EXTENSION IF NOT EXISTS postgis;

La base de datos debe contar con las tablas de telemetría y geocercas, además de las vistas utilizadas para clasificar las alertas y consultar los datos desde QGIS.

Para reproducir la estructura completa en otro equipo, también se deben incluir y ejecutar los scripts SQL que crean las tablas, vistas e índices. Si se quieren obtener los mismos resultados de prueba, será necesario cargar los datos simulados correspondientes.

4. Configurar la conexión con PostgreSQL

La aplicación se conecta a PostgreSQL mediante la variable DATABASE_URL, que se configura en el archivo .env, ubicado en la carpeta principal del proyecto.

Esta variable contiene los datos necesarios para establecer la conexión con la base de datos. Debe configurarse de acuerdo con el servidor y las credenciales del equipo donde se ejecute la aplicación.

El archivo .env se debe mantener local y no publicarse en GitHub, ya que puede contener información sensible. Para facilitar la configuración en otros equipos, se puede incluir un archivo .env.example sin contraseñas reales.

5. Ejecutar la API desde VS Code

Una vez configuradas las dependencias y la conexión a la base de datos, se abre la terminal integrada de VS Code y se activa el entorno virtual.

Para iniciar el servidor se ejecuta:

python -m uvicorn main:app --reload

Si el servidor inicia correctamente, la API estará disponible en:

http://127.0.0.1:8000

Para consultar los endpoints y probar las solicitudes se puede abrir la documentación interactiva de FastAPI:

http://127.0.0.1:8000/docs

Desde esta página se puede probar la recepción de registros GPS y la consulta que evalúa si el combustible disponible alcanza para cubrir la distancia restante de una ruta.

La opción --reload permite que el servidor se reinicie automáticamente cuando se guardan cambios en el código durante el desarrollo.

6. Ejecutar las pruebas

El proyecto incluye pruebas automatizadas para comprobar el funcionamiento de las funciones implementadas.

Desde la terminal de VS Code, con el entorno virtual activado, se ejecuta:

python -m pytest -v

En la terminal aparecerá el resultado de cada prueba. Si todas pasan correctamente, se mostrará el resumen de las pruebas ejecutadas sin errores.

Estas pruebas permiten revisar la lógica de los cálculos predictivos y otras funciones auxiliares del proyecto.

7. Consultar los datos desde pgAdmin 4

pgAdmin 4 también permite revisar los resultados que se van almacenando en la base de datos y comprobar las consultas utilizadas en el pipeline.

Desde el Query Tool se pueden ejecutar consultas SQL para contar los registros, identificar los vehículos registrados y revisar las alertas de velocidad y combustible.

Durante las comprobaciones del proyecto se obtuvieron los siguientes resultados:

1.073 registros de telemetría.
119 vehículos distintos.
75 registros clasificados como exceso de velocidad.
17 alertas de combustible.

Estos resultados corresponden a los datos simulados cargados en la base de datos y pueden variar si se agregan nuevos registros.

8. Abrir el mapa en QGIS

Para consultar la representación cartográfica se debe abrir QGIS y seleccionar el archivo telemetria_cali.qgz, incluido en el proyecto.

El mapa utiliza la información espacial almacenada en PostgreSQL para representar los registros y sus clasificaciones. Si se abre desde otro equipo, será necesario configurar una conexión a la base de datos y comprobar que las capas puedan acceder a las vistas correspondientes.

También se incluye el archivo Mapa_Telemetria_Cali.pdf, que contiene una exportación del mapa y permite consultar el resultado cartográfico sin abrir QGIS.

9. Datos y seguridad

Los datos utilizados durante el desarrollo son simulados, por lo que los resultados no corresponden a mediciones reales de vehículos ni representan necesariamente las condiciones del tráfico de Cali.

Antes de publicar el repositorio se debe comprobar que no incluya contraseñas, archivos .env ni otros datos que deban mantenerse privados.

También se implementó un enmascaramiento del identificador del vehículo en las respuestas destinadas a usuarios no administradores. Esta funcionalidad es una demostración para la prueba técnica y no reemplaza un sistema de autenticación y autorización. Para utilizar la aplicación en un entorno real sería necesario implementar controles de acceso adecuados.

10. Archivos principales del proyecto

Entre los archivos y carpetas utilizados se encuentran:

main.py: contiene la API y sus endpoints.
services/: contiene funciones auxiliares para los cálculos predictivos, la configuración de vehículos y la consulta de sus datos.
tests/: contiene las pruebas automatizadas.
DATA/: contiene los datos simulados utilizados por el proyecto.
requirements.txt: registra las dependencias de Python.
.env: contiene la configuración local de la conexión a la base de datos y no debe publicarse.
telemetria_cali.qgz: contiene el proyecto cartográfico de QGIS.
Mapa_Telemetria_Cali.pdf: contiene la exportación cartográfica.
DESIGN.md: describe la organización del pipeline y las decisiones de diseño.
SETUP.md: explica cómo preparar y ejecutar el proyecto.

Esta estructura permite identificar dónde se encuentra la API, dónde están las funciones de procesamiento, cómo se realizan las pruebas y qué archivos se utilizan para la visualización de los datos.