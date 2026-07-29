from enum import StrEnum


class ForecastMetric(StrEnum):
    WIND_SPEED = "wind_speed"
    TEMPERATURE = "temperature"
    CLOUD_COVER = "cloud_cover"

    ACTIVE_POWER = "active_power"

    ELECTRICITY_PRICE = "electricity_price"


class ForecastValueType(StrEnum):
    FORECAST = "forecast"
    MEASURED = "measured"