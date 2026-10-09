from datetime import datetime

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import os
from services.predictive import evaluar_autonomia
from services.vehicle_data import obtener_datos_vehiculo


load_dotenv()

app = FastAPI()
def enmascarar_vehicle_id(vehicle_id: str) -> str:
    return "VHC-****-ABC"

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


@app.post("/gps")
def recibir_gps(datos: GPSData):
    try:
        guardar_gps(datos)
        return {
            "mensaje": "Datos GPS almacenados correctamente",
            "vehicle_id": datos.vehicle_id,
            "latitud": datos.latitud,
            "longitud": datos.longitud,
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar GPS: {type(error).__name__}: {error}",
        )


@app.get("/prediccion/{vehicle_id}")
def predecir_autonomia(
    vehicle_id: str,
    distancia_restante_km: float,
    admin: bool = False,
):

    if distancia_restante_km < 0:
        raise HTTPException(
            status_code=400,
            detail="La distancia restante no puede ser negativa.",
        )

    datos_vehiculo = obtener_datos_vehiculo(vehicle_id)

    if datos_vehiculo is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron datos de consumo para este vehículo.",
        )

    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT fuel_pct
                FROM telemetry
                WHERE vehicle_id = %s
                ORDER BY report_time DESC
                LIMIT 1
                """,
                (vehicle_id,),
            )
            fila = cur.fetchone()
    finally:
        conn.close()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="No hay registros GPS para este vehículo.",
        )

    combustible_pct = fila[0]

    try:
        resultado = evaluar_autonomia(
            combustible_pct=combustible_pct,
            tipo_vehiculo=datos_vehiculo["tipo_vehiculo"],
            distancia_restante_km=distancia_restante_km,
            consumo_por_km=datos_vehiculo["consumo_litros_km"],
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    vehicle_id_respuesta = (
        vehicle_id if admin else enmascarar_vehicle_id(vehicle_id)
    )

    return {
        "vehicle_id": vehicle_id_respuesta,
        "distancia_restante_km": distancia_restante_km,
        **resultado,
    }

    return {
        "vehicle_id": enmascarar_vehicle_id(vehicle_id),
        "distancia_restante_km": distancia_restante_km,
        **resultado,
    }
