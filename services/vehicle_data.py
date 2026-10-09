import csv
from pathlib import Path


RUTA_VEHICULOS = (
    Path(__file__).resolve().parent.parent
    / "DATA"
    / "vehiculos_simulados.csv"
)


def obtener_datos_vehiculo(vehicle_id):
    """Busca el tipo y el consumo de un vehículo en el CSV."""
    with RUTA_VEHICULOS.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            if fila["vehiculo_id"] == vehicle_id:
                return {
                    "tipo_vehiculo": fila["tipo_vehiculo"].strip().lower(),
                    "consumo_litros_km": float(
                        fila["consumo_litros_km"]
                    ),
                }

    return None
