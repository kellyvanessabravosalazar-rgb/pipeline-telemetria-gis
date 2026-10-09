def calcular_alerta_combustible(
    combustible_actual,
    distancia_restante_km,
    consumo_por_km
):
    combustible_necesario = distancia_restante_km * consumo_por_km

    if combustible_actual <= combustible_necesario:
        return "ALERTA_COMBUSTIBLE"

    return "AUTONOMIA_SUFFICIENTE"


def test_alerta_combustible():
    resultado = calcular_alerta_combustible(
        combustible_actual=5,
        distancia_restante_km=50,
        consumo_por_km=0.1
    )

    assert resultado == "ALERTA_COMBUSTIBLE"


def test_autonomia_suficiente():
    resultado = calcular_alerta_combustible(
        combustible_actual=20,
        distancia_restante_km=50,
        consumo_por_km=0.1
    )

    assert resultado == "AUTONOMIA_SUFFICIENTE"
    
from services.predictive import (
    convertir_porcentaje_a_litros,
    evaluar_autonomia,
)


def test_convertir_porcentaje_a_litros():
    resultado = convertir_porcentaje_a_litros(
        combustible_pct=40,
        tipo_vehiculo="taxi",
    )

    assert resultado == 20.0


def test_autonomia_insuficiente_para_un_bus():
    resultado = evaluar_autonomia(
        combustible_pct=10,
        tipo_vehiculo="bus",
        distancia_restante_km=100,
        consumo_por_km=0.35,
    )

    assert resultado["combustible_disponible_litros"] == 20.0
    assert resultado["combustible_necesario_litros"] == 35.0
    assert resultado["alerta_combustible"] == "ALERTA_COMBUSTIBLE"


def test_autonomia_suficiente_para_un_taxi():
    resultado = evaluar_autonomia(
        combustible_pct=80,
        tipo_vehiculo="taxi",
        distancia_restante_km=50,
        consumo_por_km=0.09,
    )

    assert resultado["combustible_disponible_litros"] == 40.0
    assert resultado["combustible_necesario_litros"] == 4.5
    assert resultado["alerta_combustible"] == "AUTONOMIA_SUFFICIENTE"