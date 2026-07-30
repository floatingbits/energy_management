from app.forecasting.enums import ForecastMetric


OPEN_METEO_VARIABLES = {
    "temperature_2m": ForecastMetric.TEMPERATURE,
    "cloud_cover": ForecastMetric.CLOUD_COVER,
    "wind_speed_10m": ForecastMetric.WIND_SPEED,
}