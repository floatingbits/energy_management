from enum import StrEnum


class WeatherVariable(StrEnum):
    WIND_SPEED = "wind_speed"
    CLOUD_COVER = "cloud_cover"
    TEMPERATURE = "temperature"

    GLOBAL_IRRADIANCE = "global_irradiance"
    DIRECT_RADIATION = "direct_radiation"
    DIFFUSE_RADIATION = "diffuse_radiation"

    PRECIPITATION = "precipitation"

    RELATIVE_HUMIDITY = "relative_humidity"

    PRESSURE = "pressure"