import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

CARPETA_DATOS = Path(__file__).parent
ARCHIVO_VEHICULOS = CARPETA_DATOS / "vehiculos_simulados.csv"
ARCHIVO_SALIDA = CARPETA_DATOS / "recorridos_simulados.csv"

random.seed(42)

# Zona aproximada de Cali para generar datos de prueba.
LATITUD_BASE = 3.4516
LONGITUD_BASE = -76.5320

with open(ARCHIVO_VEHICULOS, "r", encoding="utf-8-sig", newline="") as archivo:
    vehiculos = list(csv.DictReader(archivo))

registros = []
inicio = datetime(2026, 10, 8, 8, 0, 0)

for vehiculo in vehiculos:
    latitud = LATITUD_BASE + random.uniform(-0.015, 0.015)
    longitud = LONGITUD_BASE + random.uniform(-0.015, 0.015)
    combustible = float(vehiculo["combustible_inicial"])

    for paso in range(10):
        fecha_hora = inicio + timedelta(seconds=paso * 60)

        velocidad = round(random.uniform(5, 60), 1)
        latitud += random.uniform(-0.001, 0.001)
        longitud += random.uniform(-0.001, 0.001)

        consumo = float(vehiculo["consumo_litros_km"])
        distancia_km = velocidad / 60
        combustible = max(0, combustible - consumo * distancia_km)

        registros.append({
            "vehiculo_id": vehiculo["vehiculo_id"],
            "fecha_hora": fecha_hora.isoformat(),
            "latitud": round(latitud, 7),
            "longitud": round(longitud, 7),
            "velocidad_kmh": velocidad,
            "combustible_pct": round(combustible, 2),
            "origen": "Simulado",
        })

with open(ARCHIVO_SALIDA, "w", encoding="utf-8", newline="") as archivo:
    columnas = [
        "vehiculo_id",
        "fecha_hora",
        "latitud",
        "longitud",
        "velocidad_kmh",
        "combustible_pct",
        "origen",
    ]
    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(registros)

print("Archivo creado:", ARCHIVO_SALIDA.name)
print("Vehículos:", len(vehiculos))
print("Registros GPS:", len(registros))
print("Origen de los datos: Simulado")