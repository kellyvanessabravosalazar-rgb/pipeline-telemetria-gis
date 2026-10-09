
import csv
from pathlib import Path

CARPETA_DATOS = Path(__file__).parent

archivos = [
    "cruces_cali.csv",
    "vehiculos.csv",
    "registro_trafico.csv",
    "coordenadas_cruces.csv",
]

for nombre in archivos:
    ruta = CARPETA_DATOS / nombre

    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        filas = list(csv.DictReader(archivo))

    print(f"\nArchivo: {nombre}")
    print(f"Registros encontrados: {len(filas)}")

    if filas:
       columnas = list(filas[0].keys())
    print(f"Columnas: {columnas}")

print("\nRevision de archivos terminada.")