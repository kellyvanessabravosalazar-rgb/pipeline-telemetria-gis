from fastapi import FastAPI
from pydantic import BaseModel


class GPSData(BaseModel):
    latitud: float
    longitud: float


def procesar_gps(datos):
    return {
        "latitud": datos.latitud,
        "longitud": datos.longitud,
        "mensaje": "Datos GPS procesados correctamente"
    }


app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "Mi primer pipeline funciona"}


@app.post("/gps")
def recibir_gps(datos: GPSData):
    return procesar_gps(datos)