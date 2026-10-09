import csv
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

CARPETA_DATOS = Path(__file__).parent
ARCHIVO_ENTRADA = CARPETA_DATOS / "cruces_cali.csv"
ARCHIVO_SALIDA = CARPETA_DATOS / "cruces_geocodificados.csv"

def geocodificar(direccion):
    
direccion_limpia = direccion.upper()
direccion_limpia = direccion_limpia.replace("CL ", "Calle ")
direccion_limpia = direccion_limpia.replace(" AV ", " Avenida ")
direccion_limpia = direccion_limpia.replace(" KR ", " Carrera ")
direccion_limpia = direccion_limpia.replace(" CR ", " Carrera ")
direccion_limpia = direccion_limpia.replace(" X ", " con ")
direccion_limpia = direccion_limpia.replace(" Y ", " y ")

consulta = f"{direccion_limpia}, Cali, Valle del Cauca, Colombia"

    parametros = urlencode({
        "q": consulta,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "co",
    })

    url = f"https://nominatim.openstreetmap.org/search?{parametros}"

    solicitud = Request(
        url,
        headers={
            "User-Agent": "ProyectoAcademicoGISCali/1.0"
        },
    )

    with urlopen(solicitud, timeout=30) as respuesta:
        resultados = json.loads(respuesta.read().decode("utf-8"))

    if not resultados:
        return "", "", "", "SIN_RESULTADO"

    resultado = resultados[0]

    return (
        resultado["lat"],
        resultado["lon"],
        resultado.get("display_name", ""),
        "REVISAR_RESULTADO",
    )


with open(
    ARCHIVO_ENTRADA, "r", encoding="utf-8-sig", newline=""
) as archivo:
    cruces = list(csv.DictReader(archivo))

resultados = []

for numero, cruce in enumerate(cruces):
    direccion = cruce["direccion"].strip()

    print(f"Consultando {numero + 1}/{len(cruces)}: {direccion}")

    try:
        latitud, longitud, coincidencia, estado = geocodificar(direccion)
    except Exception as error:
        latitud, longitud, coincidencia = "", "", ""
        estado = f"ERROR: {type(error).__name__}"

    resultados.append({
        "id": cruce["id"],
        "direccion": direccion,
        "comuna": cruce["comuna"],
        "latitud": latitud,
        "longitud": longitud,
        "direccion_encontrada": coincidencia,
        "estado_geocodificacion": estado,
        "fuente": "OpenStreetMap Nominatim",
    })

    # Guardar el avance después de cada consulta.
    with open(
        ARCHIVO_SALIDA, "w", encoding="utf-8-sig", newline=""
    ) as salida:
        columnas = [
            "id", "direccion", "comuna", "latitud", "longitud",
            "direccion_encontrada", "estado_geocodificacion", "fuente",
        ]
        escritor = csv.DictWriter(salida, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(resultados)

    # Respetar el límite de consultas del servicio.
    if numero < len(cruces) - 1:
        time.sleep(1.1)

print(f"\nProceso terminado. Registros procesados: {len(resultados)}")
print(f"Archivo generado: {ARCHIVO_SALIDA.name}")
print("Las coincidencias deben revisarse antes de usar las coordenadas.")