from services.vehicle_data import obtener_datos_vehiculo


def test_obtener_datos_vehiculo_existente():
    resultado = obtener_datos_vehiculo("BUS_001")

    assert resultado is not None
    assert resultado["tipo_vehiculo"] == "bus"
    assert resultado["consumo_litros_km"] == 0.35


def test_obtener_datos_vehiculo_inexistente():
    resultado = obtener_datos_vehiculo("BUS_PRUEBA_01")

    assert resultado is None