from shapely.geometry import Point, Polygon


def test_punto_dentro_de_geocerca():
    geocerca = Polygon([
        (-76.54, 3.44),
        (-76.52, 3.44),
        (-76.52, 3.46),
        (-76.54, 3.46),
        (-76.54, 3.44)
    ])

    punto_gps = Point(-76.5325, 3.4510)

    assert geocerca.contains(punto_gps)
    