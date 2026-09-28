from fastapi import FastAPI
from pydantic import BaseModel


class GPSData(BaseModel):
    latitud: float
    longitud: float


app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "Mi primer pipeline funciona"}


@app.post("/gps")
def recibir_gps(datos: GPSData):
    return datos