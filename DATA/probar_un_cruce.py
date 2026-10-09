import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

parametros = urlencode({
    "street": "Calle 38A",
    "city": "Cali",
    "state": "Valle del Cauca",
    "country": "Colombia",
    "format": "jsonv2",
    "limit": 5,
    "countrycodes": "co",
    "addressdetails": 1
})

url = f"https://nominatim.openstreetmap.org/search?{parametros}"

solicitud = Request(
    url,
    headers={"User-Agent": "ProyectoAcademicoGISCali/1.0"}
)

with urlopen(solicitud, timeout=30) as respuesta:
    resultados = json.loads(respuesta.read().decode("utf-8"))

if not resultados:
    print("No se encontraron coincidencias.")
else:
    for resultado in resultados:
        print("Lugar:", resultado.get("display_name"))
        print("Latitud:", resultado.get("lat"))
        print("Longitud:", resultado.get("lon"))
        print("---")