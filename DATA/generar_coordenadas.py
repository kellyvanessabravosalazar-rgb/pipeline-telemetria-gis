import csv
from pathlib import Path

CARPETA_DATOS = Path(__file__).parent
ARCHIVO_ENTRADA = CARPETA_DATOS / "coordenadas_cruces.csv"
ARCHIVO_SALIDA = CARPETA_DATOS / "coordenadas_cruces_simuladas.csv"

# Coordenadas aproximadas de referencia para simular puntos
# en distintas zonas de Cali. No representan cruces verificados.
REFERENCIAS_COMUNA = {
    "2": (3.4660, -76.5220),
    "7": (3.4440, -76.5000),
    "8": (3.4450, -76.5050),
    "9": (3.4450, -76.5290),
}

with open(ARCHIVO_ENTRADA, "r", encoding="utf-8-sig", newline="") as archivo:
    cruces = list(csv.DictReader(archivo))

columnas = list(cruces[0].keys()) + ["tipo_coordenada"]

for numero, cruce in enumerate(cruces):
    if cruce["latitud"].strip() and cruce["longitud"].strip():
        cruce["tipo_coordenada"] = "VERIFICADA_PENDIENTE_REVISION"
        continue

    lat_base, lon_base = REFERENCIAS_COMUNA.get(
        cruce["comuna"], (3.4516, -76.5320)
    )

    # Pequeñas variaciones para distinguir los puntos simulados.
    desplazamiento = numero * 0.001

    cruce["latitud"] = f"{lat_base + desplazamiento:.7f}"
    cruce["longitud"] = f"{lon_base + desplazamiento:.7f}"
    cruce["origen_coordenadas"] = "Simulacion"
    cruce["tipo_coordenada"] = "SIMULADA"

with open(ARCHIVO_SALIDA, "w", encoding="utf-8", newline="") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(cruces)

print(f"Archivo creado: {ARCHIVO_SALIDA.name}")
print(f"Total de cruces: {len(cruces)}")
print(f"Archivo original conservado: {ARCHIVO_ENTRADA.name}")