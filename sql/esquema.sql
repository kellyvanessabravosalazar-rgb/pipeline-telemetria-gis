-- Estructura de la base de datos para el proyecto de telemetría GIS.

CREATE EXTENSION IF NOT EXISTS postgis;

-- Tabla donde se guardan los datos que llegan de los vehículos.
CREATE TABLE IF NOT EXISTS public.telemetry (
id SERIAL PRIMARY KEY,
vehicle_id VARCHAR NOT NULL,
report_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
latitude DOUBLE PRECISION NOT NULL,
longitude DOUBLE PRECISION NOT NULL,
speed_kmh DOUBLE PRECISION NOT NULL,
fuel_pct DOUBLE PRECISION NOT NULL,
geom geometry(Point, 4326) NOT NULL
);

-- Tabla con las geocercas y el límite de velocidad de cada zona.
CREATE TABLE IF NOT EXISTS public.geofences (
id SERIAL PRIMARY KEY,
name VARCHAR NOT NULL,
speed_limit_kmh DOUBLE PRECISION NOT NULL,
geom geometry(Polygon, 4326) NOT NULL
);

-- Índice para agilizar las consultas por ubicación de los vehículos.
CREATE INDEX IF NOT EXISTS idx_telemetry_geom
ON public.telemetry
USING GIST (geom);

-- Índice espacial para consultar las geocercas.
CREATE INDEX IF NOT EXISTS idx_geofences_geom
ON public.geofences
USING GIST (geom);

-- Índice para buscar los registros de cada vehículo por fecha.
CREATE INDEX IF NOT EXISTS idx_telemetry_vehicle_time
ON public.telemetry (vehicle_id, report_time DESC);

-- Vista para revisar las alertas de velocidad y combustible.
CREATE OR REPLACE VIEW public.alertas_vehiculos AS
SELECT
t.id AS registro_id,
t.vehicle_id,
t.report_time,
t.latitude,
t.longitude,
t.speed_kmh,
t.fuel_pct,
g.name AS zona,
CASE
WHEN g.id IS NULL THEN 'FUERA_DE_GEOCERCA'
WHEN t.speed_kmh > g.speed_limit_kmh THEN 'EXCESO_VELOCIDAD'
ELSE 'VELOCIDAD_DENTRO_DEL_LIMITE'
END AS alerta_velocidad,
CASE
WHEN t.fuel_pct <= 20 THEN 'ALERTA_COMBUSTIBLE'
ELSE 'COMBUSTIBLE_SUFICIENTE'
END AS alerta_combustible
FROM public.telemetry AS t
LEFT JOIN public.geofences AS g
ON ST_Within(t.geom, g.geom);

-- Vista que se utiliza para mostrar los datos en el mapa.
CREATE OR REPLACE VIEW public.mapa_telemetria AS
SELECT
registro_id,
vehicle_id,
report_time,
latitude,
longitude,
speed_kmh,
fuel_pct,
zona,
alerta_velocidad,
alerta_combustible,
ST_SetSRID(ST_MakePoint(longitude, latitude), 4326) AS geom
FROM public.alertas_vehiculos;