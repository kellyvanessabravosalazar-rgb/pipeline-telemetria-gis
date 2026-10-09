Diseño del pipeline de telemetría GIS
1. ¿Qué busca hacer el proyecto?

Este proyecto busca construir un pipeline para trabajar con datos de telemetría vehicular. La idea es recibir información de los vehículos, almacenarla en una base de datos, analizar su ubicación y generar alertas que permitan identificar situaciones como excesos de velocidad o posibles problemas de autonomía por combustible.

Para desarrollarlo se utilizaron Python, FastAPI, PostgreSQL, PostGIS y QGIS. Los datos empleados son simulados y permiten probar el funcionamiento de la solución sin utilizar información real de vehículos.

2. Organización del pipeline

El proceso se organizó en tres etapas: Bronze, Silver y Gold. Cada una cumple una función dentro del tratamiento de los datos.

Bronze: recepción y almacenamiento de los datos

En esta primera etapa se reciben los reportes GPS mediante una API construida con FastAPI. Cada reporte contiene el identificador del vehículo, la fecha y hora, las coordenadas geográficas, la velocidad y el porcentaje de combustible.

Después de recibir la información, los datos se guardan en PostgreSQL. Para poder trabajar con la ubicación de los vehículos se utiliza PostGIS, que permite almacenar las coordenadas como geometrías y realizar consultas espaciales.

Silver: análisis espacial y generación de alertas

En esta etapa se relacionan los puntos GPS con las geocercas definidas en la base de datos. Para ello se utilizan consultas espaciales de PostGIS que permiten identificar si un registro se encuentra dentro de una zona o fuera de ella.

También se compara la velocidad registrada con el límite establecido para cada geocerca. A partir de esta comparación se clasifican los registros según presenten exceso de velocidad, se encuentren dentro del límite o estén fuera de una geocerca.

Por otra parte, se desarrolló un módulo para evaluar la autonomía de combustible. Este utiliza el porcentaje de combustible registrado, el tipo de vehículo, su consumo estimado y la distancia restante de la ruta para calcular si el combustible disponible sería suficiente.

Gold: consolidación y visualización

En la última etapa se utiliza la vista mapa_telemetria, que reúne los registros y sus clasificaciones para facilitar su consulta y representación cartográfica.

Esta información se puede visualizar en QGIS, lo que permite revisar la distribución espacial de los registros y distinguir las situaciones identificadas durante el procesamiento.

3. Tecnologías utilizadas
Python: desarrollo de la lógica del proyecto y de las funciones de cálculo.
FastAPI: recepción de los reportes GPS y consulta de la predicción de autonomía.
PostgreSQL: almacenamiento y consulta de los registros.
PostGIS: manejo de geometrías y análisis espacial mediante geocercas.
QGIS: elaboración y consulta de la representación cartográfica.
Pytest: ejecución de pruebas para comprobar el funcionamiento de las funciones implementadas.
Git: control de versiones del proyecto.
4. Consultas espaciales y rendimiento

La tabla de telemetría cuenta con un índice GiST sobre el campo geométrico. Este tipo de índice permite mejorar el rendimiento de determinadas consultas espaciales, especialmente cuando aumenta la cantidad de registros.

Si el volumen de datos llegara a crecer hasta millones de registros, sería necesario evaluar el rendimiento de las consultas con EXPLAIN ANALYZE, revisar los índices utilizados y considerar otras estrategias, como la partición temporal de la tabla o el procesamiento por lotes.

Estas mejoras dependerían del volumen de información, la frecuencia con la que llegan los reportes y el tipo de consultas que se realicen.

5. Protección de los identificadores

Para las respuestas destinadas a usuarios no administradores se implementó el enmascaramiento del identificador del vehículo. De esta manera, la respuesta no muestra directamente el identificador original.

Esta medida es una aproximación para la prueba técnica y no reemplaza un sistema real de autenticación y autorización. En una implementación de producción sería necesario validar los permisos de cada usuario desde el servidor y evitar que el acceso administrativo dependa únicamente de un parámetro de consulta.

6. Comprobaciones realizadas

Durante las pruebas de la base de datos se verificaron 1.073 registros de telemetría correspondientes a 119 vehículos. En la consulta de alertas se identificaron 75 registros clasificados como exceso de velocidad y 17 alertas de combustible.

Además, se ejecutaron pruebas automatizadas para revisar los cálculos predictivos y las funciones auxiliares del proyecto.

Los resultados corresponden a la simulación desarrollada y no representan mediciones reales del tráfico de Cali.

7. Aspectos por mejorar

El proyecto permite probar el flujo de recepción, almacenamiento, análisis y consulta de los datos. Sin embargo, todavía hay aspectos que podrían ampliarse.

Entre ellos están la implementación de autenticación real, el cálculo automático de rutas y distancias, las pruebas de rendimiento con mayores volúmenes de información y la incorporación de un mapa de calor para identificar concentraciones espaciales de eventos.

También sería conveniente ampliar las pruebas para cubrir diferentes tipos de vehículos, geocercas y condiciones de operación.