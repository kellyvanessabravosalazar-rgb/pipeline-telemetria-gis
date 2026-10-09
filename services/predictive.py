from services.vehicle_config import CAPACIDAD_TANQUE_LITROS


def calcular_alerta_combustible(
    combustible_actual,
    distancia_restante_km,
    consumo_por_km,
):
    """Compara el combustible disponible con el necesario para la ruta."""
    if combustible_actual < 0:
        raise ValueError("El combustible no puede ser negativo.")

    if distancia_restante_km < 0:
        raise ValueError("La distancia restante no puede ser negativa.")

    if consumo_por_km <= 0:
        raise ValueError("El consumo por kilómetro debe ser mayor que cero.")

    combustible_necesario = distancia_restante_km * consumo_por_km

    if combustible_actual <= combustible_necesario:
        return "ALERTA_COMBUSTIBLE"

    return "AUTONOMIA_SUFFICIENTE"


def convertir_porcentaje_a_litros(combustible_pct, tipo_vehiculo):
    """Convierte el porcentaje de combustible en litros estimados."""
    if not 0 <= combustible_pct <= 100:
        raise ValueError("El porcentaje debe estar entre 0 y 100.")

    tipo = tipo_vehiculo.strip().lower()

    if tipo not in CAPACIDAD_TANQUE_LITROS:
        raise ValueError(f"Tipo de vehículo desconocido: {tipo_vehiculo}")

    capacidad = CAPACIDAD_TANQUE_LITROS[tipo]
    return (combustible_pct / 100) * capacidad


def evaluar_autonomia(
    combustible_pct,
    tipo_vehiculo,
    distancia_restante_km,
    consumo_por_km,
):
    """Evalúa si el combustible alcanza para terminar la ruta."""
    combustible_litros = convertir_porcentaje_a_litros(
        combustible_pct,
        tipo_vehiculo,
    )

    combustible_necesario = distancia_restante_km * consumo_por_km

    alerta = calcular_alerta_combustible(
        combustible_actual=combustible_litros,
        distancia_restante_km=distancia_restante_km,
        consumo_por_km=consumo_por_km,
    )

    return {
        "combustible_disponible_litros": round(combustible_litros, 2),
        "combustible_necesario_litros": round(combustible_necesario, 2),
        "alerta_combustible": alerta,
    }