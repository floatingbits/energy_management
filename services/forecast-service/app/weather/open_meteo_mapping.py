from app.weather.variables import WeatherVariable

OPEN_METEO_VARIABLES = {
    "temperature_2m": WeatherVariable.TEMPERATURE,
    "cloud_cover": WeatherVariable.CLOUD_COVER,
    "wind_speed_10m": WeatherVariable.WIND_SPEED,
}