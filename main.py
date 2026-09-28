from datetime import datetime

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import os


load_dotenv()

app = FastAPI()


class GPSData(BaseModel):
    vehicle_id: str
    timestamp: datetime
    latitud: float
    longitud: float
    velocidad: float
    combustible: float


def guardar_gps(datos):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute(
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
            VALUES (
                %s, %s, %s, %s, %s, %s,
                ST_SetSRID(
                    ST_MakePoint(%s, %s),
                    4326
                )
            )
            """,
            (
                datos.vehicle_id,
                datos.timestamp,
                datos.latitud,
                datos.longitud,
                datos.velocidad,
                datos.combustible,
                datos.longitud,
                datos.latitud,
            ),
        )

    conn.commit()
    conn.close()


@app.get("/")
def inicio():
    return {"mensaje": "Pipeline GIS funcionando"}


@app.post("/gps")
def recibir_gps(datos: GPSData):
    guardar_gps(datos)

    return {
        "mensaje": "Datos GPS almacenados correctamente",
        "vehicle_id": datos.vehicle_id,
        "latitud": datos.latitud,
        "longitud": datos.longitud,
    }