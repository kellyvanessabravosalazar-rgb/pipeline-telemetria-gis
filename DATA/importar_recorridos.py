import csv
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

CARPETA_DATOS = Path(__file__).parent
ARCHIVO_CSV = CARPETA_DATOS / "recorridos_simulados.csv"

load_dotenv(CARPETA_DATOS.parent / ".env")
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("No se encontró DATABASE_URL en el archivo .env")

with open(ARCHIVO_CSV, "r", encoding="utf-8-sig", newline="") as archivo:
    registros = list(csv.DictReader(archivo))

insertados = 0
omitidos = 0

with psycopg.connect(DATABASE_URL) as conexion:
    with conexion.cursor() as cursor:
        for registro in registros:
            cursor.execute(
                """
                INSERT INTO telemetry (
                    vehicle_id,
                    report_time,
                    latitude,
                    longitude,
                    speed_kmh,
                    fuel_pct,
                    geom
                )
                SELECT
                    %s,
                    %s::timestamp,
                    %s,
                    %s,
                    %s,
                    %s,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM telemetry
                    WHERE vehicle_id = %s
                      AND report_time = %s::timestamp
                )
                """,
                (
                    registro["vehiculo_id"],
                    registro["fecha_hora"],
                    float(registro["latitud"]),
                    float(registro["longitud"]),
                    float(registro["velocidad_kmh"]),
                    float(registro["combustible_pct"]),
                    float(registro["longitud"]),
                    float(registro["latitud"]),
                    registro["vehiculo_id"],
                    registro["fecha_hora"],
                ),
            )

            if cursor.rowcount == 1:
                insertados += 1
            else:
                omitidos += 1

print("Registros leídos:", len(registros))
print("Registros nuevos importados:", insertados)
print("Registros omitidos por existir:", omitidos)