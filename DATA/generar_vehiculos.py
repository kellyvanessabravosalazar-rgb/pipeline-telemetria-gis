
import csv
import random
from pathlib import Path

CARPETA_DATOS = Path(__file__).parent
ARCHIVO_ENTRADA = CARPETA_DATOS / "vehiculos.csv"
ARCHIVO_SALIDA = CARPETA_DATOS / "vehiculos_simulados.csv"

random.seed(42)

tipos_vehiculo = {
    "bus": (0.30, 0.45),
    "taxi": (0.07, 0.12),
    "motocicleta": (0.025, 0.05),
    "automovil": (0.06, 0.11),
}

with open(ARCHIVO_ENTRADA, "r", encoding="utf-8-sig", newline="") as archivo:
    vehiculos = list(csv.DictReader(archivo))

ids_existentes = {v["vehiculo_id"] for v in vehiculos}

for numero in range(1, 101):
    vehiculo_id = f"VEH_{numero:03d}"

    if vehiculo_id in ids_existentes:
        continue

    tipo = random.choice(list(tipos_vehiculo.keys()))
    consumo_min, consumo_max = tipos_vehiculo[tipo]

    vehiculos.append({
        "vehiculo_id": vehiculo_id,
        "tipo_vehiculo": tipo,
        "combustible_inicial": str(random.randint(20, 100)),
        "consumo_litros_km": str(round(random.uniform(consumo_min, consumo_max), 3)),
    })

with open(ARCHIVO_SALIDA, "w", encoding="utf-8", newline="") as archivo:
    columnas = [
        "vehiculo_id",
        "tipo_vehiculo",
        "combustible_inicial",
        "consumo_litros_km",
    ]
    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(vehiculos)

print("Archivo creado:", ARCHIVO_SALIDA.name)
print("Total de vehículos:", len(vehiculos))
print("Tipos de vehículo:", {
    tipo: sum(v["tipo_vehiculo"] == tipo for v in vehiculos)
    for tipo in tipos_vehiculo
})