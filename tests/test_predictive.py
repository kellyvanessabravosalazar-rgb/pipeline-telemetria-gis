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
    