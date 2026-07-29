from enum import StrEnum


class WeatherVariable(StrEnum):
    WIND_SPEED = "wind_speed"

    TEMPERATURE = "temperature"

    CLOUD_COVER = "cloud_cover"

    DIRECT_RADIATION = "direct_radiation"

    DIFFUSE_RADIATION = "diffuse_radiation"

    GLOBAL_RADIATION = "global_radiation"

    PRECIPITATION = "precipitation"

    RELATIVE_HUMIDITY = "relative_humidity"

    PRESSURE = "pressure"